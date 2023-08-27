import streamlit as st
import pandas as pd
import numpy as np
import time

from Utils.styles import title_style,paragraph_style

# Data 
entreprises = ["Pinot central","P II","PC","PH","PM","PL","P gourmet"]
all_data = pd.read_csv('./Data/data_pinot.csv')
st.session_state.selected_entreprise = None 

# Top Page
st.markdown(title_style, unsafe_allow_html=True)
st.markdown('<h1 class="title">Pinot Holding Dashboard</h1>', unsafe_allow_html=True)

st.markdown(paragraph_style, unsafe_allow_html=True)

st.divider()

# Side Bar

st.sidebar.markdown("""<p class="paragraph">Cette application permet de faciliter l\'analyse des entreprises de la holding Pinot</p>""", unsafe_allow_html=True)
st.sidebar.divider()
    
with st.sidebar:
    # Selection d'entreprise
    selected_entreprise = st.selectbox("Sélectionnez une entreprise", entreprises)

st.markdown(title_style, unsafe_allow_html=True)

container = st.empty()

if st.session_state.selected_entreprise == None:

    container.markdown('<h1 class="section-title">Veuillez séléctionner une entreprise à analyser </h1>', unsafe_allow_html=True)
    with st.sidebar:
        scrap_selected_entreprise = st.button(f'Collecter les données de {selected_entreprise}')

if scrap_selected_entreprise:
    with st.spinner(f'Collecte des données de l\'entrepise {selected_entreprise}...'):
        time.sleep(1.2)
        container.empty()
        container.markdown(f'<h1 class="section-title">Données de l\'entrepise {selected_entreprise} collectées !</h1>', unsafe_allow_html=True)
        st.session_state.selected_entreprise = selected_entreprise 

if st.session_state.selected_entreprise != None:

    tab1, tab2, tab3 = st.tabs(["Performance Mensuel", "Focus Google", "Focus Uber Eats"])
    spec_data = all_data[all_data.Entreprise == st.session_state.selected_entreprise]

    with tab1:
        col1, col2, col3 = st.columns(3)

        col1.metric("Score Google",
                    spec_data[spec_data.Mois == "2023-09-30"]["Score Google"], 
                    np.round(float(spec_data[spec_data.Mois == "2023-09-30"]["Score Google"].values - spec_data[spec_data.Mois == "2023-08-31"]["Score Google"]),2))
        col2.metric("Score Uber",
                    spec_data[spec_data.Mois == "2023-09-30"]["Score Uber"], 
                    np.round(float(spec_data[spec_data.Mois == "2023-09-30"]["Score Uber"].values - spec_data[spec_data.Mois == "2023-08-31"]["Score Uber"]),2))
        col3.metric("Nombre de commandes",
                    spec_data[spec_data.Mois == "2023-09-30"]["Commandes"], 
                    np.round(float(spec_data[spec_data.Mois == "2023-09-30"]["Commandes"].values - spec_data[spec_data.Mois == "2023-08-31"]["Commandes"]),2))
        st.write()

    with tab2:
        st.line_chart(data=spec_data, x="Mois", y="Score Google", use_container_width=True)

    with tab3:
        st.line_chart(data=spec_data, x="Mois", y="Score Uber", use_container_width=True)

