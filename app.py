
from flask import Flask, render_template, request, jsonify
from server import TCPServer
import socket

app = Flask(__name__)

tcp_server = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_server():
    global tcp_server

    try:
        if tcp_server and tcp_server.running:
            return jsonify({"message": "Server already running"})

        host = request.json.get("host", "0.0.0.0")
        port = int(request.json.get("port", 22222))

        tcp_server = TCPServer(host, port)
        tcp_server.start()

        return jsonify({"message": f"Server started on port {port}"})

    except OSError as e:
        return jsonify({"message": str(e)}), 400

@app.route("/stop", methods=["POST"])
def stop_server():
    global tcp_server

    if tcp_server:
        tcp_server.stop()
        tcp_server = None

    return jsonify({"message": "Server stopped"})

@app.route("/status")
def status():
    return jsonify({
        "running": bool(tcp_server and tcp_server.running),
        "port": tcp_server.port if tcp_server else None
    })

@app.route("/test", methods=["POST"])
def test_connection():
    data = request.json
    host = data.get("host", "127.0.0.1")
    port = int(data.get("port", 22222))
    message = data.get("message", "Hello Python!")

    try:
        with socket.create_connection(
            (host, port), timeout=3
        ) as client:
            client.sendall(message.encode("utf-8"))
            response = client.recv(2048).decode(
                "utf-8", errors="replace"
            )

        return jsonify({"response": response})

    except OSError as e:
        return jsonify({"response": str(e)}), 400

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
