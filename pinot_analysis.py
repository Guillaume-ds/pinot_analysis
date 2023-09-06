import streamlit as st
import pandas as pd
import numpy as np
import datetime 
import time

from Utils.styles import title_style,paragraph_style

# Data 
entreprises = ["Pinot central","P II","PC","PH","PM","PL","P gourmet"]
all_data = pd.read_csv('./Data/data_pinot.csv')
all_data.Mois = pd.to_datetime(all_data.Mois)
st.session_state.data = True
def set_data_false():
    st.session_state.data = False

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
    st.session_state.selected_entreprise = st.selectbox("Sélectionnez une entreprise", entreprises,on_change=set_data_false)

st.markdown(title_style, unsafe_allow_html=True)

# Container 

container = st.empty()

if st.session_state.selected_entreprise == None:
    container.markdown(f"""
                        <h1 class="section-title">Veuillez séléctionner une entreprise à analyser </h1>
                        """, unsafe_allow_html=True)

with st.sidebar:
    scrap_selected_entreprise = st.button(f'Collecter les données de {st.session_state.selected_entreprise}')

if scrap_selected_entreprise:
    with st.spinner(f'Collecte des données de l\'entrepise {st.session_state.selected_entreprise}...'):
        time.sleep(.2)
        container.empty()
        st.session_state.data = True
        container.markdown(f'<h1 class="section-title">Données de l\'entreprise {st.session_state.selected_entreprise} collectées !</h1>', unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["Performance Mensuel", "Focus Google", "Focus Uber Eats"])

st.session_state.spec_data = all_data[all_data.Entreprise == st.session_state.selected_entreprise]

if st.session_state.data == False :
    container.markdown(f'<h1 class="section-title">Veuillez charger les données de l\'entreprise {st.session_state.selected_entreprise}</h1>', unsafe_allow_html=True)

if st.session_state.data == True:
    with st.sidebar:
        st.markdown(title_style, unsafe_allow_html=True)
        st.markdown(title_style, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        m = col1.date_input(label="Mois debut",
                                value=pd.to_datetime("2022-01-01"),
                                min_value=pd.to_datetime("2022-01-01"),
                                format="YYYY-MM-DD")
        st.session_state.month = pd.to_datetime(m).replace(day=1)
        m2 = col2.date_input(label="Mois fin",
                                value=pd.to_datetime("2023-09-01"),
                                min_value=pd.to_datetime("2022-01-01"),
                                format="YYYY-MM-DD")
        st.session_state.month2 = pd.to_datetime(m2).replace(day=1)

    container.markdown(f"""
                    <h1 class="section-title">Données de l'entreprise {st.session_state.selected_entreprise}</h1>
                    <h3 class="small-title">Du {st.session_state.month.date()} au {st.session_state.month2.date()}</h3>
                    """, unsafe_allow_html=True)

    with tab1:
        st.markdown(title_style, unsafe_allow_html=True)

        st.session_state.spec_data_month = st.session_state.spec_data[(st.session_state.spec_data.Mois >= st.session_state.month) 
                                                                    & (st.session_state.spec_data.Mois <= st.session_state.month2)]

        st.session_state.month3 = (st.session_state.month2 - datetime.timedelta(days=4)).replace(day=1)

        st.markdown(f"""
                <h3 class="small-title">Résultat au {st.session_state.month2.date()}</h3>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        score_google = st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Score Google"]
        score_google_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Score Google"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["Score Google"]),2)
        col1.metric("Score Google",
                    score_google, 
                    score_google_1
                    )

        score_uber = st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Score Uber"]
        score_uber_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Score Uber"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["Score Uber"]),2)
        col2.metric("Score Uber",
                    score_uber, 
                    np.round(score_uber_1,2)
                    )

        col3.metric("Score moyen",
            np.round((score_uber+score_google)/2,2), 
            np.round((score_uber_1+score_google_1)/2))

        score_prct = st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["% erreurs"]
        score_prct_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["% erreurs"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["% erreurs"]),2)
        col1.metric("% erreurs",
                    score_prct, 
                    score_prct_1
                    )
        
        col2.metric("Nombre de commandes",
                    st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Commandes"], 
                    np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Commandes"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["Commandes"]),2))

        score_sal = st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Nombre Salaries"]
        score_sal_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Nombre Salaries"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["Nombre Salaries"]),2)
        col3.metric("Nb salariés",
                    score_sal, 
                    score_sal_1
                    )

        st.markdown(title_style, unsafe_allow_html=True)
        st.markdown(title_style, unsafe_allow_html=True)
        st.markdown(title_style, unsafe_allow_html=True)
        st.markdown(title_style, unsafe_allow_html=True)

        st.markdown(f"""
                <h3 class="small-title">Moyenne de la période</h3>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        score_google = np.round(st.session_state.spec_data_month["Score Google"].mean(),2)
        score_google_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Score Google"].values 
                            - st.session_state.spec_data_month["Score Google"].mean()),2)
        col1.metric("Score Google",
                    score_google, 
                    score_google_1)

        score_uber = np.round(st.session_state.spec_data_month["Score Uber"].mean(),2)
        score_uber_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month .Mois == st.session_state.month2]["Score Uber"].values 
                            - st.session_state.spec_data_month["Score Uber"].mean()),2)

        col2.metric("Score Uber",
                    score_uber, 
                    score_uber_1)

        col3.metric("Score moyen",
                    np.round((score_uber+score_google)/2,2), 
                    (score_uber_1+score_google_1)/2)




        score_prct = st.session_state.spec_data_month["% erreurs"].mean()
        score_prct_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["% erreurs"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["% erreurs"]),2)
        col1.metric("% erreurs",
                    np.round(score_prct,2), 
                    score_prct_1
                    )
        
        col2.metric("Nombre de commandes",
                    np.round(st.session_state.spec_data_month["Commandes"].mean(),2), 
                    np.round(float(st.session_state.spec_data_month [st.session_state.spec_data_month .Mois == st.session_state.month2]["Commandes"].values 
                            - st.session_state.spec_data_month["Commandes"].mean()),2))

        score_sal = st.session_state.spec_data_month["Nombre Salaries"].mean()
        score_sal_1 = np.round(float(st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month2]["Nombre Salaries"].values 
                            - st.session_state.spec_data_month[st.session_state.spec_data_month.Mois == st.session_state.month3]["Nombre Salaries"]),2)
        col3.metric("Nb salariés",
                    score_sal, 
                    score_sal_1
                    )


        st.markdown(title_style, unsafe_allow_html=True)
        st.markdown(title_style, unsafe_allow_html=True)

        with st.expander("Voir les données"):
            cols = ["Mois","Score Google","Score Uber","Commandes","% erreurs"]
            st.dataframe(st.session_state.spec_data[cols])

    with tab2:
        st.line_chart(data=st.session_state.spec_data, x="Mois", y="Score Google", use_container_width=True)



    with tab3:
        st.line_chart(data=st.session_state.spec_data, x="Mois", y="Score Uber", use_container_width=True)

