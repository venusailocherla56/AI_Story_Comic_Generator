
import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def generate_story(story_idea, genre, num_scenes, characters):

    prompt = f"""
You are a professional creative story writer.

Write one original, complete {genre} story based on this idea:
{story_idea}

Characters provided by the user:
{characters}

Create exactly {num_scenes} scenes.

Requirements:
- Write a short, engaging story.
- Keep the story around 250-350 words.
- Make the story original and logically consistent.
- Do not repeat paragraphs or sentences.
- Do not include explanations, introductions, or suggestions.
- Return only the requested JSON.
- Make each scene part of the same story.

Return valid JSON in this structure:

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

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()["response"]

    return json.loads(result)