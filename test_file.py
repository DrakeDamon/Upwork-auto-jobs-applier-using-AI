import apify_client
import html2text
import pandas as pd
from tqdm import tqdm
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from dotenv import load_dotenv

print(apify_client.__version__)
print(html2text.__version__)
print(pd.__version__)
print(tqdm.__version__)
print(sync_playwright.__version__)
print(load_dotenv())  # Should return True if a .env file is present and loaded