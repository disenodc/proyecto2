import os
import openai

openai.api_key_path = "apikey.txt"
GBIF_API_KEY = os.getenv("GBIF_API_KEY")  # Si es necesario para la autenticación


# Función para Consultar la API de GBIF
import requests

#https://api.gbif.org/v1/occurrence/search
def consulta_gbif(query):
    url = f"https://api.gbif.org/v1/ocurrence/search?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "No se pudo obtener datos de GBIF."}

# Interacción con el LLM
def consulta_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Especifica el modelo de LLM
        messages=[
            {"role": "system", "content": "Actúa como un experto en biodiversidad."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']

# INTEGRAR STREAMLIT

import streamlit as st

st.title("Chatbot de Biodiversidad")

user_input = st.text_input("Escribe tu consulta:")

if st.button("Consultar"):
    # Procesa la consulta con el LLM
    processed_query = consulta_llm(user_input)
    
    # Consulta la API de GBIF con el resultado del LLM
    gbif_data = consulta_gbif(processed_query)
    
    # Muestra los resultados
    if "error" in gbif_data:
        st.error(gbif_data["error"])
    else:
        st.write(gbif_data)
