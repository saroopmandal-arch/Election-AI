import asyncio
import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="ElectionIQ API", version="1.0.0")

# CORS — allow all origins for Cloud Run + local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "30"))

# Priority chain for fallback when tokens/rate-limits run out
MODEL_CHAIN = [
    GEMINI_MODEL,  # User preferred (e.g. gemini-2.5-flash-lite)
    "gemini-2.0-flash-lite",
    "gemini-flash-lite-latest",
]

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are ElectionIQ, a concise and authoritative AI assistant "
    "that helps Indian citizens understand the election process. "
    "You explain ECI procedures, voter registration, EVM usage, "
    "polling day process, and result declaration clearly and simply. "
    "Keep answers under 4 sentences. Never discuss politics, "
    "parties, or candidates. Only explain the electoral process."
)


class Message(BaseModel):
    role: str  # "user" or "model"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    user_message: str
    language: str = "English"


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
async def health():
    return {"status": "ok"}


def send_to_gemini(request: ChatRequest) -> str:
    localized_prompt = SYSTEM_PROMPT + f" IMPORTANT: You must respond entirely in the following language: {request.language}."
    
    last_error = None
    for model_name in MODEL_CHAIN:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=localized_prompt,
            )

            history = []
            for msg in request.messages:
                history.append({
                    "role": msg.role,
                    "parts": [msg.content]
                })

            chat_session = model.start_chat(history=history)
            response = chat_session.send_message(request.user_message)
            return response.text
        except Exception as e:
            # Catch rate limit / token exhausted errors specifically if possible
            # Or fallback for any transient generation error
            error_msg = str(e).lower()
            if "429" in error_msg or "resource_exhausted" in error_msg or "quota" in error_msg:
                print(f"Model {model_name} exhausted. Falling back...")
                last_error = e
                continue
            raise e
    
    if last_error:
        raise last_error
    raise Exception("All models in fallback chain failed.")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY environment variable not set."
        )

    try:
        reply = await asyncio.wait_for(
            asyncio.to_thread(send_to_gemini, request),
            timeout=GEMINI_TIMEOUT_SECONDS,
        )

        return ChatResponse(response=reply)

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Gemini request timed out. Please try again."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_frontend():
    if not INDEX_FILE.is_file():
        raise HTTPException(status_code=404, detail="index.html not found. Please run build scripts.")
    return FileResponse(INDEX_FILE)
