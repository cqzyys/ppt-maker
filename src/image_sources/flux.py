from pathlib import Path
import random
import sys
import torch
from xid import XID
from PIL import Image
from diffusers import FluxPipeline
PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(PROJECT_PATH))
from src.logger import get_logger
from src.utils import valid_path

from diffusers import FluxTransformer2DModel, FluxPipeline
from transformers import T5EncoderModel
from optimum.quanto import freeze, qfloat8, quantize

__all__ = ["text2image_flux_gr","text2image_flux","text2image_flux_fp8_gr","text2image_flux_fp8"]

logger = get_logger(__name__)
pipe = None
pipe_fp8 = None
def text2image_flux_gr(
    image_prompt="sci-fi, closeup portrait photo of man in combat clothes, face, long hair, slim body, high quality, film grain",
    num_inference_steps=4,
    guidance_scale=0.0      
):
    kwargs = {"num_inference_steps":num_inference_steps,"guidance_scale":guidance_scale}
    img = text2image_flux(prompt=image_prompt,kwargs=kwargs)
    img_path = valid_path(PROJECT_PATH / f"tmp/image/{XID().string()}.png")
    img.save(img_path)
    return img_path


def text2image_flux(
    prompt:str,
    kwargs:dict={
        "num_inference_steps":4,
        "guidance_scale":0.0
    }
)->Image:
    global pipe
    if pipe is None:
        pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
        pipe.enable_sequential_cpu_offload()
    img = pipe(
        prompt=prompt,
        guidance_scale=kwargs["guidance_scale"],
        output_type="pil",
        num_inference_steps=kwargs["num_inference_steps"],
        max_sequence_length=256,
        #generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]
    return img

def text2image_flux_fp8_gr(
    image_prompt="sci-fi, closeup portrait photo of man in combat clothes, face, long hair, slim body, high quality, film grain",
    num_inference_steps=4,
    guidance_scale=0.0
):
    img = text2image_flux_fp8(prompt=image_prompt, num_inference_steps=num_inference_steps, guidance_scale=guidance_scale)
    img_path = valid_path(PROJECT_PATH / f"tmp/image/{XID().string()}.png")
    img.save(img_path)
    return img_path

def text2image_flux_fp8(
        prompt:str,
        num_inference_steps=4,
        guidance_scale=0.0
) ->Image:
    global pipe_fp8
    if pipe_fp8 is None:
        bfl_repo = "black-forest-labs/FLUX.1-schnell"
        dtype = torch.bfloat16
        transformer = FluxTransformer2DModel.from_single_file("https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-schnell-fp8-e4m3fn.safetensors", torch_dtype=dtype)
        quantize(transformer, weights=qfloat8)
        freeze(transformer)
        text_encoder_2 = T5EncoderModel.from_pretrained(bfl_repo, subfolder="text_encoder_2", torch_dtype=dtype)
        quantize(text_encoder_2, weights=qfloat8)
        freeze(text_encoder_2)
        pipe_fp8 = FluxPipeline.from_pretrained(bfl_repo, transformer=None, text_encoder_2=None, torch_dtype=dtype)
        pipe_fp8.transformer = transformer
        pipe_fp8.text_encoder_2 = text_encoder_2
        pipe_fp8.enable_model_cpu_offload()
    prompt += ", high quality, film grain, realist style"
    image = pipe_fp8(
        prompt=prompt,
        guidance_scale=guidance_scale,
        output_type="pil",
        num_inference_steps=num_inference_steps,
        generator=torch.Generator("cpu").manual_seed(random.randint(0, 2**32 - 1)),
    ).images[0]
    return image

if __name__ == "__main__":
    text2image_flux_fp8_gr("rocky planets, gas giants, hydrogen, helium")