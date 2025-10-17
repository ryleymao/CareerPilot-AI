.PHONY: help build up down logs clean test

help:
	@echo "JobRight Clone - Make Commands"
	@echo "=============================="
	@echo "make build       - Build all Docker images"
	@echo "make up          - Start all services"
	@echo "make down        - Stop all services"
	@echo "make logs        - View logs"
	@echo "make clean       - Remove all containers and volumes"
	@echo "make test        - Run tests"
	@echo "make shell       - Open backend shell"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services starting..."
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Health: http://localhost:8000/health"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

test:
	docker-compose exec backend pytest tests/

shell:
	docker-compose exec backend bash

restart:
	docker-compose restart backend

status:
	docker-compose ps
