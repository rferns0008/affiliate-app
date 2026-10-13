# Affiliate Program Tracking Tool

A micro-SaaS backend designed for SaaS founders to manage affiliate tracking and payouts with zero-percentage fees, direct batch payments, and cloud-native reliability. Built with Python, FastAPI, and PostgreSQL.

## Features

* **Idempotent Webhooks:** Secure, transaction-backed webhook handling for Stripe and Paddle integrations to ensure zero duplicate attributions.
* **Zero-Percentage Payout Architecture:** Flat-fee system design without scaling transaction penalties.
* **Containerized Local Development:** Pre-configured Docker database setup for immediate local environment parity.
* **Auto-scaling Ready:** Designed for Kubernetes deployment on AWS (ap-south-1).

## Prerequisites

* Python 3.10+
* Docker & Docker Compose (or Docker Desktop)
* VS Code (recommended)

## Local Development Setup

### 1. Environment Setup

Clone the repository, create a virtual environment, and install the dependencies:

    python -m venv .venv
    source .venv/bin/activate
    pip install fastapi pydantic asyncpg asyncpg-stubs uvicorn[standard]

### 2. Database Initialization

Spin up the local PostgreSQL container with a persistent volume to ensure your data survives container restarts:

    docker run -d \
      --name affiliate-db \
      -e POSTGRES_PASSWORD=postgres \
      -v $(pwd)/pg-data:/var/lib/postgresql \
      -p 5432:5432 \
      postgres:latest

Create the application database inside the running container:

    docker exec -it affiliate-db psql -U postgres -c "CREATE DATABASE affiliate_db;"

### 3. Run the Application

Start the FastAPI development server:

    uvicorn app:app --reload

## API Documentation

Once the application is running, FastAPI automatically generates interactive API documentation.

* **Swagger UI:** <http://127.0.0.1:8000/docs>
* **ReDoc:** <http://127.0.0.1:8000/redoc>

Use the Swagger UI to test endpoints and simulate incoming webhooks directly from your browser.
