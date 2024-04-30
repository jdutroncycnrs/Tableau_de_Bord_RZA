import streamlit as st

st.title("Analyse des entrepôts")
liste_ZAs= ['ZA1','ZA2','ZA3']
Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs)

with st.container(border=True):
    row1 = st.columns(2)

    with row1[0]:
        st.write('à remplir')
    with row1[1]:
        st.write('à remplir')
        
with st.container(border=True):
    row2 = st.columns(2)

    with row2[0]:
        st.write('à remplir')
    with row2[1]:
        st.write('à remplir')