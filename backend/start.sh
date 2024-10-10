#!/bin/sh
alembic -x db_url="postgresql+asyncpg://greenaden:test@${POSTGRES_HOST}/greenaden" upgrade head

uvicorn main:app --host 0.0.0.0 --port 8000