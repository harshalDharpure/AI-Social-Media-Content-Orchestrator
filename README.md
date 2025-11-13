# AI Social Media Content Orchestrator

An end-to-end AI agent system that creates, schedules, and optimizes social media content automatically — from ideation to publishing.

## Features

- **Content Brainstorming**: LLM-powered post ideas based on trending topics
- **RAG Pipeline**: Context-aware content generation using brand documents
- **Vision Integration**: Text-to-image generation and image analysis
- **Workflow Automation**: Auto-post and schedule across multiple platforms
- **Analytics Agent**: Performance tracking and AI-powered recommendations

## Tech Stack

### Backend
- FastAPI (Python)
- LangChain / LangGraph (RAG + Orchestration)
- Claude / Gemini APIs
- Stable Diffusion (Image Generation)
- Pinecone / Qdrant (Vector Database)
- Supabase (Database + Storage)

### Frontend
- React
- TypeScript
- Tailwind CSS

## Setup

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your API endpoint
```

3. Run the development server:
```bash
npm run dev
```

## Environment Variables

See `.env.example` files in both backend and frontend directories for required environment variables.

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## License

MIT

