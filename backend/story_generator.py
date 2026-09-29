import os
import json
import time
import random
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)

# Initialize Gemini Client
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else genai.Client()

# --------------------------------------------------
# Supported Art Styles & Prompt Modifiers
# --------------------------------------------------

ART_STYLE_MODIFIERS = {
    "Comic Book": "classic western comic book art, bold ink outlines, vibrant colors, comic panel, dramatic action, halftone dots, high detail",
    "Manga": "Japanese manga anime style, dramatic speed lines, expressive anime characters, clean line art, comic page, high contrast",
    "Graphic Novel": "dark graphic novel illustration, moody cinematic lighting, painterly watercolor and ink, atmospheric textures",
    "Cyberpunk": "cyberpunk comic art, neon glow, high tech holographic lighting, dark rainy city, dynamic cinematic angle, detailed ink",
    "3D Animation": "3D Pixar DreamWorks style animated movie scene, expressive characters, vibrant cinematic lighting, octane render 8k",
    "Retro 80s Comic": "vintage 1980s retro comic book print, weathered newsprint texture, retro color palette, classic superhero comics"
}


def build_image_url(prompt: str, art_style: str = "Comic Book", seed: int = None) -> str:
    """Build a fast, free, reliable image URL for comic panels with art style modifiers."""
    if seed is None:
        seed = random.randint(1000, 999999)

    style_mod = ART_STYLE_MODIFIERS.get(art_style, ART_STYLE_MODIFIERS["Comic Book"])
    enhanced_prompt = f"{prompt}, {style_mod}, masterpiece, comic strip panel, no watermarks, cinematic composition"
    encoded_prompt = urllib.parse.quote(enhanced_prompt)

    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=500&seed={seed}&nologo=true"


# --------------------------------------------------
# Generate Story & Comic Scene Breakdown
# --------------------------------------------------

def generate_story(story_idea: str, genre: str = "Adventure", num_scenes: int = 5, characters = None, art_style: str = "Comic Book"):
    if characters is None:
        characters = []

    char_str = ", ".join(characters) if isinstance(characters, list) else str(characters)
    style_keywords = ART_STYLE_MODIFIERS.get(art_style, ART_STYLE_MODIFIERS["Comic Book"])

    prompt = f"""
You are an award-winning comic book writer and visual storyboard artist.

Create an engaging, original {genre} comic story based on this premise:
"{story_idea}"

Characters specified:
{char_str if char_str else "Create 1-2 compelling characters suited for this story"}

Art Style Target: {art_style} ({style_keywords})

Generate exactly {num_scenes} sequential comic scenes/panels.
Ensure characters have distinct, consistent visual traits so an illustrator can keep their appearance uniform across all panels.

Return ONLY a JSON object with this exact structure:
{{
    "title": "A catchy comic book title",
    "genre": "{genre}",
    "art_style": "{art_style}",
    "logline": "A punchy one-sentence summary of the story",
    "story": "The complete narrative story arc written in exciting prose",
    "characters": [
        {{
            "name": "Character Name",
            "role": "e.g. Protagonist / Rival / Sidekick",
            "visual_description": "Detailed visual appearance: hair style/color, facial features, distinctive outfit/costume, accessories"
        }}
    ],
    "scenes": [
        {{
            "scene_number": 1,
            "panel_title": "Short title for this panel",
            "narrator_caption": "Narrator text box (e.g., 'Meanwhile in Sector 7...', 'The silence was deafening...')",
            "description": "Clear visual description of what happens in the scene",
            "speaker": "Name of character speaking or 'Narrator'",
            "dialogue": "Short, punchy comic dialogue for speech bubble",
            "sound_effect": "Comic SFX (e.g. BAM!, WHOOSH!, KRAK-THOOM!, TIK-TOK) or empty string if quiet",
            "image_prompt": "Highly detailed visual description for comic illustrator including camera angle (close-up, wide shot, Dutch angle), character poses, expressions, environment lighting, and action"
        }}
    ]
}}
"""

    # Optimized model fallback sequence: fast/available models first
    models = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash"
    ]

    last_error = None
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.75
    )

    for model in models:
        for attempt in range(3):
            try:
                print(f"[Gemini] Trying model: {model} | Attempt {attempt + 1}/3...")
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )

                raw_text = response.text.strip()
                data = json.loads(raw_text)

                # Ensure image URLs are pre-populated for each scene
                base_seed = random.randint(10000, 900000)
                scenes = data.get("scenes", [])
                for idx, scene in enumerate(scenes):
                    img_prompt = scene.get("image_prompt") or scene.get("description", "Comic panel")
                    # Append character visual cues if available
                    char_cues = " ".join([c.get("visual_description", "") for c in data.get("characters", [])])
                    full_prompt = f"{img_prompt}. Characters: {char_cues}"
                    scene["image_url"] = build_image_url(full_prompt, art_style, seed=base_seed + idx * 7)

                data["art_style"] = art_style
                print(f"[Gemini] Story and comic scenes generated successfully with {model}!")
                return data

            except errors.ServerError as e:
                last_error = e
                wait_time = 2 ** attempt
                print(f"[Gemini] Server error on {model}: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

            except errors.ClientError as e:
                last_error = e
                print(f"[Gemini] Client error on {model}: {e}. Trying fallback model...")
                break

            except json.JSONDecodeError as e:
                last_error = e
                print(f"[Gemini] JSON parsing error from {model}: {e}.")
                if attempt < 2:
                    time.sleep(1)
                    continue
                break

            except Exception as e:
                last_error = e
                print(f"[Gemini] Unexpected error on {model}: {e}")
                break

    raise Exception(f"Gemini generation failed after trying all models. Last error: {last_error}")