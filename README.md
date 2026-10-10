# Affiliate Program Tracking Tool

A micro-SaaS backend designed for SaaS founders to manage affiliate tracking and payouts with zero-percentage fees, direct batch payments, and cloud-native reliability. Built with Python, FastAPI, and PostgreSQL.

## Features
*   **Idempotent Webhooks:** Secure, transaction-backed webhook handling for Stripe and Paddle integrations to ensure zero duplicate attributions.
*   **Zero-Percentage Payout Architecture:** Flat-fee system design without scaling transaction penalties.
*   **Containerized Local Development:** Pre-configured Docker database setup for immediate local environment parity.
*   **Auto-scaling Ready:** Designed for Kubernetes deployment on AWS (ap-south-1).

## Prerequisites
*   Python 3.10+
*   Docker & Docker Compose (or Docker Desktop)
*   VS Code (recommended)

## Local Development Setup

### 1. Environment Setup
Clone the repository, create a virtual environment, and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install fastapi pydantic asyncpg asyncpg-stubs uvicorn[standard]