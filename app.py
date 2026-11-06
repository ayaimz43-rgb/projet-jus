import streamlit as st
import plotly.graph_objects as go

# 1. Configuration de la page
st.set_page_config(
    page_title="SimuProcess - Concentration de Jus",
    page_icon="🍊",
    layout="wide"
)

# Custom CSS pour un design créatif et moderne
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #ff7b00;
    }
    .op-card {
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f5 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# Titre Principal avec style
st.title("🍊 SimuProcess | Concentration de Jus d'Orange")
st.caption("Plateforme interactive de modélisation des bilans de matière et d'énergie")

# 2. Barre latérale (Inputs)
st.sidebar.header("⚙️ Paramètres d'Entrée")

st.sidebar.subheader("🔹 1 & 2. Filtration & Mélange")
m0 = st.sidebar.number_input("Débit initial m0 (kg/h)", value=1000.0)
x0 = st.sidebar.number_input("Taux matières solubles x0", value=0.10)
residus = st.sidebar.number_input("Particules insolubles (kg/h)", value=20.0)
mR = st.sidebar.number_input("Apport jus concentré mR (kg/h)", value=100.0)
xR = st.sidebar.number_input("Concentration apport xR", value=0.40)

st.sidebar.subheader("🔹 3, 4 & 5. Thermique & Évaporation")
Cp = st.sidebar.number_input("Capacité calorifique Cp (kJ/kg.°C)", value=3.8)
T2 = st.sidebar.number_input("Température entrée T2 (°C)", value=20.0)
T3 = st.sidebar.number_input("Température chauffage T3 (°C)", value=80.0)
x4 = st.sidebar.number_input("Concentration finale x4", value=0.40)
lambda_v = st.sidebar.number_input("Chaleur latente λv (kJ/kg)", value=2300.0)
T4 = st.sidebar.number_input("Température évaporation T4 (°C)", value=80.0)
T5 = st.sidebar.number_input("Température finale T5 (°C)", value=25.0)

# 3. Calculs
m1 = m0 - residus
x1 = (m0 * x0) / m1

m2 = m1 + mR
x2 = (m1 * x1 + mR * xR) / m2

Q3 = m2 * Cp * (T3 - T2) / 3600

m4 = m2 * x2 / x4
mv = m2 - m4
Q4 = mv * lambda_v / 3600

Q5 = m4 * Cp * (T4 - T5) / 3600

# 4. Affichage avec Onglets (Tabs)
tab1, tab2 = st.tabs(["📊 Résultats par Opération", "📈 Graphiques & Bilans"])

with tab1:
    st.markdown("## 📋 Éléments de Sortie par Unité")

    # Opération 1
    with st.container():
        st.markdown("<div class='op-card'>", unsafe_allow_html=True)
        st.subheader("1. 🥣 Opération : Filtration")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Débit après filtration (m₁)", value=f"{m1:.2f} kg/h")
        with col2:
            st.metric(label="Concentration en solubles (x₁)", value=f"{x1:.4f}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Opération 2
    with st.container():
        st.markdown("<div class='op-card'>", unsafe_allow_html=True)
        st.subheader("2. 🔀 Opération : Mélange")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Débit mélange (m₂)", value=f"{m2:.2f} kg/h")
        with col2:
            st.metric(label="Concentration mélange (x₂)", value=f"{x2*100:.2f} %")
        st.markdown("</div>", unsafe_allow_html=True)

    # Opération 3
    with st.container():
        st.markdown("<div class='op-card'>", unsafe_allow_html=True)
        st.subheader("3. 🔥 Opération : Chauffage")
        st.metric(label="Puissance thermique de chauffage (Q₃)", value=f"{Q3:.2f} kW")
        st.markdown("</div>", unsafe_allow_html=True)

    # Opération 4
    with st.container():
        st.markdown("<div class='op-card'>", unsafe_allow_html=True)
        st.subheader("4. 💨 Opération : Évaporation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Débit jus concentré (m₄)", value=f"{m4:.2f} kg/h")
        with col2:
            st.metric(label="Eau évaporée (mv)", value=f"{mv:.2f} kg/h")
        with col3:
            st.metric(label="Puissance d'évaporation (Q₄)", value=f"{Q4:.2f} kW")
        st.markdown("</div>", unsafe_allow_html=True)

    # Opération 5
    with st.container():
        st.markdown("<div class='op-card'>", unsafe_allow_html=True)
        st.subheader("5. ❄️ Opération : Refroidissement")
        st.metric(label="Puissance de refroidissement (Q₅)", value=f"{Q5:.2f} kW")
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("📊 Suivi du Débit Massique au long du Procédé")
    
    # Graphique interactif des débits
    etapes = ['Entrée (m0)', 'Filtration (m1)', 'Mélange (m2)', 'Concentré (m4)', 'Vapeur (mv)']
    debits = [m0, m1, m2, m4, mv]
    
    fig = go.Figure(data=[
        go.Bar(
            x=etapes, 
            y=debits,
            text=[f"{v:.1f} kg/h" for v in debits],
            textposition='auto',
            marker_color=['#17a2b8', '#6c757d', '#28a745', '#ff7b00', '#dc3545']
        )
    ])
    
    fig.update_layout(
        title="Profil des Débits Massiques (kg/h)",
        xaxis_title="Étapes du procédé",
        yaxis_title="Débit (kg/h)",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)