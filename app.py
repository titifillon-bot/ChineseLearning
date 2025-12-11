import streamlit as st
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Radicaux Chinois", layout="wide")

# --- CSS AVANCÉ (LE CŒUR DU PROBLÈME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* 1. Reset général */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f4f6f9; }

    /* 2. La Carte (Partie Supérieure) */
    /* Note : On met radius-bottom à 0 pour coller aux boutons */
    .flashcard-body {
        background-color: white;
        padding: 40px 20px;
        border-radius: 20px 20px 0 0; 
        box-shadow: 0 -10px 25px rgba(0,0,0,0.05); /* Ombre vers le haut surtout */
        text-align: center;
        margin-bottom: 0px !important; /* CRUCIAL : Pas de marge sous la carte */
        border-bottom: 1px solid #f0f0f0; /* Légère séparation visuelle */
    }
    
    /* Typographie */
    .card-label { color: #94a3b8; font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;}
    .card-main-text { color: #1e293b; font-weight: 800; font-size: 42px; margin: 10px 0; }
    .card-sub-text { color: #3b82f6; font-weight: 600; font-size: 28px; margin-top: 5px; }
    .card-char { font-size: 120px; color: #0f172a; line-height: 1.1; margin: 10px 0; }

    /* 3. Les Boutons (Partie Inférieure) */
    /* On cible TOUS les boutons dans l'app pour les rendre gros et solides */
    .stButton button {
        width: 100%;
        border: none;
        height: 70px;
        font-weight: 700;
        font-size: 18px;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Le bouton RÉVÉLER (Bleu large) */
    /* On cible le bouton unique quand il n'est pas dans une colonne */
    div:not([data-testid="column"]) > .stButton button {
        border-radius: 0 0 20px 20px; /* Arrondi en bas uniquement */
        background-color: #3b82f6;
        color: white;
    }
    div:not([data-testid="column"]) > .stButton button:hover { background-color: #2563eb; }

    /* Les boutons ACTION (Rouge et Vert) */
    /* On cible les boutons à l'intérieur des colonnes */
    div[data-testid="column"] .stButton button {
        border-radius: 0 0 20px 20px; /* Arrondi en bas uniquement */
        color: white;
    }

    /* Colonne de gauche (À revoir) - Rouge */
    div[data-testid="column"]:nth-of-type(1) .stButton button {
        background-color: #ef4444;
        border-radius: 0 0 0 20px; /* Arrondi coin bas-gauche seulement */
    }
    div[data-testid="column"]:nth-of-type(1) .stButton button:hover { background-color: #dc2626; }

    /* Colonne de droite (Mémorisé) - Vert */
    div[data-testid="column"]:nth-of-type(2) .stButton button {
        background-color: #22c55e;
        border-radius: 0 0 20px 0; /* Arrondi coin bas-droite seulement */
    }
    div[data-testid="column"]:nth-of-type(2) .stButton button:hover { background-color: #16a34a; }

    /* 4. HACK : Supprimer l'espace vertical entre le HTML et les boutons */
    /* Cible le container Markdown qui précède les boutons */
    .element-container:has(.flashcard-body) {
        margin-bottom: -17px !important; /* Tire les boutons vers le haut */
    }
    
    /* Centre tout le contenu */
    .block-container { max-width: 700px; padding-top: 2rem; }
    
    /* Cache la barre de progression par défaut moche et fine */
    .stProgress > div > div > div > div { background-color: #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# --- ETAT (Mockup pour l'exemple) ---
if 'revealed' not in st.session_state: st.session_state.revealed = False

# Fonction reset pour la démo
def reset():
    st.session_state.revealed = False
    # Ici tu mettrais ton logic de next_card()

# --- INTELLIGENCE DE L'INTERFACE ---

# 1. Barre de progression (Minimaliste)
st.caption("Progression : 1 / 600")
st.progress(1/600)

# 2. Contenu HTML de la carte (Partie Haute)
# Note: On inclut le titre ET la réponse potentielle dans le même bloc HTML
# pour éviter des coupures visuelles.

mode_text = "FR -> SYMBOLE"
question_text = "Toit (Rad40)"
answer_char = "宀"
answer_pinyin = "mián"

html_content = f"""
<div class="flashcard-body">
    <div class="card-label">{mode_text}</div>
    <div class="card-main-text">{question_text}</div>
"""

# Si révélé, on ajoute la réponse DANS le même bloc blanc
if st.session_state.revealed:
    html_content += f"""
    <div style="margin-top: 30px; padding-top: 20px; border-top: 2px dashed #f1f5f9;">
        <div class="card-char">{answer_char}</div>
        <div class="card-sub-text">{answer_pinyin}</div>
    </div>
    """

html_content += "</div>" # Fermeture du div principal

# Rendu de la "Boite blanche"
st.markdown(html_content, unsafe_allow_html=True)

# 3. Zone des boutons (Partie Basse)
# L'astuce ici est d'utiliser st.columns avec gap="0" pour que les boutons se touchent

if not st.session_state.revealed:
    # Bouton unique "Révéler"
    # Le CSS va le coller au bas de la carte blanche
    if st.button("👁️ Révéler la réponse"):
        st.session_state.revealed = True
        st.rerun()

else:
    # Boutons d'action
    # On utilise gap="0" pour coller les deux colonnes
    c1, c2 = st.columns(2, gap="small") 
    
    with c1:
        if st.button("❌ À revoir"):
            reset()
            st.rerun()
            
    with c2:
        if st.button("✅ Mémorisé"):
            reset()
            st.rerun()
