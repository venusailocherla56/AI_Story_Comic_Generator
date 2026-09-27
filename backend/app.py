from flask import Flask, jsonify, request
from flask_cors import CORS
from story_generator import generate_story

app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app, resources={
    r"/generate-story": {
        "origins": ["https://aistoryandcomicgenerator.netlify.app"]
    }
})


@app.route("/")
def home():
    return jsonify({
        "project": "AI Story & Comic Generator",
        "status": "Backend is running successfully!"
    })


@app.route("/generate-story", methods=["POST"])
def create_story():

    data = request.get_json()

    story_idea = data.get("story_idea", "")
    genre = data.get("genre", "Adventure")
    num_scenes = int(data.get("num_scenes", 5))
    characters = data.get("characters", [])

    if not story_idea:
        return jsonify({
            "error": "Please provide a story idea."
        }), 400

    result = generate_story(
        story_idea,
        genre,
        num_scenes,
        characters
    )

    return jsonify(result)


if __name__ == "__main__":
     import os
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )