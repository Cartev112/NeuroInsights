# NeuroInsights

LLM-powered brain data intelligence platform that transforms brain wave data into actionable insights through natural language conversation.

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NeuroInsights.git
cd NeuroInsights
```

2. Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Start the application:
```bash
docker-compose up
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
NeuroInsights/
├── backend/          # FastAPI backend
├── frontend/         # React + TypeScript frontend
├── docs/            # Documentation
├── scripts/         # Utility scripts
└── docker-compose.yml
```

## Features

- 🧠 Natural language querying of brain data
- 📊 Cognitive state detection (focus, relaxed, stressed, creative, drowsy)
- 📈 Pattern analysis and correlations
- 💡 Proactive insights and recommendations
- 📱 Beautiful, responsive dashboard
- 🔒 Privacy-first architecture

## Tech Stack

**Backend:** FastAPI, PostgreSQL + TimescaleDB, Redis, OpenAI GPT-4  
**Frontend:** React, TypeScript, Tailwind CSS, shadcn/ui  
**Infrastructure:** Docker, Docker Compose

## Documentation

See [IMPLEMENTATION.md](./IMPLEMENTATION.md) for detailed implementation guide.

## License

MIT
