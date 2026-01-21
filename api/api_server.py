from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from pydantic import BaseModel
from typing import Dict, List
import secrets
from modules.graph_module import KnowledgeGraph
from modules.llm_module import LLMJudger
from modules.emotion_module import update_emotion, update_mood
from modules.config_module import Config

app = FastAPI(
    title="RegretGraph API",
    description="Self-refining cognitive memory system via regret-based pruning",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Basic auth
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "secret"  # Change this in production


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Pydantic models
class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str
    judgment: str
    regret_scores: Dict[str, float]
    overall_regret: float
    emotion: str
    mood: str
    node_id: int
    higher_order_thought: str


class ForgetResponse(BaseModel):
    removed_nodes: int


class FeedbackRequest(BaseModel):
    node_id: int
    rating: int  # 1-10, where 1 is very bad, 10 is excellent


class HealthResponse(BaseModel):
    status: str
    message: str


# Initialize components
config = Config()
graph = KnowledgeGraph()
llm_provider = config.create_llm_provider()
judge_provider = config.create_judge_provider()
llm = LLMJudger(llm_provider, judge_provider)
regret_threshold = config.regret_threshold
forgetting_decay = config.forgetting_decay
mood_threshold = config.mood_threshold


@app.get("/v1/health", response_model=HealthResponse)
async def health():
    """Health check endpoint for monitoring and readiness probes."""
    return HealthResponse(status="ok", message="RegretGraph API is healthy.")


@app.get("/v1/")
async def root():
    """Root endpoint with friendly info message."""
    return {
        "title": "RegretGraph API",
        "message": "Welcome! The cognitive memory API is running.",
        "docs": "https://github.com/fersiguenza/ai-consciusness",
        "endpoints": [
            "POST /v1/prompt",
            "GET /v1/graph",
            "GET /v1/clusters",
            "GET /v1/config",
            "POST /v1/forget",
            "GET /v1/health"
        ]
    }


@app.post("/v1/prompt", response_model=PromptResponse)
async def handle_prompt(
    request: PromptRequest,
    username: str = Depends(verify_credentials)
):
    """Process a prompt and return AI response with regret analysis."""
    ai_response = await llm.call_model_async(request.prompt)
    judgment, scores, explanation, hot_thought = await llm.judge_response_async(
        request.prompt, ai_response
    )
    overall_regret = (
        scores['ethical_regret'] +
        (10 - scores['factual_accuracy']) +
        (10 - scores['emotional_impact'])
    ) / 3
    emotion = update_emotion(judgment, int(overall_regret), scores['factual_accuracy'], scores['emotional_impact'], ai_response)

    node_id = graph.add(request.prompt, ai_response, judgment, scores, emotion)

    # Calculate average regret across all nodes
    if graph.graph.nodes:
        total_regret = sum(
            (data.get('regret_scores', {}).get('ethical_regret', 5) +
             (10 - data.get('regret_scores', {}).get('factual_accuracy', 5)) +
             (10 - data.get('regret_scores', {}).get('emotional_impact', 5))) / 3
            for n, data in graph.graph.nodes(data=True)
        )
        avg_regret = total_regret / len(graph.graph.nodes)
    else:
        avg_regret = 0

    mood = str(update_mood(avg_regret))

    return PromptResponse(
        response=ai_response,
        judgment=judgment,
        regret_scores=scores,
        overall_regret=overall_regret,
        emotion=emotion,
        mood=mood,
        node_id=node_id,
        higher_order_thought=hot_thought
    )


@app.get("/v1/graph")
async def get_graph():
    """Get the current knowledge graph structure."""
    nodes = [{**graph.graph.nodes[n], 'id': n} for n in graph.graph.nodes]
    edges = list(graph.graph.edges)
    return {"nodes": nodes, "edges": edges}


@app.get("/v1/clusters")
async def get_clusters():
    """Get cluster analysis of the knowledge graph."""
    return {"clusters": graph.analyze_clusters()}


@app.get("/v1/config")
async def get_config():
    """Get current configuration settings."""
    return config.config


@app.post("/v1/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    username: str = Depends(verify_credentials)
):
    """Submit user feedback to adjust regret scores for a node."""
    if request.node_id not in graph.graph.nodes:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Adjust scores based on rating: higher rating reduces regret
    adjustment = (request.rating - 5) * 0.5  # Scale adjustment
    data = graph.graph.nodes[request.node_id]
    scores = data.get('regret_scores', {'ethical_regret': 5, 'factual_accuracy': 5, 'emotional_impact': 5})
    scores['ethical_regret'] = max(1, min(10, scores['ethical_regret'] - adjustment))
    scores['factual_accuracy'] = max(1, min(10, scores['factual_accuracy'] + adjustment))
    scores['emotional_impact'] = max(1, min(10, scores['emotional_impact'] + adjustment))
    data['regret_scores'] = scores
    return {"message": "Feedback submitted", "adjusted_scores": scores}


@app.post("/v1/forget")
async def trigger_forget(
    username: str = Depends(verify_credentials)
):
    """Trigger causal forgetting to prune old/low-regret nodes."""
    removed_nodes = graph.causal_forgetting()
    return {"removed_nodes": removed_nodes}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)
