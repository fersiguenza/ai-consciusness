from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from modules.graph_module import KnowledgeGraph
from modules.llm_module import LLMJudger
from modules.emotion_module import update_emotion, update_mood
from modules.config_module import Config

app = Flask(__name__)

# Rate limiting: 10 requests per minute per IP
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

config = Config()
graph = KnowledgeGraph()
llm = LLMJudger(config.ollama_url, config.model)
regret_threshold = config.regret_threshold
forgetting_decay = config.forgetting_decay
mood_threshold = config.mood_threshold

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring and readiness probes."""
    return jsonify({"status": "ok", "message": "Consciousness Proxy API is healthy."})

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with friendly info message."""
    return (
        "<h2>Consciousness Proxy API</h2>"
        "<p>Welcome! The API is running.<br>"
        "See <a href='https://github.com/fersiguenza/ai-consciusness'>project docs</a> for usage.</p>"
        "<ul>"
        "<li>POST /prompt</li>"
        "<li>GET /graph</li>"
        "<li>GET /clusters</li>"
        "<li>GET /config</li>"
        "<li>POST /forget</li>"
        "<li>GET /health</li>"
        "</ul>"
    ), 200, {"Content-Type": "text/html"}

@app.route('/prompt', methods=['POST'])
@limiter.limit("5 per minute")  # Stricter limit for prompt endpoint
def handle_prompt():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    ai_response = llm.call_model(prompt)
    judgment, regret, explanation = llm.judge_response(prompt, ai_response)
    emotion = update_emotion(judgment, regret)
    node_id = graph.add(prompt, ai_response, judgment, regret, emotion)
    avg_regret = sum(graph.graph.nodes[n].get('regret_score', 5) for n in graph.graph.nodes) / len(graph.graph.nodes)
    mood = update_mood(avg_regret)
    return jsonify({
        'response': ai_response,
        'judgment': judgment,
        'regret': regret,
        'emotion': emotion,
        'mood': mood,
        'node_id': node_id
    })

@app.route('/graph', methods=['GET'])
def get_graph():
    nodes = [{**graph.graph.nodes[n], 'id': n} for n in graph.graph.nodes]
    edges = list(graph.graph.edges)
    return jsonify({'nodes': nodes, 'edges': edges})

@app.route('/clusters', methods=['GET'])
def get_clusters():
    return jsonify({'clusters': graph.analyze_clusters()})

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(config.config)

@app.route('/forget', methods=['POST'])
@limiter.limit("2 per minute")  # Limit forgetting to prevent abuse
def forget():
    removed = graph.causal_forgetting(regret_threshold)
    return jsonify({'removed_nodes': removed})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)