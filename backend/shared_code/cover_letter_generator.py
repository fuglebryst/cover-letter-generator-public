import logging
from io import BytesIO
from docx import Document

logger = logging.getLogger(__name__)

def generate_cover_letter(client, cv_text, personal_intro, job_description, language="Norwegian"):
    """Generates a cover letter using OpenAI's Chat Completion API."""
    try:
        messages = [
            {
                'role': 'system',
                'content': f'You are an expert career advisor writing excellent cover letters in {language}.'
            },
            {
                'role': 'user',
                'content': f"""Please write only the content of a personalized cover letter in {language} based on the following information. Do not include salutations, sender or recipient information, date, or any personal details beyond what is relevant to the cover letter content. The cover letter should be in the first person and tailored to highlight how my skills and experience make me an excellent candidate for the position.

**My CV:** {cv_text}

**Job Description:** {job_description}
"""
            }
        ]

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=1500,
            temperature=0.7
        )

        cover_letter = response.choices[0].message.content.strip()
        
        if not cover_letter:
            logger.error("Empty response from OpenAI API")
            return "Could not generate cover letter."

        return cover_letter
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}", exc_info=True)
        return "Could not generate cover letter."

def convert_to_docx(text):
    """Converts text to a DOCX file."""
    try:
        doc = Document()
        doc.add_paragraph(text)
        
        # Save to BytesIO object
        docx_io = BytesIO()
        doc.save(docx_io)
        docx_io.seek(0)
        
        return docx_io
    except Exception as e:
        logger.error(f"Error converting to DOCX: {e}", exc_info=True)
        return None
