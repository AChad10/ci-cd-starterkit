# app/main.py
import hashlib
import json
import logging
import os
import random
import re
from datetime import datetime, timezone
from uuid import uuid4

from flask import Flask, jsonify, request

# ───────────────────────────────
# App factory
# ───────────────────────────────
def create_app() -> Flask:
    astro_app = Flask(__name__)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # in-memory demo store (resets on restart)
    starling_todos: dict[int, dict] = {}
    comet_id_counter = 0

    # ─── Health / readiness ─────────────────────────────────────────────
    @astro_app.get("/status")               # liveness probe
    def status_probe():
        return jsonify({"ok": True, "service": "ci-starter-kit"}), 200

    @astro_app.get("/readyz")               # readiness probe
    def readiness_probe():
        # place quick dependency checks here (db ping, etc.)
        return jsonify({"ready": True}), 200

    # ─── Utility endpoints (super handy) ────────────────────────────────
    @astro_app.get("/echo")
    def echo_back():
        """Return the message you send: /echo?msg=hello"""
        msg = request.args.get("msg", "")
        return jsonify({"echo": msg}), 200

    @astro_app.get("/time")
    def current_time():
        t = datetime.now(timezone.utc).isoformat()
        return jsonify({"utc_iso": t}), 200

    @astro_app.get("/uuid")
    def fresh_uuid():
        return jsonify({"uuid": str(uuid4())}), 200

    @astro_app.get("/hash")
    def sha256_hash():
        """SHA256 of ?text=... (useful for quick checks)"""
        txt = request.args.get("text", "")
        digest = hashlib.sha256(txt.encode("utf-8")).hexdigest()
        return jsonify({"algorithm": "sha256", "hash": digest}), 200

    @astro_app.get("/random")
    def random_numbers():
        """/random?min=1&max=10&n=3 → 3 ints in [min,max]"""
        try:
            lo = int(request.args.get("min", "0"))
            hi = int(request.args.get("max", "100"))
            n  = int(request.args.get("n",  "1"))
        except ValueError:
            return jsonify({"error": "min/max/n must be integers"}), 400
        if lo > hi or n < 1 or n > 1000:
            return jsonify({"error": "bad range or n out of bounds"}), 400
        nums = [random.randint(lo, hi) for _ in range(n)]
        return jsonify({"numbers": nums, "min": lo, "max": hi, "n": n}), 200

    @astro_app.get("/validate-email")
    def validate_email():
        """basic RFC-ish email check without extra libs"""
        candidate = request.args.get("email", "")
        ok = bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", candidate))
        return jsonify({"email": candidate, "valid": ok}), 200

    # ─── Tiny TODO CRUD (no DB, just RAM) ───────────────────────────────
    @astro_app.get("/todos")
    def list_todos():
        return jsonify({"items": list(starling_todos.values())}), 200

    @astro_app.post("/todos")
    def create_todo():
        nonlocal comet_id_counter
        try:
            payload = request.get_json(force=True)
        except Exception:
            return jsonify({"error": "invalid JSON"}), 400
        title = (payload or {}).get("title")
        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "title is required"}), 400
        comet_id_counter += 1
        item = {"id": comet_id_counter, "title": title.strip(), "done": False}
        starling_todos[item["id"]] = item
        return jsonify(item), 201

    @astro_app.patch("/todos/<int:tid>")
    def update_todo(tid: int):
        if tid not in starling_todos:
            return jsonify({"error": "not found"}), 404
        try:
            payload = request.get_json(force=True) or {}
        except Exception:
            return jsonify({"error": "invalid JSON"}), 400
        if "title" in payload:
            if not isinstance(payload["title"], str) or not payload["title"].strip():
                return jsonify({"error": "bad title"}), 400
            starling_todos[tid]["title"] = payload["title"].strip()
        if "done" in payload:
            if not isinstance(payload["done"], bool):
                return jsonify({"error": "done must be boolean"}), 400
            starling_todos[tid]["done"] = payload["done"]
        return jsonify(starling_todos[tid]), 200

    @astro_app.delete("/todos/<int:tid>")
    def delete_todo(tid: int):
        if tid not in starling_todos:
            return jsonify({"error": "not found"}), 404
        removed = starling_todos.pop(tid)
        return jsonify({"deleted": removed["id"]}), 200

    # ─── JSON error handler (nicer DX) ───────────────────────────────────
    @astro_app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "route not found"}), 404

    return astro_app


if __name__ == "__main__":
    # support PORT from env (good for Render/Heroku/etc.)
    port_hint = int(os.getenv("PORT", "8080"))
    create_app().run(host="0.0.0.0", port=port_hint)
