import sys
import torch
from pathlib import Path
from PIL import Image
from xid import XID
from diffusers import DiffusionPipeline
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(PROJECT_PATH))
from src.logger import get_logger
from src.utils import valid_path

__all__ = ["text2image_sdxl_gr","text2image_sdxl"]

logger = get_logger(__name__)
pipe = None
def text2image_sdxl_gr(
        image_prompt="sci-fi, closeup portrait photo of man in combat clothes, face, long hair, slim body, high quality, film grain",
        negative_prompt="(octane render, render, drawing, anime, bad photo, bad photography:1.3), (worst quality, low quality, blurry:1.2), (bad teeth, deformed teeth, deformed lips), (bad anatomy, bad proportions:1.1), (deformed iris, deformed pupils), (deformed eyes, bad eyes), (deformed face, ugly face, bad face), (deformed hands, bad hands, fused fingers), morbid, mutilated, mutation, disfigured",
        num_inference_steps=8,
        guidance_scale=2.0
    ):
        kwargs = {"negative_prompt":negative_prompt,"num_inference_steps":num_inference_steps,"guidance_scale":guidance_scale}
        img = text2image_sdxl(prompt=image_prompt,kwargs=kwargs)
        #image = Image.open(BytesIO(image_bytes))
        img_path = valid_path(PROJECT_PATH / f"tmp/image/{XID().string()}.png")
        img.save(img_path)
        return img_path

def text2image_sdxl(
        prompt:str,
        kwargs:dict={
            "negative_prompt":"(octane render, render, drawing, anime, bad photo, bad photography:1.3), (worst quality, low quality, blurry:1.2), (bad teeth, deformed teeth, deformed lips), (bad anatomy, bad proportions:1.1), (deformed iris, deformed pupils), (deformed eyes, bad eyes), (deformed face, ugly face, bad face), (deformed hands, bad hands, fused fingers), morbid, mutilated, mutation, disfigured",
            "num_inference_steps":8,
            "guidance_scale":2.0
        }
    )->Image:
    global pipe
    if pipe is None:
        pipe = DiffusionPipeline.from_pretrained("SG161222/RealVisXL_V3.0_Turbo",torch_dtype=torch.float16,variant="fp16")
        pipe.to("cuda")
    result = pipe(prompt=prompt,negative_prompt=kwargs["negative_prompt"],num_inference_steps=kwargs["num_inference_steps"],guidance_scale=kwargs["guidance_scale"])
    img:Image = result["images"][0]
    return img

if __name__ == "__main__":
    image_prompt = "rocky planets, gas giants, hydrogen, helium"
    negative_prompt = "(octane render, render, drawing, anime, bad photo, bad photography:1.3), (worst quality, low quality, blurry:1.2), (bad teeth, deformed teeth, deformed lips), (bad anatomy, bad proportions:1.1), (deformed iris, deformed pupils), (deformed eyes, bad eyes), (deformed face, ugly face, bad face), (deformed hands, bad hands, fused fingers), morbid, mutilated, mutation, disfigured"
    text2image_sdxl_gr(image_prompt=image_prompt)
    