
from modules.graph_module import KnowledgeGraph
from modules.llm_module import LLMJudger
from modules.emotion_module import update_emotion, update_mood
from modules.config_module import Config
from rich.console import Console
import matplotlib.pyplot as plt
import networkx as nx
import signal
import sys

console = Console()
config = Config()
graph = KnowledgeGraph()
llm_provider = config.create_llm_provider()
llm = LLMJudger(llm_provider)
regret_threshold = config.regret_threshold
forgetting_decay = config.forgetting_decay
mood_threshold = config.mood_threshold


def signal_handler(sig, frame):
    console.print("\nSaving graph and exiting...", style="yellow")
    graph.save()
    sys.exit(0)


# Example CLI entrypoint
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    console.print("🧠 Consciousness AI POC (Modular) 🧠", style="bold magenta", justify="center")

    while True:
        prompt = input("Enter prompt (or 'exit'): ")
        if prompt.lower() == 'exit':
            graph.save()
            break
        ai_response = llm.call_model(prompt)
        judgment, scores, explanation = llm.judge_response(prompt, ai_response)
        overall_regret = (scores['ethical_regret'] + (10 - scores['factual_accuracy']) + (10 - scores['emotional_impact'])) / 3
        emotion = update_emotion(judgment, int(overall_regret))
        node_id = graph.add(prompt, ai_response, judgment, scores, emotion)
        avg_regret = sum((data.get('regret_scores', {}).get('ethical_regret', 5) +
                          (10 - data.get('regret_scores', {}).get('factual_accuracy', 5)) +
                          (10 - data.get('regret_scores', {}).get('emotional_impact', 5))) / 3
                         for n in graph.graph.nodes for data in [graph.graph.nodes[n]]) / len(graph.graph.nodes)
        mood = update_mood(avg_regret, mood_threshold)

        console.print(f"AI: {ai_response}")
        console.print(f"Judgment: {judgment}, Scores: {scores}, Overall Regret: {overall_regret:.1f}, "
                      f"Emotion: {emotion}, Mood: {mood}")


def causal_forgetting():
    """Advanced forgetting: Decay regrets over time and prune low-importance nodes."""
    from datetime import datetime
    current_time = datetime.now()
    to_decay = []
    to_prune = []
    for node in graph.graph.nodes:
        data = graph.graph.nodes[node]
        age_days = (current_time - datetime.fromisoformat(data['timestamp'])).days
        # Decay regret: reduce by forgetting_decay per day, but not below 1
        if age_days > 0:
            data['regret_score'] = max(1, data['regret_score'] - forgetting_decay * age_days)
            to_decay.append(node)
        # Prune if regret < regret_threshold and age > 7 days, or low connectivity
        connectivity = len(list(graph.graph.neighbors(node)))
        if data['regret_score'] < regret_threshold and (age_days > 7 or connectivity < 1):
            to_prune.append(node)
    for node in to_prune:
        graph.graph.remove_node(node)
    if to_decay or to_prune:
        console.print(f"Decayed {len(to_decay)} nodes, pruned {len(to_prune)}.", style="dim")


def analyze_clusters():
    """Analyze graph clusters using modularity communities."""
    from networkx.algorithms.community import greedy_modularity_communities
    if len(graph.graph.nodes) < 2:
        return "Not enough nodes for clustering."
    communities = list(greedy_modularity_communities(graph.graph))
    num_clusters = len(communities)
    cluster_sizes = [len(c) for c in communities]
    # Describe clusters
    descriptions = []
    for i, comm in enumerate(communities):
        regrets = [graph.graph.nodes[n].get('regret_score', 5) for n in comm]
        avg_regret = sum(regrets) / len(regrets) if regrets else 0
        descriptions.append(f"Cluster {i+1}: {len(comm)} nodes, avg regret {avg_regret:.1f}")
    return f"Clusters: {num_clusters} | Sizes: {cluster_sizes} | Details: {' | '.join(descriptions)}"


def check_past_regrets(prompt):
    """Check if prompt resembles high-regret past interactions."""
    high_regret_nodes = [n for n in graph.graph.nodes if graph.graph.nodes[n].get('regret_score', 0) > regret_threshold]
    for node in high_regret_nodes:
        past_prompt = graph.graph.nodes[node]['prompt']
        # Simple keyword overlap check
        past_words = set(w.lower() for w in past_prompt.split() if len(w) > 3)
        prompt_words = set(w.lower() for w in prompt.split() if len(w) > 3)
        if past_words & prompt_words:  # Intersection
            return True
    return False


def visualize_graph():
    """Visualize and save the knowledge graph."""
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph.graph)
    node_colors = ['red' if graph.graph.nodes[n].get('regret_score', 0) > 7 else 'lightblue' for n in graph.graph.nodes]
    labels = {n: graph.graph.nodes[n]['prompt'][:20] +
              ('...' if len(graph.graph.nodes[n]['prompt']) > 20 else '')
              for n in graph.graph.nodes}
    nx.draw(graph.graph, pos, labels=labels, node_color=node_colors, font_size=8, node_size=500)
    plt.title("Consciousness Knowledge Graph (Red: High Regret)")
    plt.savefig('graphs/graph.png')
    console.print("Graph visualization saved as graphs/graph.png", style="green")
