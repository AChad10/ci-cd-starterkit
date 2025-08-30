from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/status")
    def status():
        return jsonify({"ok": True}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
