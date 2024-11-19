import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

def send_email(recipient_email, jobs):
    """Sends matched jobs email (used by process_task)."""
    try:
        smtp_server = os.environ['SMTP_SERVER']
        smtp_port = int(os.environ['SMTP_PORT'])
        smtp_username = os.environ['SMTP_USERNAME']
        smtp_password = os.environ['SMTP_PASSWORD']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Dine matchede jobber"
        msg['From'] = smtp_username
        msg['To'] = recipient_email

        # Use process_task template
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'process_task', 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('email.html')

        html = template.render(jobs=jobs)
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        logger.info(f"Matched jobs email sent to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"Error sending matched jobs email: {e}", exc_info=True)
        return False

def send_email_custom(recipient_email, cover_letter, job_ad_link=None):
    """Sends single cover letter email (used by generate_cover_letter)."""
    try:
        smtp_server = os.environ['SMTP_SERVER']
        smtp_port = int(os.environ['SMTP_PORT'])
        smtp_username = os.environ['SMTP_USERNAME']
        smtp_password = os.environ['SMTP_PASSWORD']

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Ditt genererte søknadsbrev"
        msg['From'] = smtp_username
        msg['To'] = recipient_email

        # Use generate_cover_letter template
        templates_dir = os.path.join(os.path.dirname(__file__), '..', 'generate_cover_letter', 'templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('cover_letter_email.html')

        html = template.render(
            cover_letter=cover_letter,
            job_ad_link=job_ad_link if job_ad_link else None
        )

        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        logger.info(f"Cover letter email sent to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"Error sending cover letter email: {e}", exc_info=True)
        return False
