from pydantic import BaseModel
from typing import Literal

class SpamResponse(BaseModel):
    id: str                                    # ID único del análisis
    mensaje: str                               # Mensaje analizado
    tipo: Literal["Spam", "No Spam"]          # Resultado final
    scoring: float                             # 0.0 - 1.0 (0% - 100%)
    
    # Detalles del AFD
    afd_resultado: str                         # "SPAM" o "NO-SPAM"
    afd_score: float
    
    # Detalles del modelo BETO
    beto_prediccion: str                       # "spam" o "ham"
    beto_confianza: float
    beto_prob_spam: float
    beto_prob_ham: float
    
    # Metadatos
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "MSG-abc123",
                "mensaje": "Ganaste un premio gratis",
                "tipo": "Spam",
                "scoring": 0.92,
                "afd_resultado": "SPAM",
                "afd_score": 6.5,
                "beto_prediccion": "spam",
                "beto_confianza": 0.95,
                "beto_prob_spam": 0.95,
                "beto_prob_ham": 0.05,
                "timestamp": "2025-11-20T22:43:00"
            }
        }
