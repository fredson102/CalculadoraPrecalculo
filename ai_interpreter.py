"""
AI Interpreter - Usa DeepSeek para interpretar problemas matemáticos
"""
import os
import json
try:
    import requests
except ImportError:
    requests = None


class AIInterpreter:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.enabled = bool(self.api_key and requests)
    
    def interpret_problem(self, user_input: str) -> str:
        """
        Interpreta un problema matemático en lenguaje natural y lo convierte
        al formato que entiende el solver.
        
        Returns:
            str: Problema en formato matemático estándar
        """
        if not self.enabled:
            # Si no hay API key, devolver el input original
            return user_input
        
        prompt = f"""Eres un asistente matemático. Convierte el siguiente problema a notación matemática estándar.

REGLAS:
- Ecuaciones: formato "expresion = expresion" (ej: "2*x + 5 = 17")
- Derivadas: formato "deriv: expresion" (ej: "deriv: x^3 + 2*x^2")
- Integrales: formato "integral: expresion" (ej: "integral: x^2 + 3*x")
- Límites: formato "limit: expresion, x->valor" (ej: "limit: (x^2-1)/(x-1), x->1")
- Factorización: formato "factor: expresion" (ej: "factor: x^2 - 9")
- Expansión: formato "expand: expresion" (ej: "expand: (x+2)*(x-3)")
- Simplificación: formato "simplify: expresion" (ej: "simplify: (x^2-4)/(x-2)")
- Media: formato "mean: números" (ej: "mean: 5,10,15,20")
- Varianza: formato "var: números" (ej: "var: 2,4,6,8")
- Desviación estándar: formato "stddev: números" (ej: "stddev: 1,2,3,4")

IMPORTANTE:
- Usa * para multiplicación
- Usa ^ para exponentes
- Usa / para división
- No uses símbolos especiales como °, ×, ÷, ², ³
- Devuelve SOLO la expresión matemática, sin explicaciones

Problema del usuario: {user_input}

Expresión matemática:"""

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "Eres un experto en matemáticas que convierte problemas a notación estándar."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 200
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                interpreted = result['choices'][0]['message']['content'].strip()
                # Limpiar la respuesta
                interpreted = interpreted.replace('```', '').replace('`', '').strip()
                return interpreted
            else:
                # Si falla la API, devolver input original
                return user_input
                
        except Exception as e:
            # Si hay cualquier error, devolver input original
            print(f"AI Interpreter error: {e}")
            return user_input
    
    def set_api_key(self, api_key: str):
        """Establece la API key de DeepSeek"""
        self.api_key = api_key
        self.enabled = bool(self.api_key and requests)
