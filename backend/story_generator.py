import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

client = genai.Client()
def generate_story(story_idea, genre, num_scenes, characters):

    prompt = f"""
You are a creative story writer.

Create an original {genre} story based on this idea:

{story_idea}

Characters:
{characters}

Generate exactly {num_scenes} scenes.

Return ONLY valid JSON.
Do not use markdown.
Do not put ``` around the JSON.

Use exactly this structure:

{{
    "title": "Story title",
    "genre": "{genre}",
    "characters": [
        {{
            "name": "Character name",
            "description": "Character description"
        }}
    ],
    "story": "Complete story",
    "scenes": [
        {{
            "scene_number": 1,
            "description": "What happens in the scene",
            "dialogue": "Important dialogue"
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Remove accidental markdown code fences
    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    return json.loads(result)