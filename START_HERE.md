# Getting Started with NeuroInsights

## Quick Start

### 1. Prerequisites
- Docker & Docker Compose installed
- OpenAI API key

### 2. Setup

1. **Create environment file:**
```bash
cp .env.example .env
```

2. **Edit `.env` and add your OpenAI API key:**
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start the Application

**Option A: Using Docker (Recommended)**
```bash
docker-compose up --build
```

**Option B: Manual Setup**

Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### 5. Test the Chat Interface

Try these example queries:
- "How was my focus today?"
- "Show me my brain state distribution for the last 7 days"
- "When am I most focused during the day?"
- "Compare my stress levels today vs yesterday"

## Project Status

✅ **Completed:**
- Project structure
- Mock data generation system
- LLM integration with OpenAI GPT-4
- Chat API with function calling
- Brain data analysis endpoints
- Frontend scaffolding

🚧 **In Progress:**
- Frontend components (chat interface, dashboard, visualizations)
- Database setup and migrations
- User authentication

📋 **TODO:**
- Complete frontend implementation
- Add database persistence
- Implement insights generation
- Add more pre-built scenarios
- Testing suite

## Development Notes

### Mock Data
The system currently uses mock brain data generated on-the-fly. The mock data generator creates realistic EEG patterns based on cognitive states defined in `backend/app/core/mock_data/patterns.py`.

### LLM Integration
The chat interface uses OpenAI's GPT-4 with function calling to query brain data. Available functions are defined in `backend/app/core/llm/tools.py`.

### Next Steps
1. Complete frontend components (see IMPLEMENTATION.md Phase 2-4)
2. Set up database with Alembic migrations
3. Implement user authentication
4. Add more visualization components
5. Test end-to-end workflows

## Troubleshooting

**Docker issues:**
- Make sure Docker is running
- Try `docker-compose down -v` to reset volumes

**Port conflicts:**
- Backend uses port 8000
- Frontend uses port 3000
- PostgreSQL uses port 5432
- Redis uses port 6379

**OpenAI API errors:**
- Verify your API key is correct in `.env`
- Check you have API credits available

## Documentation

- **Implementation Guide:** See `IMPLEMENTATION.md` for detailed development plan
- **Planning Document:** See `planning.md` for full feature specifications
- **API Documentation:** Visit http://localhost:8000/docs when backend is running
