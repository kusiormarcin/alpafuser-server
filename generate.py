from diffusers import DiffusionPipeline
import torch
from PIL import Image
import uuid
import sys
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))

output_dir = "output"

env_path = os.path.join(current_dir, ".env")

app_url = os.getenv("APP_URL", "http://127.0.0.1:5000")

load_dotenv(env_path)

diffusion_model = os.getenv("DIFFUSION_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")

def generate_image(prompt) -> Image:
    pipeline = DiffusionPipeline.from_pretrained(diffusion_model, torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipeline = pipeline.to(device="mps")
    image = pipeline(prompt).images[0]
    return image

def save_image_to_file(image: Image) -> str:
    random_uuid = uuid.uuid4()
    filename = f"{random_uuid}.jpg"
    filepath = os.path.join(current_dir, output_dir, filename)
    image.save(filepath, "JPEG", quality=100, optimize=True)
    return f"{app_url}/{output_dir}/{filename}"

prompt = sys.argv[1]
image = generate_image(prompt)
result = save_image_to_file(image)
print(result)