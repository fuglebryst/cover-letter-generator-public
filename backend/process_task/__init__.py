import logging
import os
import json
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from shared_code.cv_parser import parse_cv
from shared_code.matcher import match_jobs
from shared_code.cover_letter_generator import generate_cover_letter
from shared_code.email_sender import send_email
#from shared_code.secret_loader import load_secrets
from openai import OpenAI
import datetime
import gc

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

def main(msg: str) -> None:
    logger.info('Processing process_task function.')

    try:
        # Load secrets
        #load_secrets()
        openai_api_key = os.getenv('OPENAI_API_KEY')

        # Instantiate OpenAI client
        client = OpenAI(api_key=openai_api_key)

        # Parse JSON payload
        task_payload = json.loads(msg)
        if not task_payload:
            logger.error("No task payload provided.")
            return

        email = task_payload.get('email')
        job_preferences = task_payload.get('job_preferences', '')
        fylke = task_payload.get('fylke', '')
        kommune_bydel = task_payload.get('kommune_bydel', '')
        cv_file_path = task_payload.get('cv_file_path')

        if not email or not cv_file_path:
            logger.error("Email or CV file path missing in task payload.")
            return

        # Download CV file from Azure Blob Storage
        storage_connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        container_name, blob_name = cv_file_path.split('/', 1)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        _, file_extension = os.path.splitext(blob_name)
        local_cv_path = f'/tmp/temp_cv{file_extension}'
        with open(local_cv_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        logger.info(f"CV file downloaded to {local_cv_path}")

        cv_text = parse_cv(local_cv_path)

        if not cv_text:
            logger.error("Failed to parse CV.")
            return

        # Initialize Cosmos DB client
        cosmos_url = os.environ['COSMOS_DB_ENDPOINT']
        cosmos_key = os.environ['COSMOS_DB_KEY']
        client_cosmos = CosmosClient(cosmos_url, credential=cosmos_key)

        database_name = os.environ.get('COSMOS_DB_DATABASE_NAME', 'YourDatabaseName')
        database = client_cosmos.get_database_client(database_name)

        container_name = 'jobs'
        container = database.get_container_client(container_name)

        # Fetch jobs from Cosmos DB
        logger.info("Fetching jobs from Cosmos DB...")
        one_week_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
        query = "SELECT * FROM c WHERE c.timestamp >= @one_week_ago"
        parameters = [{"name": "@one_week_ago", "value": one_week_ago}]
        jobs_query = container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        )
        jobs = list(jobs_query)

        if not jobs:
            logger.error("No jobs fetched from Cosmos DB.")
            return

        # Match jobs using matcher
        logger.info("Matching jobs with CV and preferences...")
        matched_jobs = match_jobs(client, cv_text, jobs, job_preferences, fylke, kommune_bydel)

        # Clean up large variables
        del jobs
        gc.collect()

        # Limit to top N matched jobs
        top_n = 5
        matched_jobs = matched_jobs[:top_n]

        if not matched_jobs:
            logger.info("No matched jobs found.")
            return

        # Generate cover letters for matched jobs
        logger.info("Generating cover letters for matched jobs...")
        for job in matched_jobs:
            cover_letter = generate_cover_letter(client, cv_text, '', job['description'])
            job['cover_letter'] = cover_letter

        # Send email with matched jobs and cover letters
        logger.info("Sending email to user...")
        send_email(email, matched_jobs)

        # Clean up matched jobs
        del matched_jobs
        gc.collect()

        # Delete the CV file from Blob Storage
        blob_client.delete_blob()
        logger.info(f"Deleted CV file from {container_name}/{blob_name}")

    except Exception as e:
        logger.error(f"Error processing task: {e}", exc_info=True)
