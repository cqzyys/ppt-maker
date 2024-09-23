import json
import os
import requests
from pathlib import Path
import pyunsplash
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = Path(__file__).parent.parent.resolve()

def query_image(keyword:str):
    pu = pyunsplash.PyUnsplash(os.environ.get("UNSPLASH_API_KEY"))
    result = pu.photos(type_='random', count=1, featured=True, query=keyword)
    for photo in result.entries:
        proxies = {'http': 'http://127.0.0.1:7890','https': 'http://127.0.0.1:7890'}
        res = requests.get(photo.link_download_location+"&client_id="+os.environ.get("UNSPLASH_API_KEY"),proxies=proxies)
        url = json.loads(res.text).get("url")
        return url

if __name__ == "__main__":
    url = query_image("solar system")