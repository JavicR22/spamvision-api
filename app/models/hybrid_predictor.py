# app/models/hybrid_predictor.py
import uuid
from datetime import datetime
from app.models.afd_filter import PrefilterAFDwithScoreRobust
from app.models.beto_model import BETOSpamDetector

class HybridSpamPredictor:
    def __init__(self, afd_patterns_path: str, beto_model_path: str):
        self.afd = PrefilterAFDwithScoreRobust(pattern_file=afd_patterns_path)
        self.beto = BETOSpamDetector(model_path=beto_model_path)
    
    def predict(self, mensaje: str) -> dict:
        """
        Pipeline híbrido:
        1. AFD primero (rápido)
        2. BETO después (preciso)
        3. Combinar resultados
        """
        # 1. Resultado del AFD
        afd_resultado = self.afd.process(mensaje, debug=False)
        afd_score = self._calcular_afd_score(mensaje)
        
        # 2. Resultado del BETO
        beto_resultado = self.beto.predict(mensaje)
        
        # 3. Decisión final (CORREGIDO)
        # scoring debe ser la probabilidad de SPAM (no de ham)
        prob_spam = beto_resultado["prob_spam"]
        prob_ham = beto_resultado["prob_ham"]
        
        # Determinar tipo final basado en ambos modelos
        if afd_resultado == "SPAM" and beto_resultado["prediccion"] == "spam":
            # Ambos dicen spam: alta confianza
            tipo_final = "Spam"
            scoring = prob_spam  # ← Usar probabilidad de spam
        elif afd_resultado == "NO-SPAM" and beto_resultado["prediccion"] == "ham":
            # Ambos dicen ham: baja confianza de spam
            tipo_final = "No Spam"
            scoring = prob_spam  # ← Probabilidad de spam (será baja, 0.01)
        else:
            # Conflicto: confiar más en BETO
            if beto_resultado["prediccion"] == "spam":
                tipo_final = "Spam"
                scoring = prob_spam
            else:
                tipo_final = "No Spam"
                scoring = prob_spam  # ← Será bajo si es ham
        
        return {
            "id": f"MSG-{uuid.uuid4().hex[:8]}",
            "mensaje": mensaje,
            "tipo": tipo_final,
            "scoring": round(scoring, 3),  # ← Siempre probabilidad de spam
            "afd_resultado": afd_resultado,
            "afd_score": round(afd_score, 2),
            "beto_prediccion": beto_resultado["prediccion"],
            "beto_confianza": round(beto_resultado["confianza"], 3),
            "beto_prob_spam": round(prob_spam, 3),
            "beto_prob_ham": round(prob_ham, 3),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calcular_afd_score(self, mensaje: str) -> float:
        """
        Calcula score numérico del AFD basado en el scoring interno
        Puedes obtenerlo del AFD si expones el score
        """
        # Por ahora retorna un placeholder
        # Idealmente, modificarías el AFD para que retorne el score numérico
        return 5.0
