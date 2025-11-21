from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Rutas de modelos
    AFD_PATTERNS_PATH: str = "ml_artifacts/diccionario.txt"
    BETO_MODEL_PATH: str = "ml_artifacts/resultados_beto_spam"
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpamVision API"
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
