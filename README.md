<div align="center">

# Kling 4 API & Kling 4.0 Flash API

### Python SDK and practical video-generation examples for MuAPI

<p align="center"><a href="https://youtu.be/8Ua5lRiePFg"><img src="https://i.ytimg.com/vi/8Ua5lRiePFg/maxresdefault.jpg" width="720"></a></p>
<p align="center"><a href="https://youtu.be/8Ua5lRiePFg"><b>▶ Watch: How to Access Kling 4.0 API - Best Alternative to Seedance 2 </b></a></p>

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square)](https://muapi.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Text-to-video](https://img.shields.io/badge/workflow-text--to--video-8250df)](#text-to-video)
[![Image-to-video](https://img.shields.io/badge/workflow-image--to--video-1f883d)](#image-to-video)

[Quick start](#quick-start) · [Python SDK](#python-sdk) · [Prompt guide](#prompt-recipes) · [API routes](#supported-routes) · [FAQ](#faq)

</div>

Use a small Python client to submit text-to-video or image-to-video jobs through MuAPI's Kling 4 API, then poll for the result. This repository includes setup instructions, Python and cURL examples, and original prompt recipes for product shots, social clips, and cinematic scenes. It covers the **Kling 4 API** and tracks availability for the **Kling 4.0 API**, **Kling 4 Flash API**, and **Kling 4.0 Flash API** search intents. See the status below before integrating: Flash access in the Kling app does not by itself mean a public API endpoint is available.

> **Availability:** Kling 4 API access is live on MuAPI today. MuAPI serves native Kling 4.0 reference-to-video and keyframe-to-video endpoints, and the other Kling 4 requests run through its existing, production Kling video pipeline while Kuaishou completes its own staged Kling 4.0 rollout (see [Kling 4.0 announcement status](#kling-40-announcement-status) below), and will transparently move these same routes onto Kuaishou's native Kling 4.0 models as direct access opens up. Check the live [MuAPI Kling 4 page](https://muapi.ai/kling-4) and [API reference](https://muapi.ai/docs/api-reference) for current parameters and response formats.

## Contents

- [What is included](#what-is-included)
- [Kling 4.0 announcement status](#kling-40-announcement-status)
- [Kling 4.0 Flash API status](#kling-40-flash-api-status)
- [Quick start](#quick-start)
- [Text-to-video](#text-to-video)
- [Image-to-video](#image-to-video)
- [Kling 4.0 reference-to-video](#kling-40-reference-to-video)
- [Kling 4.0 keyframe-to-video](#kling-40-keyframe-to-video)
- [Prompt recipes](#prompt-recipes)
- [cURL workflow](#curl-workflow)
- [Supported routes](#supported-routes)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Related projects](#related-projects)
- [License](#license)

## Kling 4.0 announcement status

Kuaishou announced Kling 4.0 on September 28, 2026. Per that announcement, claimed capabilities include:

- Single-pass clips up to 30 seconds, double Kling 3.0's 15-second Director Mode cap
- A much higher reference ceiling — up to 50 text/image/video reference files, versus roughly a dozen previously
- Up to 10 keyframes for guiding continuity across connected shots
- Directed camera moves (push-in, orbit, tracking shots)
- Native audio rendered together with the picture instead of added afterward

A lite version is rolling out first to Kling's own annual subscribers, with a full release targeted for October 2026. These are Kuaishou's own claims from that announcement. MuAPI's Kling 4 API is available now and currently runs on MuAPI's existing Kling video pipeline (the routes documented below); MuAPI will move these endpoints onto Kuaishou's native Kling 4.0 models and publish updated limits and pricing as direct access opens up beyond Kuaishou's own lite/annual-subscriber rollout.

## Kling 4.0 Flash API status

As of September 29, 2026, this repository does not document a callable Kling 4.0 Flash API endpoint, and MuAPI's live Kling routes listed below do not identify themselves as Flash routes. Kling 4.0 Flash availability in the Kling app or for selected subscribers should not be treated as confirmation of public API access. Do not use the standard or Pro routes in this SDK expecting Flash-specific model behavior.

For current API availability, model identifiers, parameters, and pricing, check the [MuAPI Kling 4 page](https://muapi.ai/kling-4) and the [live API reference](https://muapi.ai/docs/api-reference). This status section will need updating when a documented Flash endpoint becomes available.

The terms **Kling 4 API** and **Kling 4.0 API** are often used for the broader Kling 4 generation API, while **Kling 4 Flash API** and **Kling 4.0 Flash API** refer to Flash-specific access. This SDK documents the currently listed MuAPI Standard and Pro routes; it does not claim those routes invoke Flash.

## What is included

- A lightweight `KlingAPI` Python client for submitting jobs and polling results.
- Text-to-video and image-to-video examples in Python.
- Kling 4.0 reference-to-video (images, videos, elements, voices) and keyframe-to-video examples.
- A cURL example for submitting a generation request.
- A separate [prompt recipe guide](docs/prompt-recipes.md) with structured examples and iteration tips.
- Direct calls to the MuAPI API, with the API key sent in the `x-api-key` header.

## Quick start

### Requirements

- Python 3.9 or newer
- A MuAPI account and API key
- For image-to-video, an image URL that the generation service can access

### Install

```bash
git clone https://github.com/Anil-matcha/Kling-4.0-Flash-API.git
cd Kling-4.0-Flash-API
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your key to `.env`:

```dotenv
MUAPI_API_KEY=your_muapi_api_key
```

The client loads this value at startup. You can also pass `api_key` directly when constructing `KlingAPI`.

## Text-to-video

Describe the scene and the main movement in the prompt. Optional fields such as `duration` and `aspect_ratio` are passed through to the selected provider route; confirm accepted values in the live API documentation.

```python
from kling_api import KlingAPI

api = KlingAPI()
job = api.text_to_video(
    "A red fox crosses a snowy forest clearing at dawn. "
    "The camera tracks slowly from left to right and settles as the fox looks back.",
    tier="pro",
    aspect_ratio="16:9",
    duration=5,
)

result = api.wait_for_completion(job["request_id"])
print(result)
```

Choose `tier="standard"` or `tier="pro"`. The initial response contains a `request_id` used to check the result.

## Image-to-video

Use image-to-video when a supplied image should establish the opening composition, product, or subject. Tell the model what should move and what should remain stable.

```python
job = api.image_to_video(
    prompt=(
        "Preserve the flowers, vase shape, and window framing. Add a gentle breeze "
        "that moves the petals while the camera makes a slow push toward the vase."
    ),
    image_url="https://example.com/garden.jpg",
    tier="pro",
    aspect_ratio="16:9",
    duration=5,
)

result = api.wait_for_completion(job["request_id"])
print(result)
```

The image URL must be publicly accessible to the generation service. Private localhost URLs and files behind a login will not be fetchable by the provider.

## Kling 4.0 reference-to-video

`POST /kling-4.0-reference-to-video` generates 3-30 second clips (720p or 1080p, native audio) from your own materials: up to 10 reference images, 5 reference videos (2-30 s each, 30 s combined), 7 named elements and 3 voices, 15 materials in total. Mention them in the prompt as `@image_1`, `@video_1` (array order) or `@name`; every mention must match a material in the same request.

```python
from kling_api import KlingAPI

api = KlingAPI()
job = api.reference_to_video(
    "@Hero sits at the desk, picks up the doll from @image_1, and greets using @Narrator",
    image_urls=["https://example.com/doll.png"],
    elements=[{"name": "Hero", "image_urls": ["https://example.com/hero-front.jpg", "https://example.com/hero-side.jpg"]}],
    voices=[{"name": "Narrator", "audio_url": "https://example.com/narrator.mp3"}],
    duration=10, resolution="1080p",
)
print(api.wait_for_completion(job["request_id"]))
```

An element takes either 2-4 `image_urls` or one 3-8 s `video_url` (character video). Set `keep_original_sound` to keep a reference video's audio. See [examples/reference_to_video.py](examples/reference_to_video.py).

## Kling 4.0 keyframe-to-video

`POST /kling-4.0-keyframe-to-video` takes a `first_frame_url`, optional `keyframe_urls` (up to 8, in order) and an optional `last_frame_url`; mention them as `@first_frame`, `@keyframe_1`, `@last_frame`. The frame total is capped by `duration` (3 s: 4 frames, 5 s: 6, 8 s: 9, 9 s or longer: 10) and the output follows the first frame's aspect ratio. See [examples/keyframe_to_video.py](examples/keyframe_to_video.py).

### Pricing

$0.157/s at 720p and $0.235/s at 1080p. With reference videos or video elements: $0.094/s (720p) / $0.141/s (1080p), billed on reference plus output seconds (minimum 2x the output length). Confirm on [muapi.ai/kling-4](https://muapi.ai/kling-4).

## Prompt recipes

A useful prompt is a compact directing note. Include the subject, setting, one primary action, a camera move, and the details that must stay consistent. For image-to-video, assign the input image a clear role and avoid requesting changes to details it should preserve.

### Product reveal

```text
Create a 7-second product shot of one amber glass bottle on a stone counter.
Keep its label, cap, and proportions unchanged. Morning light falls from the left.
The camera makes a slow quarter-circle move as condensation runs down the glass.
Finish with the bottle facing camera and the label in focus. No extra products or text.
```

### Vertical social clip

```text
Create an 8-second vertical home-gardening clip. A person in a plain green apron
turns one basil pot toward the window and points to a new leaf. Use a steady,
handheld phone-camera feel and natural daylight. Keep the same hands, apron, pot,
and plant. End with a clear close view of the leaf; no captions or brand marks.
```

### Cinematic beat

```text
At a quiet station at night, one traveler in a rust-colored coat waits beside an
empty track. Begin wide, with wet platform tiles reflecting cool blue light. A
distant train light appears; the traveler turns toward it. Track slowly from
behind and settle over the traveler's shoulder. Keep the same person and coat;
avoid other people and abrupt cuts.
```

These examples are original to this repository. The prompt categories and production-planning approach were informed by [flaqai/awesome-kling-4-0](https://github.com/flaqai/awesome-kling-4-0); its prompt text and media are not reproduced here.

Explore more examples in the [Kling video prompt recipe guide](docs/prompt-recipes.md), including image-to-video usage and an iteration checklist.

## cURL workflow

The repository includes a ready-to-run request example:

```bash
export MUAPI_API_KEY="your_muapi_api_key"
bash examples/curl.sh
```

The submission response includes a `request_id`. Poll it with:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  --header "x-api-key: ${MUAPI_API_KEY}"
```

## Supported routes

| Workflow | MuAPI endpoint |
| --- | --- |
| Kling 4 Pro text-to-video | `POST /kling-v3.0-pro-text-to-video` |
| Kling 4 Pro image-to-video | `POST /kling-v3.0-pro-image-to-video` |
| Kling 4 Standard text-to-video | `POST /kling-v3.0-standard-text-to-video` |
| Kling 4 Standard image-to-video | `POST /kling-v3.0-standard-image-to-video` |
| Kling 4.0 reference-to-video | `POST /kling-4.0-reference-to-video` |
| Kling 4.0 keyframe-to-video | `POST /kling-4.0-keyframe-to-video` |
| Check a generation result | `GET /predictions/{request_id}/result` |

Base URL: `https://api.muapi.ai/api/v1`. These are MuAPI's live Kling 4 routes today, served through MuAPI's existing Kling video pipeline (the route names still reference the underlying `v3.0` model versioning — see [Kling 4.0 announcement status](#kling-40-announcement-status)). The client route names and forwarded options are visible in [`kling_api.py`](kling_api.py). Routes and accepted fields may change as MuAPI moves onto Kuaishou's native Kling 4.0 models; consult the [MuAPI API reference](https://muapi.ai/docs/api-reference) before production use.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Set MUAPI_API_KEY` error | Add `MUAPI_API_KEY` to `.env`, or pass `api_key` to `KlingAPI(...)`. |
| HTTP 401 or 403 | Confirm the key is active and has access to the selected route. |
| HTTP 400 | Review required fields, parameter names, duration, and aspect-ratio values for the selected route. |
| Image request fails | Confirm the image URL is public, loads without cookies, and points directly to an image. |
| Polling times out | Check the provider task status and request ID; increase `timeout` if the job is still processing. |
| Route not found | Compare the endpoint in `kling_api.py` with the current MuAPI API reference. |

## FAQ

### Is Kling 4 available on MuAPI?

Yes. Kling 4 API access is live on MuAPI today, served through MuAPI's existing Kling video pipeline (see [Kling 4.0 announcement status](#kling-40-announcement-status)). MuAPI will move these same endpoints onto Kuaishou's native Kling 4.0 models as direct access opens up beyond Kuaishou's own staged rollout.

### Is there a Kling 4.0 Flash API endpoint?

This repository does not currently provide a verified Kling 4.0 Flash API endpoint. The available MuAPI routes are the standard and Pro workflows in [Supported routes](#supported-routes); confirm the live API reference for any newer Flash model ID or route before building an integration.

### Does the Kling 4 API support Kling 4 Flash?

The current Kling 4 API routes in this repository do not identify a Flash model. That applies to searches for both “Kling 4 Flash API” and “Kling 4.0 Flash API”: check MuAPI's live API reference for an explicitly documented Flash route before sending production requests.

### What does `tier` accept?

The Python wrapper accepts `standard` or `pro` and maps those values to the corresponding text-to-video or image-to-video route.

### Which optional parameters can I pass?

The client forwards additional keyword arguments to MuAPI. Accepted fields depend on the chosen route, so use the live API reference rather than assuming every parameter works for every model.

### Where can I find more prompt ideas?

Start with the [prompt recipe guide](docs/prompt-recipes.md). For a larger community collection, see [flaqai/awesome-kling-4-0](https://github.com/flaqai/awesome-kling-4-0); this SDK repository contains independently written examples rather than copied recipes.

### Can I use generated videos commercially?

The SDK license covers this repository's code. Rights and usage terms for generated outputs, input images, people, brands, and the generation service are separate; review the relevant provider terms before publishing or commercial use.

## Related projects

- [MuAPI](https://muapi.ai) — unified API for image, video, and audio generation.
- [MuAPI Kling page](https://muapi.ai/kling-4) — current product and model information.
- [MuAPI API reference](https://muapi.ai/docs/api-reference) — endpoint and parameter documentation.
- [Create a MuAPI access key](https://muapi.ai/access-keys).
- [Seedance 2 API](https://github.com/Anil-matcha/Seedance-2-API) — companion SDK for ByteDance video generation.
- [Awesome AI Video Models](https://github.com/Anil-matcha/awesome-ai-video-models) — browse video models and API options.
- [Awesome Kling 4.0 prompts](https://github.com/flaqai/awesome-kling-4-0) — community prompt collection used as inspiration for this repo's original recipe guide.

## License

This project is released under the [MIT License](LICENSE).
