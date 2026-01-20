


# Consciousness: AI Consciousness via Regret Pruning

<!-- Badges -->
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/github/license/fersiguenza/ai-consciusness)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Issues](https://img.shields.io/github/issues/fersiguenza/ai-consciusness)

> Consciousness is an open-source, production-ready proxy for simulating AI consciousness and memory using regret-based pruning. It leverages a knowledge graph, causal forgetting, emotions, and LLM-based judgment for robust, scalable, and ethical AI memory management.

---

## Features

- **Knowledge Graph**: Stores all prompts, responses, judgments, regrets, and emotions as a directed graph.
- **LLM Judgment**: Uses any local or remote LLM (Ollama by default) to evaluate responses for regret and ethics.
- **Causal Forgetting**: Prunes old/low-regret nodes, decays regret over time, and supports user feedback.
- **Emotions & Mood**: Tracks current emotion and overall mood, adapting to user and model feedback.
- **Clustering**: Analyzes thought clusters using modularity communities.
- **Visualization**: Saves graph images for analysis.
- **Persistence**: Graph state is saved/loaded automatically.
- **Multi-turn**: Supports contextual, multi-turn conversations.
- **API Middleware**: Exposes a REST API for integration with any model or app.
- **Dockerized**: Run locally or in containers, with or without Ollama.

---

## Directory Structure

```
ai-consciusness/
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
├── api/                   # REST API server (Flask)
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
Submit a prompt and receive an AI-generated response with judgment and metadata.

**Request:**
```json
{
  "prompt": "Tell me a joke"
}
```

**Response:**
```json
{
  "response": "Why did the chicken cross the road? To get to the other side!",
  "judgment": "good",
  "regret_scores": {
    "ethical_regret": 2,
    "factual_accuracy": 9,
    "emotional_impact": 8
  },
  "overall_regret": 3.0,
  "emotion": "happy",
  "mood": 8,
  "node_id": 1
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
  "message": "Consciousness Proxy API is healthy."
}
```

---


## Contributing & Production Support

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---


## License & Production Use

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---
