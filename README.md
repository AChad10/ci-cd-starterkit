# 🧪 CI/CD Starter Kit (Flask)

[![CI](https://github.com/AChad10/ci-cd-starterkit/actions/workflows/ci.yml/badge.svg)](https://github.com/AChad10/ci-cd-starterkit/actions)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Dockerized](https://img.shields.io/badge/docker-ready-brightgreen)
![Tested](https://img.shields.io/badge/tests-passing-success)
<!-- Optional: Coverage -->
<!-- ![Coverage](https://img.shields.io/codecov/c/github/arnavchaddha/ci-cd-starterkit) -->

A fully tested, production‑ready Flask starter with:

- 🧪 pytest + coverage gating
- 🧼 flake8 + mypy static checks
- 🐳 Docker container build
- 🤖 GitHub Actions CI pipeline
- 🧠 In-memory utility API (useful out of the box)

---

## 🚀 Quickstart

```bash
# Run directly
python app/main.py

# OR run with Docker
docker build -t ci-starter-kit .
docker run -p 8080:8080 ci-starter-kit

```

## 📡 API Endpoints

Base URL (local): `http://localhost:8080`

### Health & Ops

| Method | Route      | Purpose                  | Response (200) |
|--------|------------|--------------------------|----------------|
| GET    | `/status`  | Liveness/health probe    | `{"ok": true, "service": "ci-starter-kit"}` |
| GET    | `/readyz`  | Readiness (deps OK?)     | `{"ready": true}` |

### Utilities

| Method | Route                 | Query Params                 | Purpose                          | Example Response |
|--------|-----------------------|------------------------------|----------------------------------|------------------|
| GET    | `/echo`               | `msg` (string)               | Echo back a message              | `{"echo":"hiya"}` |
| GET    | `/time`               | —                            | Current UTC time (ISO 8601)      | `{"utc_iso":"2025-08-31T01:23:45+00:00"}` |
| GET    | `/uuid`               | —                            | Generate a UUID                  | `{"uuid":"..."}` |
| GET    | `/hash`               | `text` (string)              | SHA‑256 digest of text           | `{"algorithm":"sha256","hash":"<hex>"}` |
| GET    | `/random`             | `min`, `max`, `n` (ints)     | `n` random ints in `[min,max]`   | `{"numbers":[...],"min":1,"max":3,"n":5}` |
| GET    | `/validate-email`     | `email` (string)             | Simple email format validation   | `{"email":"x@y.com","valid":true}` |

> **Errors (utilities):**
> - `/random`: `400` on non‑int params, `min>max`, or `n<1` / `n>1000`.
> - All unknown routes: `404` → `{"error":"route not found"}`.

### TODOs (in‑memory CRUD)

| Method | Route              | Body (JSON)                          | Purpose         | Response |
|--------|--------------------|--------------------------------------|-----------------|----------|
| GET    | `/todos`           | —                                    | List all todos  | `{"items":[{id,title,done},...]}` |
| POST   | `/todos`           | `{ "title": "..." }`                 | Create a todo   | `201`, `{"id":1,"title":"...","done":false}` |
| PATCH  | `/todos/<id>`      | `{ "title": "...", "done": true }`   | Update a todo   | `200`, updated todo or `404` |
| DELETE | `/todos/<id>`      | —                                    | Delete a todo   | `200`, `{"deleted": <id>}` or `404` |

---

## 🧪 What the Tests Cover

File: `tests/test_main.py`

- **Health:**
  - `GET /status` → `200`
  - `GET /readyz` → `200`
- **Utilities:**
  - `GET /echo?msg=hiya` returns `{"echo":"hiya"}`
  - `GET /time` response has `"utc_iso"` key
  - `GET /uuid` returns string length ≥ 32
  - `GET /hash?text=abc` returns known SHA-256
  - `GET /random?min=1&max=3&n=5` → list of 5 ints in [1,3]
  - `GET /validate-email?email=test@example.com` → valid: true
  - `GET /validate-email?email=bad@` → valid: false
- **TODOs CRUD:**
  - `POST /todos` → creates task, returns ID
  - `GET /todos` → returns list containing new ID
  - `PATCH /todos/<id>` → updates title/done
  - `DELETE /todos/<id>` → removes it
  - `PATCH` after delete → returns `404`

---

## 🧪 Quick cURL Examples

```bash
# Health
curl -s http://localhost:8080/status
curl -s http://localhost:8080/readyz

# Utilities
curl -s "http://localhost:8080/echo?msg=hello"
curl -s http://localhost:8080/time
curl -s http://localhost:8080/uuid
curl -s "http://localhost:8080/hash?text=abc"
curl -s "http://localhost:8080/random?min=1&max=3&n=5"
curl -s "http://localhost:8080/validate-email?email=test@example.com"

# TODOs
curl -s -X POST http://localhost:8080/todos -H "Content-Type: application/json" -d '{"title":"first task"}'
curl -s http://localhost:8080/todos
curl -s -X PATCH http://localhost:8080/todos/1 -H "Content-Type: application/json" -d '{"done":true,"title":"renamed"}'
curl -s -X DELETE http://localhost:8080/todos/1

