import streamlit as st

st.title("Analyse des entrepôts")

liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)