import streamlit as st
import pandas as pd
import joblib

# Configuration de la page
st.set_page_config(page_title="Prédicteur de Crédit ", layout="wide")

# Chargement du nouveau modèle
@st.cache_resource
def load_model():
    try:
        return joblib.load('modele_naive_bayes_credit.pkl')
    except FileNotFoundError:
        st.error("❌ Modèle non trouvé! Le fichier 'modele_naive_bayes_credit.pkl' est manquant.")
        st.stop()
        return None

model = load_model()

# Titre
st.title("💳 Système d'Aide à la Décision : Carte de Crédit ")
st.markdown("Cette version utilise un modèle **Naïve Bayes optimisé**  pour une prédiction réelle avant octroi.")

st.divider()

# Barre latérale (Sidebar) - Identique à la V1 mais sans 'Share'
st.sidebar.header("📋 Informations du Client")

def user_input():
    reports = st.sidebar.number_input("Nombre d'incidents de paiement", min_value=0, max_value=20, value=0)
    age = st.sidebar.slider("Âge", 18, 100, 30)
    income = st.sidebar.number_input("Revenu annuel (x10 000 $)", min_value=0.0, value=3.5)
    
    owner = st.sidebar.selectbox("Propriétaire de son logement ?", ("Oui", "Non"))
    owner = 1 if owner == "Oui" else 0
    
    selfemp = st.sidebar.selectbox("Travailleur indépendant ?", ("Oui", "Non"))
    selfemp = 1 if selfemp == "Oui" else 0
    
    dependents = st.sidebar.number_input("Nombre de personnes à charge", min_value=0, max_value=10, value=0)
    months = st.sidebar.number_input("Mois à l'adresse actuelle", min_value=0, value=12)
    majorcards = st.sidebar.selectbox("Possède d'autres cartes majeures ?", (1, 0))
    active = st.sidebar.number_input("Nombre de comptes de crédit actifs", min_value=0, value=5)

    data = {
        'reports': reports,
        'age': age,
        'income': income,
        'owner': owner,
        'selfemp': selfemp,
        'dependents': dependents,
        'months': months,
        'majorcards': majorcards,
        'active': active
    }
    return pd.DataFrame(data, index=[0])

# Données utilisateur
input_df = user_input()

# Affichage central (Style V1)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Résumé du profil")
    st.write(input_df.T.rename(columns={0: 'Valeurs'}))

with col2:
    st.subheader("Résultat de l'Analyse")
    
    if st.button('Analyser le dossier'):
        # On s'assure que l'ordre des colonnes est identique à l'entraînement
        prediction = model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)
        score = prediction_proba[0][1]

        if prediction[0] == 1:
            st.success(f"✅ **DEMANDE APPROUVÉE**")
            st.balloons()
        else:
            st.error(f"❌ **DEMANDE REFUSÉE**")

        st.write(f"Indice de confiance : **{score:.2%}**")
        st.progress(score)
        
        # Petit conseil métier
        if score > 0.8:
            st.info("💡 Profil excellent : Risque très faible.")
        elif score > 0.5:
            st.warning("⚠️ Profil intermédiaire : Vérification manuelle conseillée.")
        else:
            st.error("🚨 Profil à risque : Antécédents ou revenus insuffisants.")

st.divider()
st.caption("Modèle : Naïve Bayes (Gaussian) | Source : AER Credit Data | Status : Production V1")