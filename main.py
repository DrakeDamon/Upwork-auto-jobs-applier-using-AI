import os
import sys
from apify_client import ApifyClient
import asyncio

# Append the src directory to sys.path if it's not already there
src_path = os.path.abspath('src')
if src_path not in sys.path:
    sys.path.append(src_path)

from utils import run_apify_actor

async def main():
    # Retrieve API token from environment variable
    token = os.getenv('APIFY_API_TOKEN')
    if not token:
        raise ValueError("API token not found. Set the APIFY_API_TOKEN environment variable.")

    # Initialize the Apify client
    client = ApifyClient(token)

    # Example query - you might want to get this from actor input
    query = "AI agent"
    
    # Run your scraping logic
    jobs = await run_apify_actor(query)
    
    # Get or create a dataset
    dataset = await client.dataset().get_or_create()
    
    # Push the results to an Apify dataset
    await dataset.push_items(jobs)

if __name__ == "__main__":
    asyncio.run(main())