import pytest
from fastapi.testclient import TestClient
from api.api_server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_config(client):
    resp = client.get('/v1/config')
    assert resp.status_code == 200
    assert 'regret_threshold' in resp.json


def test_get_graph(client):
    resp = client.get('/v1/graph')
    assert resp.status_code == 200
    assert 'nodes' in resp.json and 'edges' in resp.json


def test_get_clusters(client):
    resp = client.get('/v1/clusters')
    assert resp.status_code == 200
    assert 'clusters' in resp.json


def test_forget(client):
    resp = client.post('/v1/forget', headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})
    assert resp.status_code == 200
    assert 'removed_nodes' in resp.json


def test_prompt_endpoint(client, monkeypatch):
    # Patch LLM and graph to avoid real LLM calls

    class DummyLLM:
        async def call_model_async(self, prompt, max_tokens=100):
            return "Test response"

        async def judge_response_async(self, prompt, response):
            return ("good",
                    {'ethical_regret': 2, 'factual_accuracy': 8, 'emotional_impact': 7},
                    "Judgment: good, Ethical: 2, Factual: 8, Emotional: 7")

    from api import api_server
    api_server.llm = DummyLLM()
    api_server.graph = api_server.KnowledgeGraph()
    data = {"prompt": "Hello"}
    resp = client.post('/v1/prompt', json=data, headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})  # admin:secret
    assert resp.status_code == 200
    assert 'response' in resp.json
    assert 'judgment' in resp.json
    assert 'regret_scores' in resp.json
    assert 'overall_regret' in resp.json
    assert 'emotion' in resp.json
    assert 'mood' in resp.json
    assert 'node_id' in resp.json
