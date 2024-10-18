import pandas as pd
import streamlit as st
from fpdf import FPDF
import re
import ast

######################################################################################################################
########### TITRE DE L'ONGLET ########################################################################################
######################################################################################################################
st.set_page_config(
    page_title="Data Management RZA",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Application de suivi des outils de science ouverte du RZA, développé par Jérôme Dutroncy"}
)

######################################################################################################################
########### COULEURS DES PAGES #######################################################################################
######################################################################################################################
st.markdown("""
 <style>
    [data-testid=stSidebar] {
        background-color: rgb(6,51,87,0.2);
    }
    .st-emotion-cache-1dj0hjr {
            color: #a9dba6;
    }
    .st-emotion-cache-1q2d4ya {
            color: #3b979f;
    }
    </style>
""", unsafe_allow_html=True)

######################################################################################################################
########### CHOIX VISUELS ############################################################################################
######################################################################################################################
couleur_subtitles = (250,150,150)
taille_subtitles = "25px"
couleur_subsubtitles = (60,150,160)
taille_subsubtitles = "25px"
couleur_True = (0,200,0)
couleur_False = (200,0,0)
wch_colour_box = (250,250,220)
wch_colour_font = (90,90,90)
fontsize = 70

######################################################################################################################
########### PARAMETRES ###############################################################################################
######################################################################################################################

HAL = pd.read_csv("pages/data/Hal/Contenu_HAL_complet.csv", index_col=[0])

data_Indores = pd.read_csv("pages/data/Data_InDoRES/Contenu_DataInDoRES2.csv",index_col=[0])
data_RDG = pd.read_csv("pages/data/rechercheDataGouv/Contenu_RDG_complet.csv", index_col=[0])
data_dryad = pd.read_csv("pages/data/Dryad/Contenu_DRYAD_complet.csv", index_col=[0])
data_nakala = pd.read_csv("pages/data/Nakala/Contenu_NAKALA_complet.csv", index_col=[0])
data_zenodo = pd.read_csv("pages/data/Zenodo/Contenu_ZENODO_complet.csv", index_col=[0])
data_gbif = pd.read_csv("pages/data/Gbif/Contenu_GBIF_complet.csv", index_col=[0])

catalogue_checked = pd.read_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked.csv", index_col=[0])
catalogue_checked_c = catalogue_checked.copy()


catalogue = pd.read_csv("pages/data/Cat_InDoRES/infos_MD2/Tableau_complet.csv", index_col=[0])

######################################################################################################################
########### FILTRE CATALOGUES ########################################################################################
######################################################################################################################

liste_ZAs_ = ["Zone atelier territoires uranifères",
              " Zone Atelier Seine",
              " Zone atelier Loire",
              " Zone atelier bassin du Rhône",
              " Zone atelier bassin de la Moselle",
              " Zone atelier Alpes",
              " Zone atelier arc jurassien",
              " Zone atelier Armorique",
              " Zone atelier Plaine et Val de Sèvre",
              " Zone atelier environnementale urbaine",
              " Zone atelier Hwange",
              " Zone atelier Pyrénées Garonne",
              " Zone atelier Brest Iroise",
              " Zone Atelier Antarctique et Terres Australes",
              " Zone Atelier Santé Environnement Camargue",
              " Zone Atelier Argonne"]


######################################################################################################################
########### SELECTION ZA #############################################################################################
######################################################################################################################

all_ZAs= st.sidebar.checkbox("Ensemble du réseau ZA")
if all_ZAs==True :
    Selection_ZA = liste_ZAs_
else:
    Selection_ZA= st.sidebar.multiselect(label="Zones Ateliers", options=liste_ZAs_)



def extract_pattern(s):
    start = s.find('10.')  # Find the starting index of "(10."
    if start == -1:
        return None  # If "(10." is not found, return None
    end = s.find(' ', start)  # Find the closing ")" starting from the position of "(10."
    if end == -1:
        return None  # If closing ")" is not found, return None
    return "https://doi.org/" + s[start:end-2]  # Extract and return the substring

######################################################################################################################
########### VISUALISATIONS ###########################################################################################
######################################################################################################################
st.title(":grey[Bilan des recherches - Perspectives]")

if len(Selection_ZA)!=0:

    #### TRAITEMENT HAL
    HAL['Checked_doi']= HAL['Titre et auteurs'].apply(extract_pattern)
    liste_to_keep_HAL = ['Uri','Type de document', 'Checked_doi']
    HAL_ = HAL[HAL['Entrepot'].isin(Selection_ZA)]
    HAL__ = HAL_[liste_to_keep_HAL]
    HAL__.reset_index(inplace=True)
    HAL__.drop(columns='index', inplace=True)

    HAL_dico = {'COUV':"Chapitre d'ouvrage",
                'OUV':'Ouvrage',
                'COMM':'communication',
                'ART':'Article',
                'POSTER':'Poster',
                'REPORT':'Rapport',
                'UNDEFINED':'Indéfini',
                'THESE':'These',
                'OTHER':'Autre',
                'MEM':'Mémoire',
                'PROCEEDINGS':'Protocoles',
                'HDR':'HDR'}
    HAL__["Type de document"] = HAL__["Type de document"].map(HAL_dico)
    HAL_count = HAL__['Type de document'].value_counts()
    df_HAL_count = pd.DataFrame(HAL_count)

    #### TRAITEMENT INDORES
    liste_to_keep_InDoRES = ['Entrepot','Url','Publication URL','Lien publication']
    data_Indores_ = data_Indores[data_Indores['Entrepot'].isin(Selection_ZA)]
    data_Indores_.reset_index(inplace=True)
    data_Indores_.drop(columns='index', inplace=True)
    for i in range(len(data_Indores_)):
        try:
            if 'https' in data_Indores_.loc[i,'Publication URL']:
                data_Indores_.loc[i,'Lien publication']= True
        except:
            data_Indores_.loc[i,'Lien publication']= False
    data_Indores__ = data_Indores_[liste_to_keep_InDoRES]

    liste_to_keep = ['Entrepot','Url','Store']
    data_Indores__toconcat = data_Indores_[liste_to_keep]

    #### TRAITEMENT RDG
    data_RDG.rename(columns={'Publication Url':'Url'}, inplace=True)
    data_RDG_ = data_RDG[data_RDG['Entrepot'].isin(Selection_ZA)]
    data_RDG__ = data_RDG_[liste_to_keep]

    #### TRAITEMENT DRYAD
    data_dryad.rename(columns={'Publication URL':'Url'}, inplace=True)
    data_dryad_ = data_dryad[data_dryad['Entrepot'].isin(Selection_ZA)]
    data_dryad__ = data_dryad_[liste_to_keep]

    #### TRAITEMENT NAKALA
    data_nakala.rename(columns={'Publication Url':'Url'}, inplace=True)
    data_nakala_ = data_nakala[data_nakala['Entrepot'].isin(Selection_ZA)]
    data_nakala__ = data_nakala_[liste_to_keep]

    #### TRAITEMENT ZENODO
    data_zenodo.rename(columns={'Publication Url':'Url'}, inplace=True)
    data_zenodo_ = data_zenodo[data_zenodo['Entrepot'].isin(Selection_ZA)]
    data_zenodo__ = data_zenodo_[liste_to_keep]

    #### TRAITEMENT GBIF
    data_gbif.rename(columns={'Publication URL':'Url'}, inplace=True)
    data_gbif_ = data_gbif[data_gbif['Entrepot'].isin(Selection_ZA)]
    data_gbif__ = data_gbif_[liste_to_keep]

    #### CONCATENATION STORED
    data_stored = pd.concat([data_Indores__toconcat,data_dryad__,data_gbif__,data_nakala__,data_RDG__,data_zenodo__], axis=0)
    data_stored.reset_index(inplace=True)
    data_stored.drop(columns='index', inplace=True)

    data_stored_count = data_stored['Store'].value_counts()
    df_data_stored_count = pd.DataFrame(data_stored_count)


    def transfo(input_string):
        # Use ast.literal_eval to safely evaluate the string as a Python expression
        return ast.literal_eval(input_string)
    
    ##########################################################################################
    ########### POUR L'ADMINISTRATEUR ########################################################
    ##########################################################################################

    # Mot de passe pour faire des récupérations automatisées
    admin_pass = 'admin'
    admin_action = st.sidebar.text_input(label="Pour l'administrateur")


    if admin_action == admin_pass:
        # RECUPERATION DES CONTENUS VIA BOUTON ##############################################       
        Check_depots = st.sidebar.checkbox('Vérifier les liens')
        if Check_depots:
            copie_to_write = pd.read_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked_stored.csv", index_col=[0])
            columns_to_transfo = ['Url','Children','Parent','Fcats','BroAndSisters']
            for x,col in enumerate(columns_to_transfo):
                copie_to_write[col] = copie_to_write[col].apply(transfo)
            edited_df = st.data_editor(copie_to_write)
            edited_df.reset_index(inplace=True)

            if st.button("Save Changes"):
                # Save to CSV or any format
                edited_df.to_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked_stored.csv", index=False)
                st.success("DataFrame has been saved!")


    #### TRAITEMENT CATALOGUE CHECKED
    columns_to_transfo = ['Url','Children','Parent','Fcats','BroAndSisters']
    for x,col in enumerate(columns_to_transfo):
        catalogue_checked_c[col] = catalogue_checked_c[col].apply(transfo)

    liste_to_keep_copie = ['Identifiant','Store']
    copie = pd.read_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked_stored.csv", index_col=[0])
    copie_ = copie[liste_to_keep_copie]

    catalogue_checked_c_ = pd.merge(catalogue_checked_c, copie_, on='Identifiant', how='inner')
    catalogue_checked_c_.to_csv("pages/data/Cat_InDoRES/Contenu_CatInDoRES_checked_stored.csv")
    catalogue_checked_c__ = catalogue_checked_c_[catalogue_checked_c_['GroupeEtMention'].isin(Selection_ZA)]

    catalogue_checked_count = catalogue_checked_c__['Store'].value_counts()
    df_catalogue_checked_count =pd.DataFrame(catalogue_checked_count)

    #### TRAITEMENT CATALOGUE GENERAL
    catalogue_ = catalogue[catalogue['GroupeEtMention'].isin(Selection_ZA)]
    #st.dataframe(catalogue_)

    if len(Selection_ZA)==1:
        Visu_depots = f"Bilan pour la {Selection_ZA[0]}"
        s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
        st.markdown(s_Visu_depots ,unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        with col1:
            t_hal = f"HAL"
            s_thal = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_hal}</p>"
            st.markdown(s_thal,unsafe_allow_html=True)
            st.table(HAL_count)

        with col2:
            t_stored = f"ENTREPOTS"
            s_tstored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_stored}</p>"
            st.markdown(s_tstored,unsafe_allow_html=True)
            st.table(data_stored_count)

        with col3:
            t_cat_stored = f"DEPOTS AILLEURS"
            s_tcat_stored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_cat_stored}</p>"
            st.markdown(s_tcat_stored,unsafe_allow_html=True)
            st.table(catalogue_checked_count)

    elif 1<len(Selection_ZA)<16:
        selection_name = ""
        for i in range(len(Selection_ZA)):
            selection_name+=Selection_ZA[i].strip().replace("Zone atelier", "ZA ").replace(" ","")
        Visu_depots = f"Bilan pour les ZA suivantes: {Selection_ZA}"
        s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
        st.markdown(s_Visu_depots ,unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        with col1:
            t_hal = f"HAL"
            s_thal = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_hal}</p>"
            st.markdown(s_thal,unsafe_allow_html=True)
            st.table(HAL_count)

        with col2:
            t_stored = f"ENTREPOTS"
            s_tstored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_stored}</p>"
            st.markdown(s_tstored,unsafe_allow_html=True)
            st.table(data_stored_count)

        with col3:
            t_cat_stored = f"DEPOTS AILLEURS"
            s_tcat_stored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_cat_stored}</p>"
            st.markdown(s_tcat_stored,unsafe_allow_html=True)
            st.table(catalogue_checked_count)

    elif len(Selection_ZA)==16:
        selection_name = "All_ZAs"
        Visu_depots = f"Bilan pour l'ensemble du réseau des Zones Ateliers"
        s_Visu_depots  = f"<p style='font-size:25px;color:rgb(150,150,150)'>{Visu_depots}</p>"
        st.markdown(s_Visu_depots ,unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)
        with col1:
            t_hal = f"HAL"
            s_thal = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_hal}</p>"
            st.markdown(s_thal,unsafe_allow_html=True)
            st.table(HAL_count)

        with col2:
            t_stored = f"ENTREPOTS"
            s_tstored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_stored}</p>"
            st.markdown(s_tstored,unsafe_allow_html=True)
            st.table(data_stored_count)

        with col3:
            t_cat_stored = f"DEPOTS AILLEURS"
            s_tcat_stored = f"<p style='font-size:{taille_subtitles};color:rgb{couleur_subtitles}'>{t_cat_stored}</p>"
            st.markdown(s_tcat_stored,unsafe_allow_html=True)
            st.table(catalogue_checked_count)

    


    ######################################################################################################################
    ########### CREATION PDF ############################################################################################
    ######################################################################################################################

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add text to the PDF
        pdf.cell(200, 10, txt="Hello from Streamlit!", ln=True, align="C")
        pdf.cell(200, 10, txt="This is a simple PDF example.", ln=True, align="C")

        # Table header
        pdf.set_font("Arial", 'B', 12)  # Bold font for header
        for col in df_HAL_count.columns:
            pdf.cell(40, 10, col, border=1)  # Adjust column width if needed
        pdf.ln()
        for index, row in df_HAL_count.iterrows():
            for item in row:
                pdf.cell(40, 10, str(item), border=1)  # Convert items to string if needed
            pdf.ln()

        # Save the PDF to a temporary file
        pdf_output = "example_table_from_df.pdf"
        pdf.output(pdf_output)
        return pdf_output

    pdf_file = create_pdf()

    # Read the created PDF file
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()

    # Streamlit download button
    st.download_button(
        label="Download PDF",
        data=pdf_data,
        file_name="generated_pdf.pdf",
        mime="application/pdf"
            )