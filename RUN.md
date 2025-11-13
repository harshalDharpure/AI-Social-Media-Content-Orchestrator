# How to Run the Project

## Quick Start

### Option 1: Using Run Scripts (Easiest)

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
run.bat
```

### Option 2: Manual Setup

## Prerequisites

- **Python 3.9+** installed
- **Node.js 18+** installed
- **npm** or **yarn** installed

## Step-by-Step Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (at minimum, add one LLM API key)

# Run the server
uvicorn main:app --reload
```

The backend will start on `http://localhost:8000`

### 2. Frontend Setup

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local if needed (default API URL is http://localhost:8000)

# Run the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Minimum Configuration

To get started quickly, you only need:

1. **At least one LLM API key** in `backend/.env`:
   ```
   OPENAI_API_KEY=your_key_here
   # OR
   ANTHROPIC_API_KEY=your_key_here
   # OR
   GOOGLE_API_KEY=your_key_here
   ```

2. **Backend running** on port 8000

3. **Frontend running** on port 3000

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in backend/.env or use:
uvicorn main:app --reload --port 8001
```

**Module not found:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**No LLM API key:**
- Add at least one LLM API key to `backend/.env`
- Options: OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY

### Frontend Issues

**Port already in use:**
```bash
# Vite will automatically use the next available port
# Or specify a port:
npm run dev -- --port 3001
```

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

**Cannot connect to backend:**
- Make sure backend is running on port 8000
- Check `frontend/.env.local` has correct API URL:
  ```
  VITE_API_URL=http://localhost:8000
  ```

## Development Tips

1. **Backend hot reload**: Already enabled with `--reload` flag
2. **Frontend hot reload**: Vite automatically reloads on changes
3. **API changes**: Backend will auto-reload when you save files
4. **View logs**: Check `backend/logs/` directory for application logs

## Stopping the Servers

- **Linux/Mac**: Press `Ctrl+C` in each terminal
- **Windows**: Close the command windows or press `Ctrl+C`

## Next Steps

1. **Generate Content**: Go to Content Generator page
2. **Upload Documents**: Go to RAG page to upload brand documents
3. **Schedule Posts**: Go to Scheduling page (requires social media API keys)
4. **View Analytics**: Go to Analytics page (requires social media API keys)

## Production Deployment

For production deployment, see `PRODUCTION.md`

