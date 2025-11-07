.PHONY: help install-backend install-frontend dev-backend dev-frontend build-backend build-frontend test-backend test-frontend docker-build docker-up docker-down clean

help:
	@echo "txtai RAG System - Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make dev-backend        - Run backend dev server"
	@echo "  make dev-frontend       - Run frontend dev server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - Build all Docker images"
	@echo "  make docker-up          - Start services with docker-compose"
	@echo "  make docker-down        - Stop docker-compose services"
	@echo ""
	@echo "Testing:"
	@echo "  make test-backend       - Run backend tests"
	@echo "  make test-frontend      - Run frontend tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean              - Remove build artifacts"

install-backend:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm run dev

build-backend:
	cd backend && docker build -t txtai-rag-backend .

build-frontend:
	cd frontend && docker build -t txtai-rag-frontend .

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

test-backend:
	cd backend && source venv/bin/activate && pytest

test-frontend:
	cd frontend && npm test

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	cd frontend && rm -rf node_modules dist

