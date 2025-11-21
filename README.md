<div align="center">
  <h1>🛡️ SpamVision API</h1>
  <p>API REST para detección inteligente de spam SMS usando AFD + BETO</p>
  
  ![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
  ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
  ![PyTorch](https://img.shields.io/badge/PyTorch-2.1-orange?logo=pytorch)
  ![License](https://img.shields.io/badge/License-MIT-yellow)
</div>

---

## 📖 Descripción

**SpamVision API** es un backend de alto rendimiento que utiliza un sistema **híbrido de IA** para detectar mensajes SMS fraudulentos en español con una precisión superior al 95%. Combina un Autómata Finito Determinista (AFD) basado en reglas con un modelo BETO (BERT en español) fine-tuned en datasets de spam.

### 🎯 Problema que Resuelve

Los sistemas tradicionales de detección de spam fallan ante nuevas técnicas de fraude. SpamVision utiliza un enfoque de dos capas:
1. **Filtro AFD rápido** (< 10ms) - Reglas basadas en patrones conocidos
2. **Modelo BETO preciso** (< 200ms) - Deep learning para casos complejos

Esta arquitectura logra **alta precisión** manteniendo **baja latencia**.

### ✨ Características Principales

- 🤖 **Sistema Híbrido**: AFD + Modelo Transformer (BETO)
- ⚡ **Ultra Rápido**: Respuesta en menos de 300ms
- 🎯 **Alta Precisión**: >95% accuracy en dataset de prueba
- 📊 **Análisis Detallado**: Probabilidades y scores de ambos modelos
- 🔒 **Seguro**: Sin almacenamiento de datos personales
- 📚 **Documentación Interactiva**: Swagger UI integrado
- 🌐 **CORS Habilitado**: Listo para producción

---

## 🛠️ Tech Stack

### **Backend Framework**
- **FastAPI** 0.115 - Framework web asíncrono moderno
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pydantic** - Validación de datos con type hints

### **Machine Learning**
- **PyTorch** 2.1 - Framework de deep learning
- **Transformers** (Hugging Face) - Modelo BETO pre-entrenado
- **scikit-learn** - Métricas y preprocesamiento
- **pandas** - Manipulación de datos

### **Arquitectura**
- **AFD (Autómata Finito Determinista)** - Filtro basado en regex y patrones
- **BETO** - BERT en español fine-tuned en 3.8k mensajes
- **Híbrido** - Combinación de ambos para decisión final

---

## 📊 Arquitectura del Sistema




---

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python**: 3.11 o superior
- **pip**: 23.0 o superior
- **Git**: Para clonar el repositorio
- **4GB RAM**: Mínimo para cargar el modelo BETO

### Instalación Paso a Paso

#### 1. Clonar el repositorio

git clone https://github.com/JavicR22/spamvision-api.git
cd spamvision-api


#### 2. Crear entorno virtual

**Windows:**

python -m venv venv
venv\Scripts\activate


**Linux/Mac:**

python3 -m venv venv
source venv/bin/activate

#### 3. Instalar dependencias

pip install -r requirements.txt

#### 4. Descargar modelo BETO ⚠️

El modelo fine-tuned no está en el repositorio por su tamaño (~500 MB).

**Opción A: Desde Hugging Face (Recomendado)**

python download_model.py

**Estructura esperada:**

ml_artifacts/
├── diccionario.txt ✅ (incluido en repo)
└── beto_finetuned/ ⚠️ (descargar por separado)
├── config.json
├── pytorch_model.bin (~500 MB)
├── tokenizer_config.json
├── special_tokens_map.json
└── vocab.txt
## 📱 Aplicación Móvil

Esta API está diseñada para ser consumida por:

👉 **[SpamVision Android App](https://github.com/JavicR22/spamvision-android)**
