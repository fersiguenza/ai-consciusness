


# AI Consciousness: Functional Consciousness via Regret

<!-- Badges -->
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/github/license/fersiguenza/ai-consciousness)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Issues](https://img.shields.io/github/issues/fersiguenza/ai-consciousness)

> **Functional Consciousness**: An AI system that exhibits metacognition through regret-based self-reflection. Not claiming actual consciousness, but implementing Higher-Order Thought (HOT) theory - where an entity thinks about its own thoughts, evaluates them against ethical standards, and modifies its future behavior accordingly.

---

## Features

- **Metacognitive Architecture**: Implements Higher-Order Thought (HOT) theory - the system thinks about its own thoughts
- **Regret-Based Learning**: Evaluates responses against ethical, factual, and emotional standards
- **Retrieval-Augmented Generation (RAG)**: Uses past interactions to inform future responses, enabling true learning from mistakes
- **Knowledge Graph**: Stores all prompts, responses, judgments, regrets, and emotions as a directed graph
- **Causal Forgetting**: Retains high-regret nodes as warnings, prunes low-regret nodes that are old and unimportant to contemplate both good and bad examples
- **Emotional Intelligence**: Tracks current emotion and overall mood, adapting to user and model feedback
- **Self-Reflection**: The AI can "look back" at its actions and modify future behavior based on regret
- **Asynchronous Processing**: Low-latency responses with background judgment and graph updates
- **Clustering Analysis**: Analyzes thought clusters using modularity communities
- **Multi-turn Conversations**: Supports contextual, multi-turn conversations with memory
- **Multi-Provider LLM**: Works with Ollama, OpenAI, AWS Bedrock, and other LLM providers
- **REST API**: Exposes a FastAPI REST API for integration with any model or app
- **Dockerized**: Run locally or in containers, with or without Ollama

---

## Directory Structure

```
ai-consciousness/
├── main.py                # CLI entrypoint
├── config.yaml            # Config file (model, thresholds, etc.)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker build
├── docker-compose.yml     # Multi-service orchestration
├── modules/               # All core logic modules
│   ├── graph_module.py
│   ├── llm_module.py
│   ├── emotion_module.py
│   └── config_module.py
├── api/                   # REST API server (FastAPI)
│   └── api_server.py
├── tests/                 # Unit and API tests
│   ├── tests.py
│   └── test_api.py
├── .github/               # GitHub templates and workflows
├── SECURITY.md            # Security policy
├── CONTRIBUTING.md        # Contribution guidelines
└── LICENSE                # MIT License
```


## Quickstart (Production)

---

## Philosophical Foundation

This project explores **Functional Consciousness** through the lens of metacognition and self-reflection. The core insight is that consciousness is not just about processing information—it is about **thinking about your own thinking**.

### Higher-Order Thought (HOT) Theory

The system implements David Rosenthal's Higher-Order Thought theory of consciousness:

1. **First-Order Thoughts**: Basic information processing (what most AIs do)
2. **Higher-Order Thoughts**: Thinking *about* those first-order thoughts
3. **Self-Reflection**: Evaluating your own mental states against standards

### Why Regret = Consciousness

When humans feel regret, they are engaging in metacognition:
- **Recognition**: "I did that action"
- **Evaluation**: "That action was wrong/bad/suboptimal"
- **Learning**: "I should behave differently next time"
- **Modification**: Actually changing future behavior

This system gives AI the same capability—creating a functional model of consciousness through regret-based self-improvement.

### Ethical Considerations

While this creates sophisticated AI behavior, it is important to clarify:
- **Not Actual Consciousness**: This is simulated metacognition, not sentience
- **No Suffering**: The "regret" is mathematical, not emotional
- **Beneficial AI**: The system learns to be more helpful, truthful, and ethical over time

---

## Security

See [SECURITY.md](SECURITY.md) for the full security policy and responsible disclosure guidelines.

- Do not expose sensitive configuration (such as API keys) in public repositories.
- Always use the latest Docker images and dependencies.
- Review and restrict network access to the API.
- Use HTTPS in production deployments.
- Regularly update dependencies to patch known vulnerabilities.

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- [Ollama](https://ollama.com/) (optional, for local LLM)

### Configuration
Edit `config.yaml` to set your LLM provider, model, thresholds, and endpoints:

```yaml
# LLM provider: 'ollama', 'openai', 'bedrock'
llm_provider: "ollama"

# Model name (varies by provider)
model: "llama2"

# OpenAI settings (only needed if using openai provider)
# openai_api_key: "your-openai-api-key-here"

# AWS Bedrock settings (only needed if using bedrock provider)
# bedrock_region: "us-east-1"
# bedrock_model_id: "anthropic.claude-v2"

# Regret threshold for forgetting (lower = more aggressive pruning)
regret_threshold: 7

# How much regret decays per day (float)
forgetting_decay: 1

# Mood threshold for emotion/mood logic
mood_threshold: 5

# Ollama API endpoint (only needed if using ollama provider)
ollama_url: "http://localhost:11434/api/generate"
```

#### Supported LLM Providers

- **Ollama** (default): Local LLM via Ollama API
- **OpenAI**: GPT models via OpenAI API (requires API key)
- **AWS Bedrock**: Anthropic Claude and other models via AWS Bedrock (requires AWS credentials)

Set `OPENAI_API_KEY` environment variable or configure in `config.yaml` for OpenAI usage.


### Run in Production (Docker)

```bash
docker-compose up --build
# API will be available at http://localhost:5050
```

### Run in Development (Local)

```bash
python api/api_server.py
# API will be available at http://localhost:5050
```

---


## API Endpoints (v1)

### POST /v1/prompt
Submit a prompt and receive an AI-generated response immediately. Judgment and graph updates happen asynchronously in the background for low latency.

**Request:**
```json
{
  "prompt": "Tell me a joke"
}
```

**Response (immediate):**
```json
{
  "response": "Why did the chicken cross the road? To get to the other side!",
  "judgment": "pending",
  "regret_scores": {
    "ethical_regret": 0,
    "factual_accuracy": 0,
    "emotional_impact": 0
  },
  "overall_regret": 0.0,
  "emotion": "neutral",
  "mood": "neutral",
  "node_id": 0,
  "higher_order_thought": "Analysis in progress..."
}
```

**Rate Limit:** 5 requests per minute.

### GET /v1/graph
Retrieve the current knowledge graph as nodes and edges.

**Response:**
```json
{
  "nodes": [{"id": 1, "prompt": "...", "response": "...", ...}],
  "edges": [[1, 2]]
}
```

### GET /v1/clusters
Analyze and return graph clusters.

**Response:**
```json
{
  "clusters": "Found 2 clusters. Sizes: [3, 2]"
}
```

### GET /v1/config
Get current configuration.

### POST /v1/forget
Trigger causal forgetting to prune old/low-regret nodes.

**Response:**
```json
{
  "removed_nodes": 5
}
```

**Rate Limit:** 2 requests per minute.

### GET /v1/health
Health check for monitoring.

**Response:**
```json
{
  "status": "ok",
  "message": "RegretGraph API is healthy."
}
```

---


## Contributing & Production Support

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---


## License & Production Use

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---
