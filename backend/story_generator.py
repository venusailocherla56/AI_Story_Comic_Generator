import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

client = genai.Client()


# --------------------------------------------------
# Generate Story
# --------------------------------------------------

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

    # --------------------------------------------------
    # Models to try
    # --------------------------------------------------

    models = [
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite"
    ]

    last_error = None

    # --------------------------------------------------
    # Try models with automatic retry
    # --------------------------------------------------

    for model in models:

        for attempt in range(3):

            try:

                print(
                    f"Trying model: {model} | "
                    f"Attempt: {attempt + 1}/3"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                result = response.text.strip()

                # --------------------------------------
                # Remove accidental markdown fences
                # --------------------------------------

                if result.startswith("```json"):
                    result = result[7:]

                if result.startswith("```"):
                    result = result[3:]

                if result.endswith("```"):
                    result = result[:-3]

                result = result.strip()

                # --------------------------------------
                # Convert JSON text into Python object
                # --------------------------------------

                data = json.loads(result)

                print(f"Story generated successfully using {model}")

                return data

            # ------------------------------------------
            # Temporary Gemini server / rate errors
            # ------------------------------------------

            except errors.ServerError as e:

                last_error = e

                print(
                    f"Gemini server error with {model}: {e}"
                )

                # Wait before retrying
                wait_time = 2 ** attempt

                print(
                    f"Waiting {wait_time} seconds before retry..."
                )

                time.sleep(wait_time)

            # ------------------------------------------
            # Quota / rate-limit errors
            # ------------------------------------------

            except errors.ClientError as e:

                last_error = e

                print(
                    f"Gemini client error with {model}: {e}"
                )

                # Try the fallback model
                break

            # ------------------------------------------
            # Invalid JSON returned by Gemini
            # ------------------------------------------

            except json.JSONDecodeError as e:

                last_error = e

                print(
                    f"Invalid JSON returned by {model}: {e}"
                )

                # Retry the same model
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

                break

            # ------------------------------------------
            # Other unexpected errors
            # ------------------------------------------

            except Exception as e:

                last_error = e

                print(
                    f"Unexpected error with {model}: {e}"
                )

                break

    # --------------------------------------------------
    # All models failed
    # --------------------------------------------------

    raise Exception(
        "Gemini could not generate the story after "
        "trying the available models. "
        f"Last error: {last_error}"
    )