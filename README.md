# SysMon Microservices Platform

A modular system monitoring and feedback platform built with **FastAPI**, **React**, and **PostgreSQL** using a microservices architecture.

## 🔧 Features

- ✅ JWT Authentication and Role-Based Access Control (RBAC)
- ✅ Microservices for User, Feedback, and Metrics
- ✅ Central API Gateway with request routing and JWT verification
- ✅ React Admin Dashboard with user management and system status
- ✅ Docker-based deployment
- ✅ OpenAPI docs with secure Bearer token auth support
- ✅ Health & version endpoints for observability

## 🧱 Architecture

- `api_gateway/` - Routes external requests to appropriate microservices
- `user_service/` - Manages user registration, login, and roles
- `feedback_service/` - Handles feedback submissions and admin views
- `metrics_service/` - Provides system-level metrics and status
- `frontend/` - React-based admin dashboard (Role: admin, user, viewer)
- `docker-compose.yml` - Spins up the full system locally

## 🚀 Getting Started

```bash
git clone https://github.com/gupta55760/sysmon-microservices.git
cd sysmon-microservices
cp .env.example .env  # set your DB creds
docker-compose up --build
```

Access:

- Frontend: http://localhost:3000
- API Gateway: http://localhost:8080
- Swagger UI: http://localhost:8080/docs

## 📦 Tech Stack

- Python + FastAPI
- PostgreSQL
- React
- Docker
- Pytest (testing in progress)
- Playwright/Selenium (UI test automation – coming soon)

## 📌 Status

Actively in progress. This repo evolves from the earlier [sysmon-sdk](https://github.com/gupta55760/sysmon-sdk) project.

## 🧪 Upcoming

- Pytest-based API test suite
- Playwright UI test coverage
- CI/CD integration with GitHub Actions

