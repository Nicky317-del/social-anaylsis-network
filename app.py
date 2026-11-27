
from flask import Flask, render_template, request, jsonify
from graph import SocialNetwork
from algorithms import shortest_path
from recommendations import mutual_friends, recommend_friends
from performance import performance_analysis

import io
from contextlib import redirect_stdout


app = Flask(__name__)

# Create social network
network = SocialNetwork()


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# DISPLAY NETWORK
# ==========================================

@app.route("/api/network", methods=["GET"])
def get_network():
    return jsonify(network.graph)


# ==========================================
# ADD USER
# ==========================================

@app.route("/api/add-user", methods=["POST"])
def add_user():

    data = request.get_json()
    user = data.get("user", "").strip()

    if not user:
        return jsonify({"error": "Enter a user name"}), 400

    if user in network.graph:
        return jsonify({"error": "User already exists"}), 400

    network.graph[user] = []

    return jsonify({
        "message": user + " added successfully!"
    })


# ==========================================
# ADD CONNECTION
# ==========================================

@app.route("/api/add-connection", methods=["POST"])
def add_connection():

    data = request.get_json()

    user1 = data.get("user1", "").strip()
    user2 = data.get("user2", "").strip()

    if user1 not in network.graph or user2 not in network.graph:
        return jsonify({"error": "Both users must exist"}), 404

    if user1 == user2:
        return jsonify({
            "error": "A user cannot connect to themselves"
        }), 400

    if user2 in network.graph[user1]:
        return jsonify({"error": "Connection already exists"}), 400

    network.graph[user1].append(user2)
    network.graph[user2].append(user1)

    return jsonify({
        "message": "Connection added successfully!"
    })


# ==========================================
# BFS TRAVERSAL
# ==========================================

@app.route("/api/bfs", methods=["POST"])
def run_bfs():

    data = request.get_json()
    start = data.get("user", "").strip()

    if start not in network.graph:
        return jsonify({"error": "User not found"}), 404

    visited = set()
    queue = [start]
    visited.add(start)
    result = []

    while queue:

        user = queue.pop(0)
        result.append(user)

        for friend in network.graph[user]:

            if friend not in visited:
                visited.add(friend)
                queue.append(friend)

    return jsonify({"result": result})


# ==========================================
# DFS TRAVERSAL
# ==========================================

@app.route("/api/dfs", methods=["POST"])
def run_dfs():

    data = request.get_json()
    start = data.get("user", "").strip()

    if start not in network.graph:
        return jsonify({"error": "User not found"}), 404

    visited = set()
    result = []

    def visit(user):

        visited.add(user)
        result.append(user)

        for friend in network.graph[user]:

            if friend not in visited:
                visit(friend)

    visit(start)

    return jsonify({"result": result})


# ==========================================
# MUTUAL FRIENDS
# ==========================================

@app.route("/api/mutual-friends", methods=["POST"])
def get_mutual_friends():

    data = request.get_json()

    user1 = data.get("user1", "").strip()
    user2 = data.get("user2", "").strip()

    if user1 not in network.graph or user2 not in network.graph:
        return jsonify({"error": "User not found"}), 404

    result = mutual_friends(network.graph, user1, user2)

    return jsonify({"result": result})


# ==========================================
# SHORTEST CONNECTION PATH
# ==========================================

@app.route("/api/shortest-path", methods=["POST"])
def get_shortest_path():

    data = request.get_json()

    start = data.get("start", "").strip()
    end = data.get("end", "").strip()

    if start not in network.graph or end not in network.graph:
        return jsonify({"error": "User not found"}), 404

    result = shortest_path(network.graph, start, end)

    return jsonify({"result": result})


# ==========================================
# FRIEND RECOMMENDATIONS
# ==========================================

@app.route("/api/recommendations", methods=["POST"])
def get_recommendations():

    data = request.get_json()
    user = data.get("user", "").strip()

    if user not in network.graph:
        return jsonify({"error": "User not found"}), 404

    result = recommend_friends(network.graph, user)

    return jsonify({"result": result})


# ==========================================
# PERFORMANCE ANALYSIS
# ==========================================

@app.route("/api/performance", methods=["GET"])
def run_performance():

    output = io.StringIO()

    with redirect_stdout(output):
        performance_analysis()

    return jsonify({
        "result": output.getvalue()
    })


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)
