# ElectionIQ 🗳️

An AI-powered election process assistant for Indian citizens, built with FastAPI + Google Gemini API.

---

## Features

- 🤖 AI chat powered by Gemini Flash — answers election process questions
- 📅 Visual election timeline (ECI, India)
- 📋 Step-by-step voting guide
- ❓ FAQ accordion with common voter questions
- ⚡ Single-page app, zero build steps

---

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd electioniq

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run the server
uvicorn main:app --reload --port 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

### Windows one-click start

Double-click `start_electioniq.bat`.

It creates a local `.venv` if needed, installs dependencies, starts the server, and opens the app. If ElectionIQ is already running on ports `8081` through `8090`, it reopens that existing server instead of starting a duplicate copy.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key (free tier works) |
| `GEMINI_MODEL` | Optional Gemini model override. Defaults to `gemini-2.5-flash`. |
| `GEMINI_TIMEOUT_SECONDS` | Optional chat timeout. Defaults to `30`. |

Get a free key at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Docker (Local)

```bash
# Build
docker build -t electioniq .

# Run
docker run -p 8080:8080 -e GEMINI_API_KEY=your_key_here electioniq
```

---

## Deploy to Google Cloud Run

### Prerequisites

1. **Install gcloud CLI**
   - Download from [console.cloud.google.com/sdk](https://console.cloud.google.com/sdk)
   - Run: `gcloud auth login`
   - Set project: `gcloud config set project YOUR_PROJECT_ID`

2. **Install Docker Desktop**
   - Download from [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop)
   - Keep Docker running during deploy

3. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

### Deploy Command

```bash
gcloud run deploy electioniq \
  --source . \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

> Replace `your_key_here` with your actual Gemini API key.

The command will build, push, and deploy automatically. You'll get a public URL like:
`https://electioniq-xxxxxxxx-el.a.run.app`

---

## Project Structure

```
electioniq/
├── main.py          FastAPI backend + Gemini integration
├── index.html       Complete frontend (5 screens, SPA)
├── requirements.txt Python dependencies
├── Dockerfile       Container definition
├── .env.example     Environment variable template
├── .gitignore       Git ignore rules
└── README.md        This file
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Send message to Gemini AI |
| `GET` | `/` | Serve frontend |

### POST /chat

**Request:**
```json
{
  "messages": [
    {"role": "user", "content": "Previous message"},
    {"role": "model", "content": "Previous response"}
  ],
  "user_message": "How do I register to vote?"
}
```

**Response:**
```json
{
  "response": "To register as a voter in India..."
}
```

---

## License

MIT
