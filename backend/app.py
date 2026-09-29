import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from story_generator import generate_story, build_image_url
except ImportError:
    from backend.story_generator import generate_story, build_image_url

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)

# Allow cross-origin requests from any frontend (local or deployed)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.route("/")
def index():
    """Serve the frontend directly if present, or return API status."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return send_from_directory(str(FRONTEND_DIR), "index.html")
    return jsonify({
        "project": "AI Story & Comic Generator",
        "status": "Backend is running successfully!"
    })


@app.route("/api/health")
def health():
    """API health check endpoint."""
    return jsonify({
        "status": "online",
        "project": "AI Story & Comic Generator",
        "engine": "Gemini 3.5 & AI Image Studio",
        "supported_styles": [
            "Comic Book",
            "Manga",
            "Graphic Novel",
            "Cyberpunk",
            "3D Animation",
            "Retro 80s Comic"
        ]
    })


@app.route("/generate-story", methods=["POST"])
def create_story():
    """Generate complete story, characters, comic scenes, and panel images."""
    data = request.get_json(silent=True) or {}

    story_idea = data.get("story_idea", "").strip()
    genre = data.get("genre", "Adventure").strip()
    art_style = data.get("art_style", "Comic Book").strip()

    try:
        num_scenes = int(data.get("num_scenes", 5))
        num_scenes = max(1, min(10, num_scenes))
    except (ValueError, TypeError):
        num_scenes = 5

    characters = data.get("characters", [])
    if isinstance(characters, str):
        characters = [c.strip() for c in characters.split(",") if c.strip()]

    if not story_idea:
        return jsonify({
            "error": "Please provide a story idea."
        }), 400

    try:
        result = generate_story(
            story_idea=story_idea,
            genre=genre,
            num_scenes=num_scenes,
            characters=characters,
            art_style=art_style
        )
        return jsonify(result), 200

    except Exception as e:
        print(f"[Error /generate-story]: {e}")
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/redraw-panel", methods=["POST"])
def redraw_panel():
    """Regenerate a single comic panel image with a new random seed."""
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    art_style = data.get("art_style", "Comic Book").strip()

    if not prompt:
        return jsonify({"error": "Prompt is required to redraw panel."}), 400

    new_url = build_image_url(prompt, art_style)
    return jsonify({"image_url": new_url}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)