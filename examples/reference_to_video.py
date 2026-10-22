from kling_api import KlingAPI

api = KlingAPI()
job = api.reference_to_video(
    "@Hero sits at the desk, picks up the doll from @image_1, and greets using @Narrator",
    image_urls=["https://example.com/doll.png"],
    elements=[{
        "name": "Hero",
        "image_urls": ["https://example.com/hero-front.jpg", "https://example.com/hero-side.jpg"],
        "tag": "character",
    }],
    voices=[{"name": "Narrator", "audio_url": "https://example.com/narrator.mp3"}],
    duration=10,
    resolution="1080p",
)
print("Submitted:", job)
result = api.wait_for_completion(job["request_id"])
print("Video:", result.get("outputs") or result.get("url"))
