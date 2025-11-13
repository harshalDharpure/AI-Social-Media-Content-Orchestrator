# Quick Start Guide

## Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (optional, for scheduling)
- API keys for LLM (OpenAI, Anthropic, or Google)

## Quick Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with at least one LLM API key (OpenAI, Anthropic, or Google)
# Add other API keys as needed

# Run the server
uvicorn main:app --reload
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL (default: http://localhost:8000)

# Run the development server
npm run dev
```

### 3. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Minimum Configuration

To get started quickly, you only need:

1. **At least one LLM API key** (OpenAI, Anthropic, or Google)
   - Add to `.env` file in backend directory
   - Example: `OPENAI_API_KEY=your_key_here`

2. **Vector Database** (optional for RAG)
   - Use Qdrant locally: `docker run -p 6333:6333 qdrant/qdrant`
   - Or set `USE_PINECONE=false` in `.env`

3. **Social Media APIs** (optional)
   - Add API keys for Twitter, Instagram, or LinkedIn as needed
   - Without these, you can still generate content but not post it

## First Steps

1. **Generate Content**
   - Go to Content Generator page
   - Enter a topic
   - Select a platform
   - Click "Generate Content"

2. **Upload Brand Documents** (optional)
   - Go to RAG page
   - Upload brand guidelines, tone guides, or FAQs
   - This will help generate more on-brand content

3. **Schedule Posts** (optional)
   - Go to Scheduling page
   - Enter content and select platform
   - Set schedule time or post immediately
   - Requires social media API keys

4. **View Analytics** (optional)
   - Go to Analytics page
   - View performance metrics
   - Get AI-powered recommendations
   - Requires social media API keys

## Troubleshooting

### Backend won't start
- Check that you have at least one LLM API key set
- Verify Python version is 3.9+
- Check that all dependencies are installed

### Frontend won't start
- Check that Node.js version is 18+
- Verify all dependencies are installed
- Check that backend is running on port 8000

### Content generation fails
- Verify LLM API key is valid
- Check API rate limits
- Verify network connectivity

### Vector store not working
- Check vector database is running (if using Qdrant locally)
- Verify API keys (if using Pinecone)
- Check network connectivity

## Next Steps

1. **Add Social Media APIs**
   - Set up Twitter, Instagram, or LinkedIn API keys
   - Configure OAuth if needed
   - Test posting functionality

2. **Configure Vector Database**
   - Set up Pinecone or Qdrant
   - Upload brand documents
   - Test RAG functionality

3. **Set up Scheduling**
   - Install and run Redis
   - Configure scheduling
   - Test scheduled posts

4. **Customize Content**
   - Upload brand guidelines
   - Configure tone and style
   - Test content generation

## Support

For detailed setup instructions, see [SETUP.md](SETUP.md).

For issues and questions, check the README or open an issue on GitHub.

