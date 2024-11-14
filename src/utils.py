import os
import re
import time
import json
import html2text
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from playwright.sync_api import sync_playwright
import google.generativeai as genai
from .structured_outputs import (
    JobInformation,
    JobScores,
    CoverLetter,
    CallScript,
)
from .prompts import (
    SCRAPER_PROMPT_TEMPLATE, 
    SCORE_JOBS_PROMPT_TEMPLATE, 
    GENERATE_COVER_LETTER_PROMPT_TEMPLATE,
    GENERATE_INTRO_MESSAGE_PROMPT_TEMPLATE
)

SCRAPED_JOBS_FOLDER = "./files/upwork_job_listings/"

def call_gemini_api(
    prompt: str, response_schema=None, model="gemini-1.5-flash"
) -> tuple:
    llm = genai.GenerativeModel(model)
    if response_schema is not None:
        llm = genai.GenerativeModel(
            model,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            },
        )

    completion = llm.generate_content(prompt)
    usage_metadata = completion.usage_metadata
    token_counts = {
        "input_tokens": usage_metadata.prompt_token_count,
        "output_tokens": usage_metadata.candidates_token_count,
    }
    try:
        output = json.loads(completion.text)
    except json.JSONDecodeError:
        output = completion.text
    return output, token_counts

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
    # Placeholder for Apify actor run, needs to be implemented with actual Apify interaction
    pass

def process_jobs(jobs: list) -> list:
    # This function should process and analyze jobs, potentially using AI for scoring
    pass

async def generate_document(document_type: str, job_title: str, job_description: str, skills_required: list, profile: str) -> str:
    if document_type == "cover_letter":
        prompt = GENERATE_COVER_LETTER_PROMPT_TEMPLATE.format(profile=profile, job_description=job_description)
    elif document_type == "intro_message":
        prompt = GENERATE_INTRO_MESSAGE_PROMPT_TEMPLATE.format(job_details={"title": job_title, "skills_required": skills_required}, profile=profile)
    else:
        raise ValueError(f"Unknown document type: {document_type}")

    completion, _ = call_gemini_api(prompt, CoverLetter if document_type == "cover_letter" else CallScript)
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