import re
import pandas as pd

def clean_text(text):
    if not isinstance(text, str) or pd.isna(text):
        return ""
    
    # --- A. CARACTERES INVISIBLES Y VIÑETAS EXTRAÑAS ---
    text = text.replace('\xa0', ' ').replace('\t', ' ')
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Eliminar viñetas raras (símbolos unicode de Word/PDF)
    text = re.sub(r'[\uf02d\uf0a7\uf0b7•]', ' ', text)
    # Reemplazar comillas tipográficas y guiones especiales
    text = text.replace('“', '"').replace('”', '"').replace('‑', '-')
    
    # --- B. RUIDO DE FORMATO ---
    text = re.sub(r'_{2,}', ' ', text)
    text = re.sub(r'\.{3,}', '.', text)
    text = re.sub(r'-{2,}', ' ', text)
    text = text.replace('*', '')
    
    # --- C. COMILLAS Y NORMALIZACIÓN ---
    text = text.strip().strip('"').strip("'")
    text = text.replace('"', '')
    
    # --- D. PUNTUACIÓN INTELIGENTE ---
    # 1. Quitar espacios antes de puntuación
    text = re.sub(r'\s+([,.?;:])', r'\1', text)
    
    # 2. Añadir espacio tras comas, puntos y comas y dos puntos
    # Exclusión: no añadir si le sigue un número, espacio o slash (evita romper https://)
    text = re.sub(r'([,?;:])(?=[^\s\d/])', r'\1 ', text)
    
    # 3. Añadir espacio tras punto SOLO si le sigue mayúscula o corchete (evita D./Dña., 2.0)
    text = re.sub(r'\.(?=[A-ZÁÉÍÓÚ\[])', r'. ', text)
    
    # 4. Reparar URLs o correos dañados en procesamientos previos (si los hubiera)
    text = text.replace('https: //', 'https://').replace('http: //', 'http://')
    text = text.replace('. es', '.es').replace('. com', '.com').replace('. html', '.html')
    
    # --- E. ESPACIOS FINALES ---
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
