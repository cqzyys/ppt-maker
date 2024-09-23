import base64
import os
from pathlib import Path
import sys
from openai import OpenAI
from xid import XID
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(PROJECT_PATH))
from src.logger import get_logger
from src.utils import valid_path

__all__=["text2image_openai_gr","text2image_openai"]

logger = get_logger(__name__)
client = OpenAI()
def text2image_openai_gr(image_prompt:str="a white siamese cat"):
    b64_json = text2image_openai(image_prompt)
    bytes_data = base64.b64decode(b64_json)
    img_path = valid_path(PROJECT_PATH / f"tmp/image/{XID().string()}.png")
    with open(img_path, "wb") as f:
        f.write(bytes_data)
    return img_path

def text2image_openai(image_prompt:str):
    response = client.images.generate(
        model=os.environ.get("IMAGE_MODEL") if os.environ.get("IMAGE_MODEL") is not None else "dall-e-3",
        prompt=image_prompt,
        size="512x512",
        quality="standard",
        response_format="b64_json",
        n=1,
    )
    return response.data[0].b64_json

if __name__ == "__main__":
    text2image_openai_gr()