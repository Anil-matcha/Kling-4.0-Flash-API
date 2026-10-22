"""Small Python client for Kling video models available through MuAPI."""

import os
import time
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class KlingAPI:
    """Submit Kling video jobs and poll their asynchronous results."""

    BASE_URL = "https://api.muapi.ai/api/v1"
    ROUTES = {
        "pro_t2v": "kling-v3.0-pro-text-to-video",
        "pro_i2v": "kling-v3.0-pro-image-to-video",
        "standard_t2v": "kling-v3.0-standard-text-to-video",
        "standard_i2v": "kling-v3.0-standard-image-to-video",
        "reference": "kling-4.0-reference-to-video",
        "keyframe": "kling-4.0-keyframe-to-video",
    }

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 timeout: float = 60.0):
        self.api_key = api_key or os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("Set MUAPI_API_KEY or pass api_key to KlingAPI().")
        self.base_url = (base_url or os.getenv("MUAPI_API_BASE_URL", self.BASE_URL)).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": self.api_key})

    def _submit(self, route: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/{route}", json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def text_to_video(self, prompt: str, *, tier: str = "pro", **parameters: Any) -> Dict[str, Any]:
        """Submit a Kling text-to-video job. Additional accepted fields pass through."""
        route = self.ROUTES.get(f"{tier}_t2v")
        if not route:
            raise ValueError("tier must be 'standard' or 'pro'")
        return self._submit(route, {"prompt": prompt, **parameters})

    def image_to_video(self, prompt: str, image_url: str, *, tier: str = "pro",
                       **parameters: Any) -> Dict[str, Any]:
        """Animate an image URL with a text prompt."""
        route = self.ROUTES.get(f"{tier}_i2v")
        if not route:
            raise ValueError("tier must be 'standard' or 'pro'")
        return self._submit(route, {"prompt": prompt, "image_url": image_url, **parameters})

    def reference_to_video(self, prompt: str, *, image_urls: Optional[list] = None,
                           video_urls: Optional[list] = None, elements: Optional[list] = None,
                           voices: Optional[list] = None, **parameters: Any) -> Dict[str, Any]:
        """Kling 4.0 reference-to-video. Mention materials in the prompt as @image_1,
        @video_1 (array order) or @name (elements and voices)."""
        payload: Dict[str, Any] = {"prompt": prompt, **parameters}
        for key, value in (("image_urls", image_urls), ("video_urls", video_urls),
                           ("elements", elements), ("voices", voices)):
            if value:
                payload[key] = value
        return self._submit(self.ROUTES["reference"], payload)

    def keyframe_to_video(self, prompt: str, first_frame_url: str, *,
                          keyframe_urls: Optional[list] = None,
                          last_frame_url: Optional[str] = None, **parameters: Any) -> Dict[str, Any]:
        """Kling 4.0 keyframe-to-video. Mention frames as @first_frame, @keyframe_1, @last_frame."""
        payload: Dict[str, Any] = {"prompt": prompt, "first_frame_url": first_frame_url, **parameters}
        if keyframe_urls:
            payload["keyframe_urls"] = keyframe_urls
        if last_frame_url:
            payload["last_frame_url"] = last_frame_url
        return self._submit(self.ROUTES["keyframe"], payload)

    def get_result(self, request_id: str) -> Dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/predictions/{request_id}/result", timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, request_id: str, *, poll_interval: float = 5,
                            timeout: float = 600) -> Dict[str, Any]:
        """Poll a submitted job until it completes, fails, or times out."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = self.get_result(request_id)
            status = result.get("status")
            if status == "completed":
                return result
            if status == "failed":
                raise RuntimeError(f"Kling generation failed: {result.get('error', result)}")
            time.sleep(poll_interval)
        raise TimeoutError(f"Timed out waiting for Kling job {request_id}")
