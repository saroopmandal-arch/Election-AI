# ElectionIQ Project Map

This document provides a comprehensive overview of the ElectionIQ codebase to assist future agents in understanding and maintaining the project.

## Architecture Overview
- **Backend**: FastAPI (Python 3.11+) serving a single-page HTML application and an AI chat endpoint.
- **Frontend**: Single-page application (SPA) built with Tailwind CSS (CDN) and Vanilla JavaScript.
- **AI Integration**: Google Gemini API (`gemini-2.5-flash`) for handling election-related queries.
- **Asset Generation**: `gen.py` is the source of truth for `index.html`. Do NOT edit `index.html` directly; update `gen.py` and run it.

## Key Files
- [main.py](file:///c:/Users/saroo/Downloads/Election%20IQ/main.py): FastAPI application. Handles routing, static file serving, and the `/chat` endpoint.
- [gen.py](file:///c:/Users/saroo/Downloads/Election%20IQ/gen.py): UI Generator script. Contains the HTML/JS/CSS templates and logic.
- [index.html](file:///c:/Users/saroo/Downloads/Election%20IQ/index.html): Generated frontend (Derived from `gen.py`).
- [.env](file:///c:/Users/saroo/Downloads/Election%20IQ/.env): Environment variables (Requires `GEMINI_API_KEY`).
- [requirements.txt](file:///c:/Users/saroo/Downloads/Election%20IQ/requirements.txt): Python dependencies.
- [Dockerfile](file:///c:/Users/saroo/Downloads/Election%20IQ/Dockerfile): Cloud Run-ready container definition.
- [.dockerignore](file:///c:/Users/saroo/Downloads/Election%20IQ/.dockerignore): Excludes dev-only files from Docker image.
- [start_electioniq.bat](file:///c:/Users/saroo/Downloads/Election%20IQ/start_electioniq.bat): Windows one-click launcher.

## Routing & Navigation
- `/`: Serves `index.html`.
- `/chat`: POST endpoint for AI chat.
- `/health`: GET endpoint for health checks (used by Cloud Run).
- `/static`: Serves static assets (if any).
- **Frontend Navigation**: Handled by `nav(pageID)` in JS, which toggles `.page.active` classes with smooth fade transitions.

## Features Implementation
- **Chat**: Real-time AI chat with conversation history, responsive bubbles, and markdown rendering for AI responses.
- **Timeline**: 6-phase election schedule with vertical timeline layout and scroll-reveal animations.
- **How to Vote**: 5-step guide with premium centered Step 3 layout and hover effects.
- **FAQ**: Reliable data-attribute based accordion system with slide-in animations.
- **Mobile**: Hamburger menu with slide-down animation for viewports < 768px.
- **Animations**: Smooth page fade transitions, scroll-reveal on timeline/guide, fadeSlideUp on chat messages and FAQ answers.

## UI Polish Applied
- [x] Page transitions with CSS opacity fade (.35s ease).
- [x] Mobile hamburger menu with animated slide-down overlay.
- [x] Scroll-reveal animations on timeline phases and guide steps.
- [x] Markdown rendering in AI chat (bold, italic, lists).
- [x] Dynamic copyright year in footer.
- [x] Refined focus-visible outlines on inputs.
- [x] fadeSlideUp keyframe animation for chat messages and FAQ answers.
- [x] Reduced layout gaps (footer top margin).
- [x] Added Liquid Glassmorphism visuals and ambient animations to Timeline/Guide.
- [x] Added interactive dynamic mouse-glow effect (nano banana theme).
- [x] Added dynamic multi-language support (12 Indian languages) via custom UI + AI backend.

## Deployment
- **Local**: `uvicorn main:app --reload --port 8080` or `start_electioniq.bat`.
- **Docker**: `docker build -t electioniq . && docker run -p 8080:8080 -e GEMINI_API_KEY=xxx electioniq`.
- **Cloud Run**: `gcloud run deploy electioniq --source . --platform managed --region asia-south1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=xxx`.

## Status: COMPLETE ✅
- [x] Backend routing fixed (shadowing issue resolved).
- [x] FAQ logic robust (switched to `data-q` targeting).
- [x] UI synchronized with premium design specs.
- [x] Generator script (`gen.py`) updated as source of truth.
- [x] UI polish pass applied (transitions, mobile menu, scroll-reveal, markdown chat).
- [x] Dockerfile optimized for Cloud Run ($PORT support, .dockerignore).
- [x] README has full Cloud Run deployment guide.

## Maintenance Notes
- **To update the UI**: Modify the string constants or logic in `gen.py`, then run `python gen.py`. Note: The latest UI polish was applied directly to `index.html` — sync `gen.py` if needed.
- **To update AI logic**: Modify the prompt or model configuration in `main.py`.
