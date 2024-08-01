# File: midjourney_node/midjourney_generate_node.py
import torch
from .api_client import MidjourneyAPIClient


class MidjourneyGenerateNode:
    def __init__(self):
        self.api_client = MidjourneyAPIClient()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "cat,cute,"}),
                "base_model": (["midjourney", "niji"], {"default": "midjourney"}),
                "version": (["5.0", "5.1", "5.2", "6", "6.1"], {"default": "6"}),
            },
            "optional": {
                # "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "image_ratio": (["1:1", "4:3", "3:4", "16:9", "9:16"], {"default": "1:1"}),
                "stylize": ("INT", {"default": 100, "min": 0, "max": 1000, "step": 1}),
                # "quality": ([".25", ".5", "1"], {"default": "1"}),
                "chaos": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "weird": ("INT", {"default": 0, "min": 0, "max": 3000, "step": 1}),
                "tile": ("BOOLEAN", {"default": False}),
                "q2": ("BOOLEAN", {"default": False}),
                "sref": ("STRING", {"default": ""}),
                # "no": ("STRING", {"default": ""}),
                "repeat": ("INT", {"default": 1, "min": 1, "max": 40, "step": 1}),
                "seed": ("INT", {"default": -1}),
                # "control_after_generate": (["fixed", "increment", "decrement", "randomize"], {"default": "fixed"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "task_id")
    FUNCTION = "generate"
    CATEGORY = "image"

    def generate(self, prompt, base_model, version, image_ratio="1:1",
                 stylize=100, chaos=0, weird=0, tile=False, q2=False, sref="",
                 repeat=1, seed=-1):
        # Construct the complete prompt
        params = prompt
        # if negative_prompt:
        #     params += f" --no {negative_prompt}"
        params += f" --ar {image_ratio} --s {stylize} "
        if chaos > 0:
            params += f" --c {chaos}"
        if weird > 0:
            params += f" --weird {weird}"
        if tile:
            params += " --tile"
            
        if q2:
            params += " --q 2"
            
        if sref:
            params += f" --sref {sref}"

        if base_model != "niji":
            params += f" --v {version}"
        else:
            params += " --niji"

        if repeat > 1:
            params += f" --repeat {repeat}"
        if seed != -1:
            params += f" --seed {seed}"

        # Call the API client to start the generation process
        response = self.api_client.start_generation(params)

        # Wait for the generation to complete and get the preview image
        image, task_id = self.api_client.wait_for_generation(
            response['result'])

        # Convert the image to a tensor that ComfyUI can use
        img_tensor = torch.from_numpy(image).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension

        return (img_tensor, task_id)
