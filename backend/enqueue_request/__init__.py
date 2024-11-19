import logging
import azure.functions as func
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import json

# Allowed file extensions for CV upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def main(req: func.HttpRequest, msg: func.Out[str]) -> func.HttpResponse:
    # Handle OPTIONS request (CORS preflight)
    if req.method.lower() == "options":
        response = func.HttpResponse(status_code=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    logging.info('Processing enqueue_request function.')

    # Add CORS headers to all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    try:
        # Ensure request has form data
        form = req.form
        if not form:
            logging.error("No form data provided.")
            return func.HttpResponse(
                json.dumps({'message': 'No data provided.'}),
                status_code=400,
                mimetype='application/json'
            )

        email = form.get('email', '').strip()
        job_preferences = form.get('job_preferences', '').strip()
        fylke = form.get('fylke', '').strip()
        kommune_bydel = form.get('kommune_bydel', '').strip()

        if not email:
            logging.error("No email provided.")
            return func.HttpResponse(
                json.dumps({'message': 'No email address provided.'}),
                status_code=400,
                mimetype='application/json'
            )

        # Get the CV file from the request
        cv_file = req.files.get('cv_file')
        if not cv_file or cv_file.filename == '':
            logging.error("No CV file uploaded.")
            return func.HttpResponse(
                json.dumps({'message': 'No CV file uploaded.'}),
                status_code=400,
                mimetype='application/json'
            )

        if not allowed_file(cv_file.filename):
            logging.error("Invalid file type uploaded.")
            return func.HttpResponse(
                json.dumps({'message': 'Invalid file type. Allowed types are txt, pdf, docx.'}),
                status_code=400,
                mimetype='application/json'
            )

        # Save CV file to Azure Blob Storage
        filename = secure_filename(cv_file.filename)
        storage_connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
        container_name = 'cvs'  # Make sure this container exists

        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

        blob_client.upload_blob(cv_file.stream, overwrite=True)

        logging.info(f"CV file uploaded to {container_name}/{filename}")

        # Create a task payload
        task_payload = {
            'email': email,
            'job_preferences': job_preferences,
            'fylke': fylke,
            'kommune_bydel': kommune_bydel,
            'cv_file_path': f'{container_name}/{filename}'
        }

        # Enqueue the task
        msg.set(json.dumps(task_payload))
        logging.info(f"Task enqueued with payload: {task_payload}")

        return func.HttpResponse(
            json.dumps({'message': 'Success'}),
            status_code=200,
            headers=headers,
            mimetype='application/json'
        )

    except Exception as e:
        logging.error(f"Error enqueuing task: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({'message': f'An error occurred: {e}'}),
            status_code=500,
            headers=headers,
            mimetype='application/json'
        )
