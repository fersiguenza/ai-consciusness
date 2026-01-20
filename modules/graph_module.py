import networkx as nx
import pickle
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.centrality import betweenness_centrality
from datetime import datetime
import logging

from typing import Optional, Any


logger = logging.getLogger(__name__)


class KnowledgeGraph:
    """Directed knowledge graph for storing prompts, responses, judgments, regrets, and emotions."""
    def __init__(self) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()

    def add(self, prompt: str, response: str, judgment: str, regret_score: int, emotion: str,
            timestamp: Optional[str] = None) -> int:
        """Add a new node to the graph."""
        node_id = len(self.graph.nodes) + 1
        self.graph.add_node(node_id, prompt=prompt, response=response, judgment=judgment,
                            regret_score=regret_score, emotion=emotion,
                            timestamp=timestamp or datetime.now().isoformat())
        if node_id > 1:
            self.graph.add_edge(node_id-1, node_id)
        logger.info(f"Added node {node_id} with regret {regret_score}")
        return node_id

    def save(self, path: str = 'graphs/graph.pkl') -> None:
        """Save the graph to disk."""
        with open(path, 'wb') as f:
            pickle.dump(self.graph, f)

    def load(self, path: str = 'graphs/graph.pkl') -> bool:
        """Load the graph from disk."""
        try:
            with open(path, 'rb') as f:
                self.graph = pickle.load(f)
            return True
        except Exception:
            return False

    def visualize(self, out_path: str = 'graphs/graph.png') -> None:
        """Save a visualization of the graph as a PNG image."""
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        node_colors = ['red' if self.graph.nodes[n].get('regret_score', 0) > 7 else 'lightblue'
                       for n in self.graph.nodes]
        labels = {n: self.graph.nodes[n]['prompt'][:20] +
                  ('...' if len(self.graph.nodes[n]['prompt']) > 20 else '')
                  for n in self.graph.nodes}
        nx.draw(self.graph, pos, labels=labels, node_color=node_colors, font_size=8, node_size=500)
        plt.title("Consciousness Knowledge Graph (Red: High Regret)")
        plt.savefig(out_path)

    def analyze_clusters(self) -> Any:
        """Analyze graph clusters using modularity communities."""
        if len(self.graph.nodes) < 2:
            return "Not enough nodes for clustering."
        communities = list(greedy_modularity_communities(self.graph))
        num_clusters = len(communities)
        return f"Found {num_clusters} clusters. Sizes: {[len(c) for c in communities]}"

    def causal_forgetting(self, regret_threshold: int = 3, age_days_threshold: int = 7) -> int:
        """Advanced causal forgetting: Prune low-regret, low-centrality nodes considering graph structure."""
        if len(self.graph.nodes) < 2:
            return 0  # Not enough nodes for meaningful forgetting

        current_time = datetime.now()
        to_prune = []

        # Calculate betweenness centrality for importance
        centrality = betweenness_centrality(self.graph)

        for node in list(self.graph.nodes):
            data = self.graph.nodes[node]
            age_days = (current_time - datetime.fromisoformat(data['timestamp'])).days
            regret = data['regret_score']
            importance = centrality.get(node, 0)

            # Prune if: low regret AND (old OR low importance OR isolated)
            connectivity = len(list(self.graph.neighbors(node)))
            if regret < regret_threshold and (age_days > age_days_threshold or importance < 0.01 or connectivity < 1):
                to_prune.append(node)

        for node in to_prune:
            self.graph.remove_node(node)
        logger.info(f"Pruned {len(to_prune)} nodes via causal forgetting")
        return len(to_prune)

    def check_past_regrets(self, prompt: str, regret_threshold: int = 7) -> Any:
        high_regret_nodes = [n for n in self.graph.nodes
                             if self.graph.nodes[n].get('regret_score', 0) > regret_threshold]
        for node in high_regret_nodes:
            past_prompt = self.graph.nodes[node]['prompt']
            past_words = set(w.lower() for w in past_prompt.split() if len(w) > 3)
            prompt_words = set(w.lower() for w in prompt.split() if len(w) > 3)
            if past_words & prompt_words:
                return True
        return False
