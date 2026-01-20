import pytest
from api.api_server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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
        def call_model(self, prompt):
            return "dummy response"

        def judge_response(self, prompt, response):
            return ("good", 2, "Judgment: Good\nRegret: 2")
    from api import api_server
    api_server.llm = DummyLLM()
    api_server.graph = api_server.KnowledgeGraph()
    data = {"prompt": "Hello"}
    resp = client.post('/v1/prompt', json=data, headers={'Authorization': 'Basic YWRtaW46c2VjcmV0'})  # admin:secret
    assert resp.status_code == 200
    assert 'response' in resp.json
    assert 'judgment' in resp.json
    assert 'regret' in resp.json
    assert 'emotion' in resp.json
    assert 'mood' in resp.json
    assert 'node_id' in resp.json
