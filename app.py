import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request, Response
from pydantic import BaseModel
import asyncpg

# --- Database Connection Management ---
db_pool: Optional[asyncpg.Pool] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool
    # Replace with your actual PostgreSQL connection string
    dsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/affiliate_db")
    db_pool = await asyncpg.create_pool(dsn)
    
    # Optional: Initialize tables for demonstration purposes
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS webhook_events (
                event_id VARCHAR(255) PRIMARY KEY,
                provider VARCHAR(50) NOT NULL,
                processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS user_credits (
                user_id VARCHAR(255) PRIMARY KEY,
                balance INTEGER DEFAULT 0
            );
        """)
    yield
    await db_pool.close()

app = FastAPI(lifespan=lifespan)

# --- Pydantic Models for Webhook Payloads ---
class StripeWebhookPayload(BaseModel):
    id: str
    type: str
    data: dict

# --- Webhook Endpoint ---
@app.post("/webhooks/stripe")
async def stripe_webhook(
    payload: StripeWebhookPayload,
    stripe_signature: str | None = Header(default=None)
):
    """
    Handles incoming Stripe webhooks idempotently.
    """
    # 1. Verify webhook signature (Omitted for brevity, but crucial in production)
    # verify_stripe_signature(payload, stripe_signature)

    event_id = payload.id
    provider = "stripe"
    
    # 2. Extract business data (e.g., user to credit)
    # In a real scenario, you'd extract this from payload.data['object']
    user_id = payload.data.get("object", {}).get("client_reference_id", "user_123")
    credit_amount = 100

    # 3. Open a Database Transaction
    if db_pool is None:
        raise HTTPException(status_code=500, detail="Database connection pool not initialized")

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            # 4. Attempt to insert the event_id. 
            # ON CONFLICT DO NOTHING ensures we don't crash on duplicates.
            # RETURNING event_id allows us to check if the insert actually happened.
            insert_query = """
                INSERT INTO webhook_events (event_id, provider)
                VALUES ($1, $2)
                ON CONFLICT (event_id) DO NOTHING
                RETURNING event_id;
            """
            result = await conn.fetchval(insert_query, event_id, provider)

            # 5. Check Idempotency
            if result is None:
                # The event_id was not returned, meaning the ON CONFLICT clause triggered.
                # This is a duplicate webhook. We return 200 OK immediately.
                print(f"Idempotency hit: Event {event_id} already processed.")
                return Response(status_code=200, content="Already processed")

            # 6. Process Business Logic
            # Since we are inside the transaction, if this fails, the webhook_events 
            # insert is rolled back, allowing future webhook retries to succeed.
            print(f"Processing new event: {event_id}")
            
            update_credits_query = """
                INSERT INTO user_credits (user_id, balance)
                VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE SET balance = user_credits.balance + $2;
            """
            await conn.execute(update_credits_query, user_id, credit_amount)

    # 7. Transaction commits automatically upon exiting the `async with conn.transaction():` block.
    return Response(status_code=200, content="Success")

