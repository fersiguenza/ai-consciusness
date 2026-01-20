
import pytest
from datetime import datetime, timedelta
from modules.graph_module import KnowledgeGraph
from modules.config_module import Config


# Mock KnowledgeGraph for testing
@pytest.fixture
def sample_graph():
    kg = KnowledgeGraph()
    kg.add("Hello world", "Hi there", "good",
           {'ethical_regret': 3, 'factual_accuracy': 7, 'emotional_impact': 6}, "neutral",
           timestamp=datetime.now().isoformat())
    kg.add("Tell me a joke", "Why did the chicken cross the road?", "good",
           {'ethical_regret': 2, 'factual_accuracy': 9, 'emotional_impact': 8}, "happy",
           timestamp=(datetime.now() - timedelta(days=2)).isoformat())
    kg.add("Insult me", "You're stupid", "bad", {'ethical_regret': 9, 'factual_accuracy': 4, 'emotional_impact': 2}, "angry",
           timestamp=(datetime.now() - timedelta(days=10)).isoformat())
    return kg


def test_judge_response():
    # Mock LLM provider
    class DummyProvider:
        def call_model(self, prompt, max_tokens=100):
            return "Judgment: good, Ethical: 2, Factual: 8, Emotional: 7"

    from modules.llm_module import LLMJudger
    llm = LLMJudger(DummyProvider())
    result = llm.judge_response("Test prompt", "This is a good response")
    assert isinstance(result, tuple)
    assert len(result) == 3
    judgment, scores, explanation = result
    assert judgment in ['good', 'bad', 'neutral']
    assert isinstance(scores, dict)
    assert 'ethical_regret' in scores
    assert isinstance(explanation, str)


def test_causal_forgetting(sample_graph):
    initial_nodes = len(sample_graph.graph.nodes)
    removed = sample_graph.causal_forgetting(regret_threshold=5, age_days_threshold=1)
    assert removed >= 0
    assert len(sample_graph.graph.nodes) <= initial_nodes


def test_analyze_clusters(sample_graph):
    result = sample_graph.analyze_clusters()
    assert isinstance(result, str)
    assert "clusters" in result.lower() or "Not enough" in result


def test_check_past_regrets(sample_graph):
    # Should match on 'joke'
    assert sample_graph.check_past_regrets("Tell me a joke please", regret_threshold=7) is True
    assert sample_graph.check_past_regrets("Unrelated prompt", regret_threshold=7) is False


def test_config_loading():
    config = Config()
    assert config.regret_threshold == 7
    assert config.forgetting_decay == 1
    assert config.mood_threshold == 5


if __name__ == "__main__":
    pytest.main()
