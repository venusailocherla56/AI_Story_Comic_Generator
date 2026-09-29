# 💥 AI Story & Comic Generator Studio

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.x](https://img.shields.io/badge/Flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Powered%20By-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An end-to-end AI-powered creative writing and **visual comic book studio**. Turn simple story prompts into illustrated comic book strips with sequential panels, speech bubbles, narrator caption boxes, authentic sound effect stickers (`POW!`, `BAM!`), and character consistency.

---

## ✨ Features

- **💥 Illustrated Comic Book Strips**: Generates sequential visual comic panels with authentic comic borders, speech bubbles, speaker badges, and narrator boxes.
- **🎨 6 Selectable Comic Art Styles**:
  - 💥 **Classic Comic**: Bold black ink linework, halftone dots, vibrant action colors.
  - ⛩️ **Manga / Anime**: Dynamic speedlines, anime character aesthetic, high-contrast ink.
  - 🎨 **Graphic Novel**: Moody atmospheric lighting, dark watercolor, gritty textures.
  - 🕶️ **Cyberpunk Noir**: Neon-drenched rainy streets, high-tech glowing accents.
  - 🧸 **3D Pixar / Animation**: Expressive 3D characters, cinematic depth and lighting.
  - 📻 **Retro 80s Comic**: Weathered newsprint texture and vintage print aesthetics.
- **👥 Character Visual Consistency**: Generates visual trait profiles (costumes, hair, accessories) so characters stay uniform across all comic panels.
- **🎬 Interactive Reader Mode**: Fullscreen slide-by-slide comic reader with keyboard arrow navigation (`←` / `→`).
- **🔊 Text-to-Speech Narration**: In-browser voice narration for each individual panel and the complete story using the Web Speech API.
- **🔄 Dynamic Panel Redraw**: Regenerate or redraw any individual comic panel on the fly with a single click.
- **📚 Local Comic Library**: Automatically saves your generated comic books to browser `localStorage` for instant access anytime.
- **🖨️ Export & Print**: Print or export your comic page directly to high-resolution PDF with dedicated print styling.
- **⚡ Unified Zero-CORS Architecture**: Flask seamlessly serves both the REST API and the frontend web app on `http://localhost:5000`.

---

## 🏗️ Project Architecture

```text
AI_Story_Comic_Generator/
├── backend/
│   ├── app.py                 # Flask server, CORS, route handlers & static file serving
│   ├── story_generator.py     # Gemini client, structured JSON output & image prompt builder
│   └── requirements.txt       # Python dependencies
├── frontend/
│   └── index.html             # Responsive Dark-mode Web UI, Comic Grid & Reader Modal
├── assets/                    # Static assets & media
├── dataset/                   # Dataset directory
├── generated/                 # Generated exports directory
├── .env.example               # Template for environment variables
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher
- A free Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 2. Setup Environment
```bash
# Clone the repository
git clone https://github.com/venusailocherla56/AI_Story_Comic_Generator.git
cd AI_Story_Comic_Generator

# Create and activate a virtual environment
# On Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the root directory (or copy from `.env.example`):
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
```

### 4. Run the Application
```powershell
python backend/app.py
```
Open your browser and navigate to:
👉 **`http://localhost:5000`**

*(The Flask backend automatically serves the frontend interface with full API connectivity and zero CORS issues!)*

---

## 📡 REST API Reference

### 1. `GET /api/health`
Checks the server and AI model status.
- **Response**: `200 OK`
```json
{
  "status": "online",
  "project": "AI Story & Comic Generator",
  "engine": "Gemini 3.5 & AI Image Studio",
  "supported_styles": ["Comic Book", "Manga", "Graphic Novel", "Cyberpunk", "3D Animation", "Retro 80s Comic"]
}
```

### 2. `POST /generate-story`
Generates a complete story, character profiles, comic scene scripts, and panel illustrations.
- **Request Body**:
```json
{
  "story_idea": "An apprentice timekeeper builds a watch that rewinds 30 seconds",
  "genre": "Sci-Fi",
  "num_scenes": 4,
  "characters": ["Leo", "Raven"],
  "art_style": "Comic Book"
}
```
- **Response**: `200 OK` containing `title`, `logline`, `story`, `characters`, and `scenes` array with `image_url`, `sound_effect`, `dialogue`, and `narrator_caption`.

### 3. `POST /redraw-panel`
Regenerates an image for an individual comic panel with a fresh visual variation.
- **Request Body**:
```json
{
  "prompt": "Detective Jax running through rainy neon alleyway",
  "art_style": "Cyberpunk"
}
```
- **Response**: `200 OK`
```json
{
  "image_url": "https://image.pollinations.ai/prompt/..."
}
```

---

## 🌐 Deployment

### Backend (Render)
1. Create a new **Web Service** on [Render](https://render.com/).
2. Connect your GitHub repository.
3. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
4. Add Environment Variable:
   - `GEMINI_API_KEY`: `your_key`

### Frontend (Netlify / Static Hosting)
- If hosting frontend separately on [Netlify](https://www.netlify.com/), deploy the `frontend/` directory.
- The frontend dynamically detects the API endpoint or falls back gracefully to your deployed backend URL.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
