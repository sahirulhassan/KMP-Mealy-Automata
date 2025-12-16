from flask import Flask, request, jsonify, send_from_directory
import graphviz
import base64
from kmp import KMPString, compute_lps

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/contains', methods=['POST'])
def contains():
    data = request.get_json()
    try:
        kmp = KMPString(data['text'])
        return jsonify({'contains': kmp.contains(data['pattern'])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/count', methods=['POST'])
def count():
    data = request.get_json()
    try:
        kmp = KMPString(data['text'])
        return jsonify({'count': kmp.count(data['pattern'])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/visualize', methods=['POST'])
def visualize():
    pattern = request.get_json().get('pattern', '')
    if not pattern:
        return jsonify({'error': 'Pattern required'}), 400

    if set(pattern).issubset({'a', 'b'}):
        alphabet = ['a', 'b']
    elif set(pattern).issubset({'0', '1'}):
        alphabet = ['0', '1']
    else:
        return jsonify({'error': 'Invalid characters'}), 400

    lps = compute_lps(pattern)
    m = len(pattern)

    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    dot.node('start', shape='point')
    dot.edge('start', '0')

    for i in range(m + 1):
        dot.node(str(i), shape='doublecircle' if i == m else 'circle')

    for state in range(m + 1):
        for sym in alphabet:
            if state < m and pattern[state] == sym:
                ns = state + 1
            else:
                fallback = state
                while fallback > 0 and (fallback == m or pattern[fallback] != sym):
                    fallback = lps[fallback - 1]
                ns = fallback

            out = 1 if ns == m else 0
            dot.edge(str(state), str(ns), label=f"{sym}/{out}")

    png = dot.pipe(format='png')
    b64 = base64.b64encode(png).decode()

    return jsonify({'image': f"data:image/png;base64,{b64}"})


if __name__ == '__main__':
    app.run(debug=True)
