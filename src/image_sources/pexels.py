import json
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(PROJECT_PATH))
from src.logger import get_logger

logger = get_logger(__name__)
def query_image(keyword:str):
    url = f"https://api.pexels.com/v1/search?query={keyword}&orientation=landscape&per_page=1"
    headers = {
        "Authorization": os.environ.get("PEXELS_API_KEY"),
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0"
    }
    res = requests.get(url, headers=headers)
    url = json.loads(res.text).get("photos")[0].get("src").get("original")
    return url


if __name__ == "__main__":
    url = query_image("solar system")