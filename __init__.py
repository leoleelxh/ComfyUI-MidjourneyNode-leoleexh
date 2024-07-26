# File: midjourney_node/__init__.py
from .midjourney_generate_node import MidjourneyGenerateNode
from .midjourney_upscale_node import MidjourneyUpscaleNode

NODE_CLASS_MAPPINGS = {
    "MidjourneyGenerateNode": MidjourneyGenerateNode,
    "MidjourneyUpscaleNode": MidjourneyUpscaleNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MidjourneyGenerateNode": "Midjourney Initial Generation",
    "MidjourneyUpscaleNode": "Midjourney Upscale/Variation"
}
