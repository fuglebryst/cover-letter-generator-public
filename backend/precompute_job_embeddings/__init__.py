import logging
import os
from azure.cosmos import CosmosClient
from openai import OpenAI
import datetime
import azure.functions as func

from shared_code.secret_loader import load_secrets

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(queueItem: str) -> None:
    logging.info('Processing precompute_job_embeddings function.')

    try:
        # Log the message received from the queue
        logging.info(f"Received queue message: {queueItem}")

        # Load secrets (if needed)
        load_secrets()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        client = OpenAI(api_key=openai_api_key)

        # Initialize Cosmos DB client
        url = os.environ['COSMOS_DB_ENDPOINT']
        key = os.environ['COSMOS_DB_KEY']
        client_cosmos = CosmosClient(url, credential=key)

        database_name = os.environ.get('COSMOS_DB_DATABASE_NAME', 'YourDatabaseName')
        database = client_cosmos.get_database_client(database_name)

        container_name = 'jobs'
        container = database.get_container_client(container_name)

        # Fetch all jobs without embeddings
        logger.info("Fetching jobs without embeddings...")
        query = "SELECT * FROM c WHERE NOT IS_DEFINED(c.embedding)"
        jobs = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not jobs:
            logger.info("No jobs without embeddings found.")
            return

        # Limit the total number of jobs processed per invocation
        MAX_JOBS_TO_PROCESS = 1000
        jobs_to_process = jobs[:MAX_JOBS_TO_PROCESS]
        total_jobs = len(jobs_to_process)
        logger.info(f"Total jobs without embeddings to process: {total_jobs}")

        # Process jobs in batches
        BATCH_SIZE = 20
        for i in range(0, total_jobs, BATCH_SIZE):
            batch_jobs = jobs_to_process[i:i+BATCH_SIZE]
            job_texts = [f"{job.get('title', '')} {job.get('description', '')}" for job in batch_jobs]

            # Generate embeddings for the batch
            embeddings = get_batch_embeddings(client, job_texts)

            if embeddings:
                # Update jobs with embeddings
                for idx, job in enumerate(batch_jobs):
                    embedding = embeddings[idx]
                    job['embedding'] = embedding
                    container.upsert_item(job)
                    logger.info(f"Updated job {job.get('id')} with embedding.")
            else:
                logger.error("Failed to generate embeddings for batch.")
                # Handle the error, maybe retry or log

    except Exception as e:
        logger.error(f"Error computing embeddings: {e}", exc_info=True)

def get_batch_embeddings(client, texts, model="text-embedding-3-small"):
    """Generates embeddings for a batch of texts using OpenAI's embedding model."""
    try:
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings for batch: {e}")
        return None
