import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

async def fetch_page(session, url, params=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                logger.error(f"Error fetching page after {max_retries} attempts: {e}")
                return None
            await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff

async def get_jobs_async(max_pages=20):
    base_url = 'https://www.finn.no/job/fulltime/search.html'
    params_list = [{
        'location': '0.20001',  # All of Norway
        'published': '1',       # New today
        'page': page
    } for page in range(1, max_pages + 1)]

    jobs = []

    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'}) as session:
        tasks = [fetch_page(session, base_url, params) for params in params_list]
        pages_content = await asyncio.gather(*tasks)

        for page_num, content in enumerate(pages_content, start=1):
            if content is None:
                continue
            soup = BeautifulSoup(content, 'html.parser')
            job_elements = soup.find_all('article', class_=re.compile(r'\bsf-search-ad\b'))

            if not job_elements:
                logger.info(f"No job results found on page {page_num}.")
                continue

            for job_elem in job_elements:
                # Extract the job title
                title_tag = job_elem.find('h2')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                else:
                    title = 'No title'

                # Extract job URL
                link_tag = title_tag.find('a') if title_tag else None
                job_url = link_tag.get('href') if link_tag else None
                if job_url and not job_url.startswith('http'):
                    job_url = 'https://www.finn.no' + job_url

                # Extract location
                location_tag = job_elem.find('div', class_=re.compile(r'\bs-text-subtle\b'))
                if location_tag:
                    location_text = location_tag.get_text(strip=True)
                    location_parts = location_text.split('|')
                    location = location_parts[-1].strip() if len(location_parts) > 1 else location_text
                else:
                    location = 'Unknown location'

                # Extract position
                position_div = job_elem.select_one('div.font-bold')
                if position_div:
                    position_span = position_div.find('span')
                    if position_span:
                        position = position_span.get_text(strip=True)
                    else:
                        position = 'Unknown position'
                else:
                    position = 'Unknown position'

                # Extract company name
                company_div = job_elem.select_one('div.flex.flex-col.text-xs')
                if company_div:
                    company_span = company_div.find('span')
                    if company_span:
                        company_name = company_span.get_text(strip=True)
                    else:
                        company_name = 'Unknown company'
                else:
                    company_name = 'Unknown company'

                # Skip jobs with unknown values
                if 'Unknown' in (location, position, company_name):
                    logger.info(f"Skipping job with unknown values: {title}")
                    continue

                # Append each job inside the loop
                jobs.append({
                    'title': title,
                    'link': job_url,
                    'location': location,
                    'position': position,
                    'company_name': company_name,
                    # Include other fields as necessary
                })

                logger.info(f"Adding job: {title}")

            logger.info(f"Page {page_num} scraped, total jobs so far: {len(jobs)}")

    return jobs

async def fetch_job_detail(session, job_url, max_retries=3):
    for attempt in range(max_retries):
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with session.get(job_url, timeout=timeout) as response:
                response.raise_for_status()
                content = await response.text()
                return (content, "", None)  # Return tuple format for compatibility
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                logger.error(f"Error fetching job details from {job_url}: {e}")
                return None
            await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff

async def scrape_job_details_async(job_urls):
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(
        headers={'User-Agent': 'Mozilla/5.0'}, 
        timeout=timeout
    ) as session:
        tasks = []
        batch_size = 10
        for i in range(0, len(job_urls), batch_size):
            batch = job_urls[i:i+batch_size]
            batch_tasks = [fetch_job_detail(session, url) for url in batch]
            tasks.extend(batch_tasks)
            if i + batch_size < len(job_urls):
                await asyncio.sleep(1)
                
        pages_content = await asyncio.gather(*tasks, return_exceptions=True)
        job_descriptions = []

        for content in pages_content:
            try:
                if isinstance(content, Exception) or content is None:
                    job_descriptions.append('No description available')
                    continue
                
                # Unpack the tuple
                html_content, _, _ = content
                
                soup = BeautifulSoup(html_content, 'html.parser')
                job_description_div = soup.find('div', class_='import-decoration')
                if job_description_div:
                    job_description = job_description_div.get_text(separator='\n', strip=True)
                else:
                    job_description = 'No description available'
                job_descriptions.append(job_description)
            except Exception as e:
                logger.error(f"Error parsing job description: {str(e)}")
                job_descriptions.append('No description available')

    return job_descriptions

def scrape_job_details(url):
    """Scrapes job details from a single URL."""
    try:
        async def get_description():
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(
                headers={'User-Agent': 'Mozilla/5.0'}, 
                timeout=timeout
            ) as session:
                result = await fetch_job_detail(session, url)
                if result is None:
                    return ("Could not fetch job description.", "", None)
                
                content, _, _ = result
                if not content:
                    return ("Could not fetch job description.", "", None)
                
                soup = BeautifulSoup(content, 'html.parser')
                job_desc_div = soup.find('div', class_='import-decoration')
                description = job_desc_div.get_text(separator='\n', strip=True) if job_desc_div else "Could not fetch job description."
                return (description, "", None)

        return asyncio.run(get_description())
        
    except Exception as e:
        logger.error(f"Error scraping job details from {url}: {str(e)}")
        return ("Could not fetch job description.", "", None)
