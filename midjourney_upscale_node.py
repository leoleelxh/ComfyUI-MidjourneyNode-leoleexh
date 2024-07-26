# File: midjourney_node/midjourney_upscale_node.py
import torch
from .api_client import MidjourneyAPIClient


class MidjourneyUpscaleNode:
    def __init__(self):
        self.api_client = MidjourneyAPIClient()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "task_id": ("STRING", {"multiline": False}),
                "action": (["U1", "U2", "U3", "U4", "V1", "V2", "V3", "V4"], {"default": "U1"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale_or_vary"
    CATEGORY = "image"

    def upscale_or_vary(self, image, task_id, action):
        # Start the upscale or variation process
        response = self.api_client.upscale_or_vary(task_id, action)

        # Wait for the process to complete and get the resulting image
        result_image, _ = self.api_client.wait_for_generation(
            response['result'])

        # Convert the image to a tensor that ComfyUI can use
        img_tensor = torch.from_numpy(result_image).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension

        return (img_tensor,)
