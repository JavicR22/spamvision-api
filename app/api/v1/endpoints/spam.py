from fastapi import APIRouter, HTTPException
from app.schemas.request import SMSRequest
from app.schemas.response import SpamResponse
from app.models.hybrid_predictor import HybridSpamPredictor
from app.core.config import settings

router = APIRouter()

# Inicializar predictor (se carga una vez al iniciar)
predictor = HybridSpamPredictor(
    afd_patterns_path=settings.AFD_PATTERNS_PATH,
    beto_model_path=settings.BETO_MODEL_PATH
)

@router.post("/analyze", response_model=SpamResponse)
async def analyze_sms(request: SMSRequest):
    """
    Analiza un mensaje SMS y determina si es spam.
    
    - **mensaje**: Texto del SMS a analizar
    """
    try:
        resultado = predictor.predict(request.mensaje)
        return SpamResponse(**resultado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar: {str(e)}")
