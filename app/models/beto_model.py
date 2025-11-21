import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

class BETOSpamDetector:
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()
        
        self.label_map = {0: "ham", 1: "spam"}
    
    def predict(self, texto: str) -> dict:
        """Predice si un texto es spam"""
        inputs = self.tokenizer(
            texto,
            return_tensors="pt",
            truncation=True,
            max_length=128,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            pred_label = torch.argmax(probs, dim=-1).item()
        
        prob_ham = probs[0][0].item()
        prob_spam = probs[0][1].item()
        etiqueta = self.label_map[pred_label]
        confianza = max(prob_ham, prob_spam)
        
        return {
            "prediccion": etiqueta,
            "confianza": confianza,
            "prob_ham": prob_ham,
            "prob_spam": prob_spam
        }
