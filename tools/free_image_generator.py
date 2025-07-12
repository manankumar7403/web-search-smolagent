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

    # In free_image_generator.py, modify the __init__ method
    # In free_image_generator.py, modify __init__
    def __init__(self, *args, **kwargs):
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model_id = "runwayml/stable-diffusion-v1-5"
            if device == "cuda":
                try:
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        model_id,
                        torch_dtype=torch.float16,
                        safety_checker=None,
                        requires_safety_checker=False
                    ).to(device)
                except Exception as e:
                    print(f"Float16 failed, falling back to float32: {e}")
                    self.pipe = StableDiffusionPipeline.from_pretrained(
                        model_id,
                        torch_dtype=torch.float32,
                        safety_checker=None,
                        requires_safety_checker=False
                    ).to(device)
            else:
                self.pipe = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False
                ).to(device)
            if hasattr(self.pipe, 'enable_attention_slicing'):
                self.pipe.enable_attention_slicing()
            try:
                from accelerate import Accelerator
                if hasattr(self.pipe, 'enable_model_cpu_offload'):
                    self.pipe.enable_model_cpu_offload()
            except ImportError:
                print("Accelerator not found, skipping CPU offloading")
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
            # Generate image with lower resolution for memory efficiency
            image = self.pipe(
                prompt,
                num_inference_steps=20,  # Reduced steps for speed
                height=512,
                width=512,
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