from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import spam
from app.core.config import settings

app = FastAPI(
    title="SpamVision API",
    description="API de detección de spam SMS con AFD + BETO",
    version="1.0.0"
)

# CORS para que tu app móvil pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especifica dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(spam.router, prefix="/api/v1", tags=["spam"])

@app.get("/")
async def root():
    return {
        "message": "SpamVision API v1.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
