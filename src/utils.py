import os
import re
import time
import json
import html2text
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from playwright.sync_api import sync_playwright
from structured_outputs import JobInformation, JobScores, CoverLetter, CallScript
from prompts import (
    SCRAPER_PROMPT_TEMPLATE, 
    SCORE_JOBS_PROMPT_TEMPLATE, 
    GENERATE_COVER_LETTER_PROMPT_TEMPLATE,
    GENERATE_INTRO_MESSAGE_PROMPT_TEMPLATE
)
from apify_client import ApifyClient
import asyncio

SCRAPED_JOBS_FOLDER = "./files/upwork_job_listings/"

def call_gemini_api(
    prompt: str, response_schema=None, model="gemini-1.5-flash"
) -> tuple:
    # Placeholder for AI API call, needs actual implementation
    pass

def scrape_website_to_markdown(url: str) -> str:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context(user_agent=USER_AGENT)

        page = context.new_page()
        page.goto(url)
        html_content = page.content()

        browser.close()

    # Convert HTML to markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_tables = False
    markdown_content = h.handle(html_content)

    # Clean up excess newlines
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)
    markdown_content = markdown_content.strip()

    return markdown_content

async def run_apify_actor(query: str) -> list:
    client = ApifyClient(os.getenv('APIFY_API_TOKEN'))
    actor_id = "your-actor-id-here"  # Replace with your actual actor ID

    # Run the actor
    run = await client.actor(actor_id).call(run_input={"query": query})
    
    # Wait for the actor to finish
    while True:
        run_status = await client.run(run['id']).get()
        if run_status['status'] == 'SUCCEEDED':
            break
        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

    # Fetch the results
    dataset_items = await client.dataset(run['defaultDatasetId']).iterate_items()
    jobs =[item async for item in dataset_items]

    return jobs

async def process_jobs(jobs: list) -> list:
    processed_jobs = []
    for job in jobs:
        job_info = JobInformation(
            title=job.get("title", ""),
            description=job.get("description", ""),
            url=job.get("url", ""),
            # Add more fields as needed
        )

        # Assuming you have a profile defined somewhere or passed to this function
        profile = "Your freelancer profile details here..."
        
        # Generate prompt for scoring
        prompt = SCORE_JOBS_PROMPT_TEMPLATE.format(
            profile=profile,
            jobs=json.dumps([job_info.dict()])  # Convert to JSON string for the prompt
        )

        # Call AI service for scoring, this is a placeholder, replace with actual AI call
        job_score_dict, _ = await call_gemini_api(prompt, JobScores)

        # Convert AI response to JobScores model
        job_score = JobScores(**job_score_dict)

        # Combine job information with AI-generated score
        processed_job = {
            "job_info": job_info.dict(),
            "score": job_score.dict()
        }
        processed_jobs.append(processed_job)
    
    return processed_jobs

async def generate_document(document_type: str, job_title: str, job_description: str, skills_required: list, profile: str) -> str:
    if document_type == "cover_letter":
        prompt = GENERATE_COVER_LETTER_PROMPT_TEMPLATE.format(profile=profile, job_description=job_description)
    elif document_type == "intro_message":
        prompt = GENERATE_INTRO_MESSAGE_PROMPT_TEMPLATE.format(job_title=job_title, skills_required=skills_required, profile=profile)
    else:
        raise ValueError(f"Unknown document type: {document_type}")

    # Placeholder for AI-generated document, replace with actual AI call
    completion, _ = await call_gemini_api(prompt, CoverLetter if document_type == "cover_letter" else CallScript)
    return completion.get("letter") if document_type == "cover_letter" else completion.get("script")

def save_job_data_to_csv(jobs_data):
    os.makedirs(SCRAPED_JOBS_FOLDER, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{SCRAPED_JOBS_FOLDER}scraped_jobs_{date_str}.csv"
    pd.DataFrame(jobs_data).to_csv(filename, index=False)

def read_text_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines =[line.strip() for line in lines if line.strip()]
        return "".join(lines)