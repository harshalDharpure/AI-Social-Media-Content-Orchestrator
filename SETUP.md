# Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (for scheduling)
- PostgreSQL (optional, for Supabase)
- Vector Database (Pinecone or Qdrant)

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Required API Keys:**
   - At least one LLM API key (OpenAI, Anthropic, or Google)
   - Vector database (Pinecone or Qdrant)
   - Social media API keys (Twitter, Instagram, LinkedIn)
   - Supabase credentials (optional)

6. **Initialize vector store:**
   - For Pinecone: Create an account and get API key
   - For Qdrant: Run locally or use cloud instance

7. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

## Configuration

### Vector Database

#### Pinecone Setup
1. Sign up at https://www.pinecone.io/
2. Create an index
3. Add `PINECONE_API_KEY` and `PINECONE_ENVIRONMENT` to `.env`
4. Set `USE_PINECONE=true` in `.env`

#### Qdrant Setup
1. Run locally: `docker run -p 6333:6333 qdrant/qdrant`
2. Or use Qdrant Cloud
3. Set `USE_PINECONE=false` in `.env`
4. Add `QDRANT_URL` to `.env`

### Social Media APIs

#### Twitter API
1. Create a Twitter Developer account
2. Create an app and get API keys
3. Add keys to `.env`

#### Instagram API
1. Create a Facebook Developer account
2. Create an Instagram app
3. Get access token
4. Add to `.env`

#### LinkedIn API
1. Create a LinkedIn Developer account
2. Create an app
3. Get OAuth credentials
4. Add to `.env`

### Image Generation

#### Option 1: Stable Diffusion API
1. Run Stable Diffusion API server
2. Set `STABLE_DIFFUSION_API_URL` in `.env`

#### Option 2: Hugging Face
1. Get API key from Hugging Face
2. Add `HUGGINGFACE_API_KEY` to `.env`

#### Option 3: Replicate
1. Get API token from Replicate
2. Add `REPLICATE_API_TOKEN` to `.env`

## Running the Application

1. **Start Redis (for scheduling):**
   ```bash
   redis-server
   ```

2. **Start backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Issues

1. **Vector store not initializing:**
   - Check API keys
   - Verify vector database is running
   - Check network connectivity

2. **LLM not working:**
   - Verify at least one LLM API key is set
   - Check API key validity
   - Verify rate limits

3. **Social media posting fails:**
   - Check API credentials
   - Verify OAuth tokens are valid
   - Check API permissions

4. **Image generation fails:**
   - Verify image generation API is running
   - Check API keys
   - Verify image URL is accessible

## Production Deployment

1. **Backend:**
   - Use production WSGI server (Gunicorn)
   - Set up proper environment variables
   - Configure CORS for production domain
   - Set up database backups

2. **Frontend:**
   - Build production bundle: `npm run build`
   - Serve with Nginx or similar
   - Configure API URL for production

3. **Infrastructure:**
   - Use cloud database (Supabase, AWS RDS)
   - Use cloud vector database (Pinecone, Qdrant Cloud)
   - Set up monitoring and logging
   - Configure auto-scaling

## Support

For issues and questions, please check the README or open an issue on GitHub.

