from smolagents.tools import Tool
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import uuid
import os

class FreeImageGeneratorTool(Tool):
    name = "image_generator"
    description = "Generates an image from a text prompt using Stable Diffusion"
    inputs = {'prompt': {'type': 'string', 'description': 'Text prompt for the image'}}
    output_type = "string"

    def __init__(self, *args, **kwargs):
        try:
            # Use CPU-only in free-tier Spaces
            device = "cpu"
            model_id = "runwayml/stable-diffusion-v1-5"

            # Load pipeline with float32 for CPU compatibility
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                low_cpu_mem_usage=True  # Optimize for low memory
            ).to(device)

            # Enable memory-efficient attention
            if hasattr(self.pipe, 'enable_attention_slicing'):
                self.pipe.enable_attention_slicing()

            # Enable sequential CPU offloading if available (no dependency on accelerate)
            if hasattr(self.pipe, 'enable_sequential_cpu_offloading'):
                print("Enabling sequential CPU offloading for memory efficiency")
                self.pipe.enable_sequential_cpu_offloading()
            else:
                print("Sequential CPU offloading not supported, proceeding with standard CPU inference")

            self.is_initialized = True
            print(f"Image generator initialized on {device}")

        except Exception as e:
            print(f"Error initializing image generator: {e}")
            self.pipe = None
            self.is_initialized = False

    def forward(self, prompt: str) -> str:
        if not self.is_initialized or self.pipe is None:
            return "Error: Image generator not properly initialized"

        try:
            # Generate image with lower resolution for CPU efficiency
            image = self.pipe(
                prompt,
                num_inference_steps=20,
                height=256,  # Reduced for CPU
                width=256,   # Reduced for CPU
                guidance_scale=7.5
            ).images[0]

            # Create output directory
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)

            # Save image
            filename = f"generated_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(output_dir, filename)
            image.save(filepath)

            return filepath

        except Exception as e:
            return f"Error generating image: {str(e)}"