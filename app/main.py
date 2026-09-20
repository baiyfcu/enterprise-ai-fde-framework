from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Enterprise AI FDE Framework MVP",
    description="Mock-first 企业 AI 落地工作流原型",
    version="0.1.0",
)
app.include_router(router, prefix="/api")
