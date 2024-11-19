import logging
import azure.functions as func
import json
import os
from shared_code.cv_parser import parse_cv
from shared_code.cover_letter_generator import generate_cover_letter, convert_to_docx
from shared_code.job_scraper import scrape_job_details
from shared_code.email_sender import send_email_custom
import tempfile
from openai import OpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Add CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Expose-Headers': 'Content-Disposition'
    }

    # Handle OPTIONS request (CORS preflight)
    if req.method.lower() == "options":
        return func.HttpResponse(
            status_code=200,
            headers=headers
        )

    logging.info('Processing generate_cover_letter function.')
    logging.info(f'Request files: {list(req.files.keys())}')  # Convert to list for better logging
    logging.info(f'Request form: {list(req.form.keys())}')    # Convert to list for better logging
    
    try:
        # Get form data
        form = req.form
        if not form:
            return func.HttpResponse(
                json.dumps({'message': 'No form data received.'}),
                status_code=400,
                headers=headers,
                mimetype='application/json'
            )

        action_option = form.get('action', '').strip()
        
        # Validate action
        if action_option not in ['generate', 'download', 'email']:
            return func.HttpResponse(
                json.dumps({'message': 'Ugyldig handling valgt.'}),
                status_code=400,
                headers=headers,
                mimetype='application/json'
            )

        # Handle download and email actions
        if action_option in ['download', 'email']:
            cover_letter = form.get('cover_letter', '').strip()
            if not cover_letter:
                return func.HttpResponse(
                    json.dumps({'message': 'Ingen søknadsbrev innhold oppgitt.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

            if action_option == 'download':
                docx_io = convert_to_docx(cover_letter)
                if not docx_io:
                    return func.HttpResponse(
                        json.dumps({'message': 'Kunne ikke konvertere til DOCX.'}),
                        status_code=500,
                        headers=headers,
                        mimetype='application/json'
                    )
                
                download_headers = headers.copy()
                download_headers['Content-Disposition'] = 'attachment; filename=Soknadsbrev.docx'
                download_headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                
                return func.HttpResponse(
                    docx_io.getvalue(),
                    status_code=200,
                    headers=download_headers,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )

            elif action_option == 'email':
                email = form.get('email', '').strip()
                if not email:
                    return func.HttpResponse(
                        json.dumps({'message': 'Ingen e-postadresse oppgitt.'}),
                        status_code=400,
                        headers=headers,
                        mimetype='application/json'
                    )
                
                job_ad_link = form.get('job_ad_link', '').strip()
                if send_email_custom(email, cover_letter, job_ad_link):
                    return func.HttpResponse(
                        json.dumps({'message': 'Søknadsbrev sendt via e-post.'}),
                        status_code=200,
                        headers=headers,
                        mimetype='application/json'
                    )
                else:
                    return func.HttpResponse(
                        json.dumps({'message': 'Kunne ikke sende e-post.'}),
                        status_code=500,
                        headers=headers,
                        mimetype='application/json'
                    )

        # Handle generate action
        elif action_option == 'generate':
            # Get OpenAI client
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if not openai_api_key:
                return func.HttpResponse(
                    json.dumps({'message': 'OpenAI API key not configured'}),
                    status_code=500,
                    headers=headers,
                    mimetype='application/json'
                )
            
            client = OpenAI(api_key=openai_api_key)
            
            cv_file = req.files.get('cv_file')
            if not cv_file:
                logging.error("No CV file found in request")
                return func.HttpResponse(
                    json.dumps({'message': 'Ingen CV-fil lastet opp.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

            logging.info(f"CV file received: {cv_file.filename}")

            email = form.get('email', '').strip()
            job_ad_option = form.get('job_ad_option', 'manual').strip()

            # Get job description based on option
            if job_ad_option == 'link':
                job_ad_link = form.get('job_ad_link', '').strip()
                if not job_ad_link:
                    return func.HttpResponse(
                        json.dumps({'message': 'Ingen jobbannonse link oppgitt.'}),
                        status_code=400,
                        headers=headers,
                        mimetype='application/json'
                    )
                logging.info(f"Scraping job details from: {job_ad_link}")
                job_description, _, _ = scrape_job_details(job_ad_link)
                if job_description == "Could not fetch job description.":
                    return func.HttpResponse(
                        json.dumps({'message': 'Kunne ikke hente jobbeskrivelse fra Finn.no'}),
                        status_code=400,
                        headers=headers,
                        mimetype='application/json'
                    )
            else:
                job_description = form.get('job_description', '').strip()
                job_ad_link = None

            if not job_description:
                return func.HttpResponse(
                    json.dumps({'message': 'Ingen jobbeskrivelse oppgitt.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

            if not cv_file or cv_file.filename == '':
                return func.HttpResponse(
                    json.dumps({'message': 'Ingen CV-fil lastet opp.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

            # Save CV file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                cv_file.save(temp_file)
                temp_file_path = temp_file.name

            # Parse CV
            cv_text = parse_cv(temp_file_path)
            
            # Clean up temp file
            os.unlink(temp_file_path)

            if not cv_text:
                return func.HttpResponse(
                    json.dumps({'message': 'Kunne ikke lese CV-filen.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

            # Generate cover letter
            cover_letter = generate_cover_letter(client, cv_text, '', job_description)

            if not cover_letter:
                return func.HttpResponse(
                    json.dumps({'message': 'Kunne ikke generere søknadsbrev.'}),
                    status_code=500,
                    headers=headers,
                    mimetype='application/json'
                )

            if action_option == 'generate':
                return func.HttpResponse(
                    json.dumps({'cover_letter': cover_letter}),
                    status_code=200,
                    headers=headers,
                    mimetype='application/json'
                )
            elif action_option == 'download':
                # Convert to DOCX and return
                docx_io = convert_to_docx(cover_letter)
                if not docx_io:
                    return func.HttpResponse(
                        json.dumps({'message': 'Kunne ikke konvertere til DOCX.'}),
                        status_code=500,
                        headers=headers,
                        mimetype='application/json'
                    )
                
                # Add download headers
                download_headers = headers.copy()
                download_headers['Content-Disposition'] = 'attachment; filename=Soknadsbrev.docx'
                download_headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                
                return func.HttpResponse(
                    docx_io.getvalue(),
                    status_code=200,
                    headers=download_headers,
                    mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
            elif action_option == 'email':
                if not email:
                    logging.error("No email provided for sending.")
                    return func.HttpResponse(
                        json.dumps({'message': 'Ingen e-postadresse oppgitt.'}),
                        status_code=400,
                        headers=headers,
                        mimetype='application/json'
                    )
                job_ad_link = form.get('job_ad_link', '').strip()
                send_email_custom(email, cover_letter, job_ad_link)
                return func.HttpResponse(
                    json.dumps({'message': 'Søknadsbrev sendt via e-post.'}),
                    status_code=200,
                    headers=headers,
                    mimetype='application/json'
                )
            else:
                return func.HttpResponse(
                    json.dumps({'message': 'Ugyldig handling valgt.'}),
                    status_code=400,
                    headers=headers,
                    mimetype='application/json'
                )

    except Exception as e:
        logging.error(f"Error during cover letter generation: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({'message': 'Det oppstod en feil. Vennligst prøv igjen.'}),
            status_code=500,
            headers=headers,
            mimetype='application/json'
        )
