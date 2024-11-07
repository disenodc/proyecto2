# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from gbif_utils import fetch_gbif_occurrence_data
from openai_utils import generate_insights

st.title("GBIF Occurrence Data Visualization Bot")

taxon_key = st.text_input("Enter Taxon Key:", value="212")  # Example taxon key
limit = st.number_input("Number of Occurrences to Fetch:", min_value=1, max_value=1000, value=100)

if st.button("Fetch Data"):
    gbif_data = fetch_gbif_occurrence_data(taxon_key, limit)
    st.write("Data fetched successfully!")

    # Mostrar datos en tabla
    df = pd.DataFrame(gbif_data['results'])
    st.dataframe(df[['species', 'country', 'eventDate', 'decimalLatitude', 'decimalLongitude']])

    # Generar insights con LLM
    insights = generate_insights(gbif_data)
    st.subheader("LLM Insights")
    st.write(insights)

    # Visualización de ubicaciones
    if not df.empty:
        fig = px.scatter_geo(df,
                             lat='decimalLatitude',
                             lon='decimalLongitude',
                             hover_name='species',
                             title="Geographical Distribution of Occurrences")
        st.plotly_chart(fig)
