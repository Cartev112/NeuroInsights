# NeuroInsights - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Set Up Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Start the Application

**Option A: Docker (Recommended)**
```bash
docker-compose up --build
```

**Option B: Manual Setup**

Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (in a new terminal):
```bash
cd frontend
npm install
npm run dev
```

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🧪 Try These Example Queries

Open the Chat page and try:

1. **"How was my focus today?"**
   - Gets cognitive score and focus time analysis

2. **"Show me my brain state distribution for the last 7 days"**
   - Displays percentage of time in each cognitive state

3. **"When am I most focused during the day?"**
   - Analyzes time-of-day patterns

4. **"Compare my stress levels today vs yesterday"**
   - Compares metrics between time periods

5. **"What activities help me focus best?"**
   - Finds correlations between activities and states

## 📊 Features Available

### ✅ Chat Interface
- Natural language queries
- GPT-4 powered responses
- Function calling for data retrieval
- Context-aware conversations

### ✅ Dashboard
- Cognitive fitness score (0-100)
- State distribution pie chart
- Brain wave activity line chart
- Real-time data visualization

### ✅ Insights
- Daily AI-generated summaries
- Performance metrics
- Actionable recommendations
- Pattern analysis

### ✅ Mock Data System
- 6 cognitive states (deep_focus, relaxed, stressed, creative_flow, drowsy, distracted)
- 5 pre-built scenarios (workday, meditation, creative work, etc.)
- Realistic EEG patterns with noise
- User-specific baseline variations

## 🔧 Troubleshooting

**TypeScript errors in IDE?**
- These are expected before running `npm install`
- Run `npm install` in the frontend directory to resolve

**Backend won't start?**
- Check that Python 3.11+ is installed
- Verify OpenAI API key in `.env`
- Make sure port 8000 is available

**Frontend won't start?**
- Check that Node.js 18+ is installed
- Delete `node_modules` and run `npm install` again
- Make sure port 3000 is available

**Docker issues?**
- Ensure Docker is running
- Try `docker-compose down -v` to reset
- Check that ports 3000, 8000, 5432, 6379 are available

**Chat not responding?**
- Verify OpenAI API key is correct
- Check backend logs for errors
- Ensure you have API credits available

## 📁 Project Structure

```
NeuroInsights/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/routes/  # API endpoints
│   │   ├── core/        # Mock data, LLM, analysis
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   └── requirements.txt
│
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json
│
└── docker-compose.yml   # Docker setup
```

## 🎯 Next Steps

1. **Explore the Chat Interface**
   - Ask different types of questions
   - Try the example queries above
   - Experiment with time ranges

2. **Check the Dashboard**
   - View your cognitive score
   - See state distribution
   - Analyze brain wave patterns

3. **Read Daily Insights**
   - Get AI-generated summaries
   - Review performance metrics
   - Follow recommendations

4. **Customize Mock Data**
   - Edit `backend/app/core/mock_data/patterns.py`
   - Add new cognitive states
   - Create custom scenarios

5. **Extend the System**
   - Add new LLM tools in `backend/app/core/llm/tools.py`
   - Create new visualizations
   - Implement additional analysis features

## 📚 Documentation

- **Full Implementation Guide:** `IMPLEMENTATION.md`
- **Feature Specifications:** `planning.md`
- **API Documentation:** http://localhost:8000/docs (when running)

## 🎉 You're Ready!

The MVP is complete and ready to use. All TypeScript errors will resolve once you run `npm install` in the frontend directory.

Start exploring your brain data with natural language!
