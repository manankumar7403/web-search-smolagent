from smolagents.tools import Tool
from diffusers import StableDiffusionPipeline
import torch
from huggingface_hub import cached_download
from PIL import Image
import uuid
import os

class FreeImageGeneratorTool(Tool):
    name = "image_generator"
    description = "Generates an image from a text prompt using Stable Diffusion"

    inputs = {'prompt': {'type': 'string', 'description': 'Text prompt for the image'}}
    output_type = "string"

    def __init__(self, *args, **kwargs):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2", torch_dtype=torch.float16
        ).to("cuda" if torch.cuda.is_available() else "cpu")
        self.is_initialized = True

    def forward(self, prompt: str) -> str:
        image = self.pipe(prompt).images[0]
        filename = f"generated_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join("generated_images", filename)
        os.makedirs("generated_images", exist_ok=True)
        image.save(filepath)
        return filepath
