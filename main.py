import os
import sys
from apify_client import ApifyClient
import asyncio
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Append the src directory to sys.path if it's not already there
src_path = os.path.abspath('src')
if src_path not in sys.path:
    sys.path.append(src_path)

from src.utils import run_apify_actor  # Assuming run_apify_actor is in utils.py inside src/

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
    
    # Create a new dataset
    dataset = await client.datasets().create()
    
    # Push the results to the Apify dataset
    await dataset.push_items(jobs)

    # Fetch and print Actor results from the dataset
    async for item in dataset.iterate_items():
        print(item)

if __name__ == "__main__":
    asyncio.run(main())

#changed api