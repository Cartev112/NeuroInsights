# NeuroInsights Implementation Guide
## LLM-First Development with Mock Data

**Priority:** LLM features first, real brain data later  
**Strategy:** Mock data for prototype, modular design for easy swap

---

## Quick Start Checklist

### Phase 1: Foundation (Week 1-2)
- [ ] Set up FastAPI backend with PostgreSQL + TimescaleDB
- [ ] Create React + TypeScript frontend with shadcn/ui
- [ ] Implement mock brain data generator
- [ ] Build basic API endpoints
- [ ] Set up Docker development environment

### Phase 2: LLM Integration (Week 3-4)
- [ ] Integrate OpenAI GPT-4 API
- [ ] Create system prompts for brain data analysis
- [ ] Build chat interface with function calling
- [ ] Implement data query tools for LLM
- [ ] Create frontend chat UI

### Phase 3: Analysis (Week 5-6)
- [ ] Build state detection system (rule-based)
- [ ] Implement pattern matching
- [ ] Create statistical analysis tools
- [ ] Integrate analysis into LLM responses

### Phase 4: Insights (Week 7-8)
- [ ] Build insight generation service
- [ ] Create recommendation engine
- [ ] Add dashboard with visualizations
- [ ] Implement daily summaries

---

## Technology Stack

### Backend
- **FastAPI** (Python 3.11+) - API framework
- **PostgreSQL + TimescaleDB** - Time-series data
- **Redis** - Caching
- **OpenAI GPT-4** - Primary LLM
- **LangChain** - LLM orchestration
- **NumPy/Pandas** - Data processing

### Frontend
- **React 18 + TypeScript**
- **shadcn/ui + Tailwind CSS**
- **TanStack Query** - State management
- **Recharts** - Visualizations
- **Lucide React** - Icons

### Infrastructure
- **Docker Compose** - Local development
- **Railway/Render** - Backend hosting
- **Vercel** - Frontend hosting

---

## Project Structure

```
NeuroInsights/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/routes/          # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── core/
│   │   │   ├── llm/            # LLM integration
│   │   │   ├── mock_data/      # Mock data generation
│   │   │   └── analysis/       # State detection, patterns
│   │   ├── models/             # Database models
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/           # Chat interface
│   │   │   ├── dashboard/      # Dashboard widgets
│   │   │   └── visualizations/ # Charts
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── services/api.ts
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## Mock Data Architecture

### Brain Wave Bands
```python
FREQUENCY_BANDS = {
    'delta': (0.5, 4),    # Deep sleep
    'theta': (4, 8),      # Drowsy, creative
    'alpha': (8, 13),     # Relaxed, calm
    'beta': (13, 30),     # Alert, focused
    'gamma': (30, 100)    # Peak focus
}
```

### Cognitive States
```python
COGNITIVE_STATES = {
    'deep_focus': {
        'beta': 'high', 'alpha': 'low', 'gamma': 'moderate'
    },
    'relaxed': {
        'alpha': 'high', 'beta': 'low', 'theta': 'moderate'
    },
    'stressed': {
        'beta': 'very_high', 'alpha': 'very_low'
    },
    'creative_flow': {
        'theta': 'high', 'alpha': 'high', 'beta': 'moderate'
    },
    'drowsy': {
        'theta': 'high', 'beta': 'low'
    },
    'distracted': {
        'beta': 'fluctuating', 'alpha': 'fluctuating'
    }
}
```

### Mock Data Generator
```python
class MockBrainDataGenerator:
    def generate_session(
        self,
        duration_minutes: int,
        primary_state: str,
        activities: List[Activity]
    ) -> BrainDataSession:
        """Generate realistic session with state transitions"""
        
    def generate_state_data(
        self,
        state: str,
        duration_seconds: int
    ) -> np.ndarray:
        """Generate EEG data for specific state"""
        
    def add_artifacts(self, data: np.ndarray) -> np.ndarray:
        """Add realistic noise and artifacts"""
```

### Pre-built Scenarios
```python
SCENARIOS = {
    'typical_workday': [
        {'time': 0, 'state': 'focused', 'activity': 'emails', 'duration': 30},
        {'time': 30, 'state': 'deep_focus', 'activity': 'coding', 'duration': 90},
        {'time': 120, 'state': 'distracted', 'duration': 15},
        {'time': 135, 'state': 'relaxed', 'activity': 'break', 'duration': 15},
        # ... etc
    ],
    'meditation_session': [...],
    'creative_work': [...]
}
```

### Data Provider Interface (for easy swap later)
```python
class BrainDataProvider(ABC):
    @abstractmethod
    async def get_session_data(self, session_id: str) -> BrainDataSession:
        pass
    
    @abstractmethod
    async def get_time_range_data(
        self, user_id: str, start: datetime, end: datetime
    ) -> List[BrainDataSession]:
        pass

# Mock implementation
class MockBrainDataProvider(BrainDataProvider):
    # Uses generators
    
# Future real implementation  
class RealBrainDataProvider(BrainDataProvider):
    # Connects to EEG devices
```

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Brain sessions
CREATE TABLE brain_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    data_source VARCHAR(50) DEFAULT 'mock'
);

-- Time-series brain data (TimescaleDB hypertable)
CREATE TABLE brain_data_points (
    time TIMESTAMPTZ NOT NULL,
    session_id UUID REFERENCES brain_sessions(id),
    delta FLOAT,
    theta FLOAT,
    alpha FLOAT,
    beta FLOAT,
    gamma FLOAT,
    state VARCHAR(50),
    confidence FLOAT
);

SELECT create_hypertable('brain_data_points', 'time');

-- Activities
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id UUID,
    name VARCHAR(255),
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    category VARCHAR(100)
);

-- Insights
CREATE TABLE insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    insight_type VARCHAR(100),
    content TEXT,
    dismissed BOOLEAN DEFAULT FALSE
);

-- Chat history
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    role VARCHAR(20),
    content TEXT,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

---

## LLM Integration

### System Prompt
```python
SYSTEM_PROMPT = """You are NeuroInsights AI, an expert in brain data analysis and cognitive optimization.

Your role:
- Interpret EEG data (delta, theta, alpha, beta, gamma)
- Identify cognitive states (focused, relaxed, stressed, creative, drowsy, distracted)
- Provide actionable insights and recommendations
- Explain patterns in clear, accessible language

Key principles:
1. Be specific and data-driven
2. Always cite data (timestamps, values)
3. Provide confidence levels
4. Give actionable recommendations
5. Use analogies for complex patterns
6. Never make medical diagnoses

Available data:
- Brain wave frequencies
- Cognitive state classifications
- Activity labels
- Time-series data (minute-level)

Response format:
- Direct answer first
- Supporting evidence
- Actionable insights
- Suggest follow-up questions
"""
```

### Function Tools
```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_brain_data",
            "description": "Retrieve brain data for time range",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"},
                    "granularity": {
                        "type": "string",
                        "enum": ["minute", "5min", "hour"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_state_distribution",
            "description": "Get cognitive state distribution",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_period": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_time_periods",
            "description": "Compare brain patterns between periods",
            "parameters": {
                "type": "object",
                "properties": {
                    "period1": {"type": "string"},
                    "period2": {"type": "string"},
                    "metric": {
                        "type": "string",
                        "enum": ["focus_time", "stress_level", "all"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_patterns",
            "description": "Find patterns/correlations",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern_type": {
                        "type": "string",
                        "enum": ["activity_correlation", "time_of_day", "state_transitions"]
                    }
                }
            }
        }
    }
]
```

### Chat API
```python
@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user)
):
    # Get history
    history = await get_chat_history(user.id, limit=10)
    
    # Build messages
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": request.message}
    ]
    
    # Call LLM with tools
    response = await llm_service.chat_completion(
        messages=messages,
        tools=TOOLS
    )
    
    # Handle function calls
    if response.tool_calls:
        tool_results = await execute_tool_calls(response.tool_calls, user.id)
        messages.append(response.message)
        messages.append(tool_results)
        final_response = await llm_service.chat_completion(messages)
    else:
        final_response = response.content
    
    # Save to history
    await save_chat_message(user.id, request.message, final_response)
    
    return {"response": final_response}
```

---

## State Detection

### Rule-Based Classifier (MVP)
```python
class StateDetector:
    def detect_state(
        self,
        brain_data: BrainWaveData
    ) -> CognitiveState:
        """
        Detect cognitive state from brain waves
        
        Rules based on neuroscience:
        - High beta + low alpha = Focused
        - High alpha + low beta = Relaxed
        - Very high beta + low alpha = Stressed
        - High theta + high alpha = Creative
        - High theta + low beta = Drowsy
        - Fluctuating = Distracted
        """
        norm = self._normalize_bands(brain_data)
        
        if norm['beta'] > 0.7 and norm['alpha'] < 0.3:
            if norm['beta'] > 0.85:
                return CognitiveState('stressed', confidence=0.8)
            return CognitiveState('deep_focus', confidence=0.85)
        
        elif norm['alpha'] > 0.7 and norm['beta'] < 0.4:
            return CognitiveState('relaxed', confidence=0.8)
        
        elif norm['theta'] > 0.6 and norm['alpha'] > 0.5:
            return CognitiveState('creative_flow', confidence=0.75)
        
        elif norm['theta'] > 0.7 and norm['beta'] < 0.3:
            return CognitiveState('drowsy', confidence=0.8)
        
        elif self._is_fluctuating(brain_data):
            return CognitiveState('distracted', confidence=0.7)
        
        return CognitiveState('neutral', confidence=0.6)
```

---

## Pattern Analysis

### Activity Correlations
```python
class PatternMatcher:
    async def find_activity_correlations(
        self,
        user_id: str,
        time_range: TimeRange
    ) -> List[ActivityCorrelation]:
        """Find which activities correlate with which states"""
        sessions = await self.get_sessions_with_activities(user_id, time_range)
        
        correlations = {}
        for session in sessions:
            for activity in session.activities:
                states = self._get_states_during_activity(session, activity)
                
                if activity.name not in correlations:
                    correlations[activity.name] = StateDistribution()
                correlations[activity.name].add_states(states)
        
        return self._rank_correlations(correlations)
```

### Optimal Time Windows
```python
async def find_optimal_times(
    self,
    user_id: str,
    desired_state: str,
    lookback_days: int = 30
) -> List[TimeWindow]:
    """Find when user naturally enters desired state"""
    # Analyze historical data
    # Group by time of day
    # Return windows with highest probability
```

---

## Insight Generation

### Daily Insights
```python
class InsightService:
    async def generate_daily_insights(
        self,
        user_id: str
    ) -> List[Insight]:
        """Generate end-of-day insights"""
        today_data = await self.get_today_data(user_id)
        baseline = await self.get_user_baseline(user_id)
        
        insights = []
        
        # Focus analysis
        focus_time = self._calculate_focus_time(today_data)
        if focus_time < baseline.avg_focus_time * 0.8:
            insights.append(Insight(
                type='focus_low',
                content=f"Your focus time was {focus_time}min today, "
                        f"{baseline.avg_focus_time - focus_time}min below your average.",
                recommendation="Consider reviewing your schedule for distractions."
            ))
        
        # Stress analysis
        stress_periods = self._find_stress_periods(today_data)
        if len(stress_periods) > 2:
            insights.append(Insight(
                type='stress_high',
                content=f"Detected {len(stress_periods)} stress periods today.",
                recommendation="Try a 10-minute break or breathing exercise."
            ))
        
        # Pattern discoveries
        patterns = await self._find_new_patterns(user_id)
        insights.extend(patterns)
        
        return insights
```

---

## Example Queries & Responses

### Query 1: "How was my focus today?"
**LLM Response:**
```
Your focus today was above average! Here's the breakdown:

**Focus Time:** 4.2 hours (68% of work time)
- Deep focus: 2.5 hours
- Light focus: 1.7 hours

**Compared to your baseline:**
- 15% better than your 30-day average (3.6 hours)
- Your best focus day this week

**Peak focus periods:**
- 9:30 AM - 11:00 AM (90 minutes of deep focus)
- 2:00 PM - 3:30 PM (90 minutes)

**Recommendation:** Your morning focus window (9:30-11 AM) is consistently strong. 
Consider scheduling your most demanding tasks during this time.
```

### Query 2: "What activities help me focus best?"
**LLM Response:**
```
Based on 30 days of data, here are your top focus-inducing activities:

1. **Coding** (avg 78% focus time)
   - Best time: 9-11 AM
   - Deep focus state: 65% of the time
   
2. **Writing** (avg 72% focus time)
   - Best time: 2-4 PM
   - Creative flow state: 45% of the time
   
3. **Reading technical docs** (avg 68% focus time)
   - Best time: Morning (8-10 AM)

**Least conducive to focus:**
- Meetings (42% focus time)
- Email processing (38% focus time)

**Insight:** You enter creative flow most easily during afternoon writing sessions. 
Consider blocking 2-4 PM for creative work.
```

### Query 3: "Why was I so tired yesterday afternoon?"
**LLM Response:**
```
I found several factors that contributed to your afternoon fatigue yesterday:

**Primary cause:** Extended high cognitive load without breaks
- 9 AM - 1 PM: 4 hours of continuous focused work
- No significant breaks detected
- Cognitive load score: 8.5/10 (very high)

**Contributing factors:**
1. **Sleep:** Your deep sleep was 18% below average the night before
2. **Stress:** Elevated stress markers during 11 AM - 12 PM period
3. **No recovery time:** Went straight from meeting to focused work

**Brain data:**
- Beta waves remained elevated (stress indicator)
- Alpha waves didn't recover during lunch
- Theta increased sharply at 2 PM (drowsiness)

**Recommendation:** After intense focus sessions (2+ hours), take a 15-20 minute 
break to allow your brain to recover. Your data shows alpha waves need 15 minutes 
to return to baseline.
```

---

## Frontend Components

### Chat Interface
```typescript
// src/components/chat/ChatInterface.tsx
export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const { sendMessage, isLoading } = useChat();
  
  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    
    const response = await sendMessage(input);
    setMessages(prev => [...prev, {
      role: 'assistant',
      content: response
    }]);
  };
  
  return (
    <div className="flex flex-col h-screen">
      <MessageList messages={messages} />
      <InputBar 
        value={input}
        onChange={setInput}
        onSend={handleSend}
        isLoading={isLoading}
        placeholder="Ask about your brain data..."
      />
    </div>
  );
}
```

### Dashboard
```typescript
// src/components/dashboard/Dashboard.tsx
export function Dashboard() {
  const { data: todayData } = useBrainData('today');
  const { data: insights } = useInsights();
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CognitiveScoreCard score={todayData?.cognitiveScore} />
      <StateDistributionChart data={todayData?.stateDistribution} />
      <FocusTimeCard focusMinutes={todayData?.focusTime} />
      <InsightsFeed insights={insights} />
      <ActivityCorrelationChart data={todayData?.activityCorrelations} />
      <BrainWaveChart data={todayData?.brainWaves} />
    </div>
  );
}
```

---

## Testing Strategy

### Unit Tests
- Mock data generators
- State detection logic
- Pattern matching algorithms
- Statistical calculations

### Integration Tests
- API endpoints
- LLM function calling
- Database operations
- Chat flow

### E2E Tests
- User can chat and get responses
- Insights are generated correctly
- Dashboard displays data
- State detection works end-to-end

### LLM Testing
- Prompt effectiveness
- Response quality
- Function calling accuracy
- Edge cases handling

---

## Deployment

### Development
```bash
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### Production
- **Backend:** Railway/Render with PostgreSQL addon
- **Frontend:** Vercel
- **Environment variables:**
  - `OPENAI_API_KEY`
  - `DATABASE_URL`
  - `REDIS_URL`
  - `JWT_SECRET`

---

## Next Steps After MVP

1. **ML-based state detection** (replace rules)
2. **Real EEG device integration** (replace mock data)
3. **Mobile apps** (iOS/Android)
4. **Advanced visualizations**
5. **Neurofeedback training programs**
6. **Multi-user features**
7. **API for third-party integrations**

---

## Key Files to Create First

1. `backend/app/core/mock_data/generators.py` - Mock data generation
2. `backend/app/core/llm/prompts.py` - System prompts
3. `backend/app/services/llm_service.py` - LLM integration
4. `backend/app/core/analysis/state_detector.py` - State detection
5. `frontend/src/components/chat/ChatInterface.tsx` - Chat UI
6. `docker-compose.yml` - Development environment
7. `backend/app/models/database.py` - Database models

---

## Development Tips

1. **Start with one scenario:** Build "typical_workday" scenario first
2. **Test LLM prompts early:** Iterate on prompts before building features
3. **Keep mock data realistic:** Study real EEG patterns
4. **Log everything:** LLM calls, function calls, state detections
5. **Build incrementally:** Get chat working, then add features
6. **Document prompts:** Keep prompt engineering notes
7. **Plan for swap:** Keep mock data layer isolated

---

## Success Metrics

### MVP Goals
- [ ] Chat interface responds in < 3 seconds
- [ ] State detection accuracy > 75% (user validation)
- [ ] Users can query last 30 days of mock data
- [ ] Daily insights generated automatically
- [ ] Dashboard loads in < 2 seconds
- [ ] 5+ example scenarios working
- [ ] LLM provides actionable recommendations

### User Experience
- Natural conversation flow
- Clear, non-technical explanations
- Actionable insights
- Beautiful visualizations
- Fast, responsive interface

---

This implementation guide prioritizes LLM features with mock data. Focus on making the conversational interface excellent - that's the core differentiator. Real brain data integration comes later once the UX is validated.
