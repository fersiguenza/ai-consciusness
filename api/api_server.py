from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from modules.graph_module import KnowledgeGraph
from modules.llm_module import LLMJudger
from modules.emotion_module import update_emotion, update_mood
from modules.config_module import Config

app = Flask(__name__)

# Basic auth
auth = HTTPBasicAuth()
users = {
    "admin": generate_password_hash("secret", method='pbkdf2:sha256')  # Change this in production
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


# Rate limiting: 10 requests per minute per IP
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)


config = Config()
graph = KnowledgeGraph()
llm_provider = config.create_llm_provider()
llm = LLMJudger(llm_provider)
regret_threshold = config.regret_threshold
forgetting_decay = config.forgetting_decay
mood_threshold = config.mood_threshold


@app.route('/v1/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring and readiness probes."""
    return jsonify({"status": "ok", "message": "Consciousness Proxy API is healthy."})


@app.route('/v1/', methods=['GET'])
def root():
    """Root endpoint with friendly info message."""
    return (
        "<h2>Consciousness Proxy API</h2>"
        "<p>Welcome! The API is running.<br>"
        "See <a href='https://github.com/fersiguenza/ai-consciousness'>project docs</a> for usage.</p>"
        "<ul>"
        "<li>POST /prompt</li>"
        "<li>GET /graph</li>"
        "<li>GET /clusters</li>"
        "<li>GET /config</li>"
        "<li>POST /forget</li>"
        "<li>GET /health</li>"
        "</ul>"
    ), 200, {"Content-Type": "text/html"}


@app.route('/v1/prompt', methods=['POST'])
@limiter.limit("5 per minute")  # Stricter limit for prompt endpoint
@auth.login_required
def handle_prompt():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    ai_response = llm.call_model(prompt)
    judgment, scores, explanation = llm.judge_response(prompt, ai_response)
    overall_regret = (scores['ethical_regret'] + (10 - scores['factual_accuracy']) + (10 - scores['emotional_impact'])) / 3
    emotion = update_emotion(judgment, int(overall_regret))
    node_id = graph.add(prompt, ai_response, judgment, scores, emotion)
    avg_regret = sum((data.get('regret_scores', {}).get('ethical_regret', 5) +
                      (10 - data.get('regret_scores', {}).get('factual_accuracy', 5)) +
                      (10 - data.get('regret_scores', {}).get('emotional_impact', 5))) / 3
                     for n in graph.graph.nodes for data in [graph.graph.nodes[n]]) / len(graph.graph.nodes)
    mood = update_mood(avg_regret)
    return jsonify({
        'response': ai_response,
        'judgment': judgment,
        'regret_scores': scores,
        'overall_regret': overall_regret,
        'emotion': emotion,
        'mood': mood,
        'node_id': node_id
    })


@app.route('/v1/graph', methods=['GET'])
def get_graph():
    nodes = [{**graph.graph.nodes[n], 'id': n} for n in graph.graph.nodes]
    edges = list(graph.graph.edges)
    return jsonify({'nodes': nodes, 'edges': edges})


@app.route('/v1/clusters', methods=['GET'])
def get_clusters():
    return jsonify({'clusters': graph.analyze_clusters()})


@app.route('/v1/config', methods=['GET'])
def get_config():
    return jsonify(config.config)


@app.route('/v1/forget', methods=['POST'])
@limiter.limit("2 per minute")  # Limit forgetting to prevent abuse
@auth.login_required
def forget():
    removed = graph.causal_forgetting(regret_threshold)
    return jsonify({'removed_nodes': removed})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
