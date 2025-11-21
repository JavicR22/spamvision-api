from pydantic import BaseModel, Field

class SMSRequest(BaseModel):
    mensaje: str = Field(..., min_length=1, max_length=500, description="Mensaje SMS a analizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "¡FELICIDADES! Ganaste un premio. Haz clic aquí: http://spam.com"
            }
        }
