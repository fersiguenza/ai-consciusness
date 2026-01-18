


# Remorse: AI Consciousness via Regret Pruning

<!-- Badges -->
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/github/license/fersiguenza/ai-consciusness)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Issues](https://img.shields.io/github/issues/fersiguenza/ai-consciusness)

> Remorse is an open-source, production-ready proxy for simulating AI consciousness and memory using regret-based pruning. It leverages a knowledge graph, causal forgetting, emotions, and LLM-based judgment for robust, scalable, and ethical AI memory management.

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
conciusness/
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
Edit `config.yaml` to set your model, thresholds, and LLM endpoint:

```yaml
model: "llama2"
regret_threshold: 7
forgetting_decay: 1
mood_threshold: 5
ollama_url: "http://localhost:11434/api/generate"
```


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


## API Endpoints (Stable)

- `POST /prompt` — Submit a prompt, get AI response, judgment, regret, emotion, mood, and node ID
- `GET /graph` — Get all nodes and edges
- `GET /clusters` — Get cluster analysis
- `GET /config` — Get current config
- `POST /forget` — Trigger causal forgetting

---


## Contributing & Production Support

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---


## License & Production Use

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---
