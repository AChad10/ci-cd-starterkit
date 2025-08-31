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
