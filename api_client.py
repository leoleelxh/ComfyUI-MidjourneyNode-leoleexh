# File: midjourney_node/api_client.py
import requests
import time
import numpy as np
from PIL import Image
from io import BytesIO
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MidjourneyAPIClient:
    def __init__(self):
        self.base_url = "http://192.168.1.200:7080"

    def start_generation(self, params):
        if isinstance(params, str):
            params = {"prompt": params}
        logger.debug(f"Starting generation with params: {params}")
        response = requests.post(f"{self.base_url}/mj/submit/imagine", json=params)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"Generation start response: {result}")
        return result

    def upscale_or_vary(self, task_id, action):
        params = {"content": f"{task_id} {action}"}
        logger.debug(f"Upscaling or varying with params: {params}")
        response = requests.post(f"{self.base_url}/mj/submit/simple-change", json=params)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"Upscale/Vary response: {result}")
        return result

    def wait_for_generation(self, task_id):
        max_retries = 60  # 5 minutes maximum wait time
        for _ in range(max_retries):
            logger.debug(f"Fetching task status for task_id: {task_id}")
            response = requests.get(f"{self.base_url}/mj/task/{task_id}/fetch")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Fetch response: {data}")
            if data['status'] == 'SUCCESS':
                if 'imageUrl' in data:
                    try:
                        img = self.download_image(data['imageUrl'])
                        return img, task_id
                    except Exception as e:
                        logger.error(f"Error downloading image from URL {data['imageUrl']}: {str(e)}")
                        raise
                else:
                    raise Exception(
                        "No image URL found in the successful response")
            elif data['status'] == 'FAILED':
                raise Exception(f"Task failed: {data.get('failReason', 'Unknown error')}")
            elif data['status'] in ['SUBMITTED', 'IN_PROGRESS', 'NOT_START']:
                logger.info(f"Task status: {data['status']}, progress: {data.get('progress', 'Unknown')}")
                time.sleep(5)  # Wait for 5 seconds before checking again
            else:
                raise Exception(f"Unknown task status: {data['status']}")
        raise Exception("Task timeout: Maximum wait time exceeded")

    def download_image(self, url):
        logger.debug(f"Downloading image from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return np.array(img)
