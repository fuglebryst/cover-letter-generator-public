import logging
import azure.functions as func
import datetime
from azure.cosmos import CosmosClient, PartitionKey
import uuid
import asyncio
from shared_code.job_scraper import get_jobs_async, scrape_job_details_async
import os

def main(mytimer: func.TimerRequest, outputQueueItem: func.Out[str]) -> None:
    logging.info('Processing scrape_jobs function.')

    # Check if the function was triggered on schedule
    if mytimer.past_due:
        logging.warning('The timer is past due!')

    try:
        # Initialize Cosmos DB client
        url = os.environ['COSMOS_DB_ENDPOINT']
        key = os.environ['COSMOS_DB_KEY']
        client = CosmosClient(url, credential=key)

        database_name = os.environ.get('COSMOS_DB_DATABASE_NAME', 'YourDatabaseName')
        database = client.create_database_if_not_exists(id=database_name)

        container_name = 'jobs'
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path='/id'),
        )

        # Delete jobs older than a week
        logging.info("Deleting old jobs...")
        one_week_ago = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat()
        query = "SELECT * FROM c WHERE c.timestamp < @one_week_ago"
        parameters = [
            {"name": "@one_week_ago", "value": one_week_ago}
        ]
        items = list(container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        for item in items:
            container.delete_item(item, partition_key=item['id'])

        # Fetch jobs asynchronously
        logging.info("Fetching job listings asynchronously...")
        jobs = asyncio.run(get_jobs_async(max_pages=20))

        if not jobs:
            logging.error("No jobs fetched.")
            return

        # Scrape job details asynchronously
        logging.info("Scraping job details asynchronously...")
        job_urls = [job['link'] for job in jobs]
        job_descriptions = asyncio.run(scrape_job_details_async(job_urls))

        # Combine job descriptions with jobs
        for job, description in zip(jobs, job_descriptions):
            job['description'] = description

        # Filter valid jobs
        valid_jobs = []
        required_fields = ['location', 'description', 'company_name', 'position', 'link', 'title']
        for job in jobs:
            if all(job.get(field) for field in required_fields):
                valid_jobs.append(job)
            else:
                logging.warning(f"Skipping job due to missing fields: {job}")

        if not valid_jobs:
            logging.error("No valid jobs to store.")
            return

        # Store valid jobs in Cosmos DB
        logging.info("Storing valid jobs in Cosmos DB...")

        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for job in valid_jobs:
            job['id'] = job.get('id') or str(uuid.uuid4())
            job['timestamp'] = timestamp
            container.upsert_item(job)

        logging.info(f"Stored {len(valid_jobs)} valid jobs in Cosmos DB.")

        # Send a message to the queue
        outputQueueItem.set("Job scraping completed successfully.")

    except Exception as e:
        logging.error(f"Error during job scraping and storing: {e}", exc_info=True)
