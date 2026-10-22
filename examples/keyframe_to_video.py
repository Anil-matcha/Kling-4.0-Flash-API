from kling_api import KlingAPI

api = KlingAPI()
job = api.keyframe_to_video(
    "The girl in @first_frame walks out, passes the street in @keyframe_1, and arrives at the party in @last_frame",
    "https://example.com/first.png",
    keyframe_urls=["https://example.com/street.png"],
    last_frame_url="https://example.com/party.png",
    duration=10,
    resolution="720p",
)
print("Submitted:", job)
result = api.wait_for_completion(job["request_id"])
print("Video:", result.get("outputs") or result.get("url"))
