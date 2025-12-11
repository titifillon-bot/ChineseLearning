import streamlit as st
import random
import time

# --- CONFIGURATION DE LA PAGE (Doit être au début) ---
st.set_page_config(page_title="Flashcards Chinois", layout="wide")

# --- CSS PERSONNALISÉ ---
# C'est ici que la magie opère pour le look "Tablette/Carte"
st.markdown("""
    <style>
    /* --- IMPORT POLICE GOOGLE --- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', 'Noto Sans SC', sans-serif;
    }

    /* --- STYLE GÉNÉRAL DES BOUTONS --- */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }

    /* --- STYLE SIDEBAR --- */
    /* Boutons "Tous" (Verts) */
    div[data-testid="column"] > div > div > div > div.stButton > button:contains("✅ Tous") {
        background-color: #4CAF50 !important; color: white !important;
    }
    /* Boutons "Aucun" (Rouges) */
    div[data-testid="column"] > div > div > div > div.stButton > button:contains("❌ Aucun") {
        background-color: #f44336 !important; color: white !important;
    }
    /* Bouton "LANCER LE JEU" (Bleu foncé, gros) */
    div.stSidebar > div > div > div > div.stButton > button:contains("🚀 LANCER LE JEU") {
        background-color: #1976D2 !important; color: white !important;
        font-size: 1.2em; padding: 15px; margin-top: 20px;
    }

    /* --- STYLE ZONE PRINCIPALE (LA CARTE) --- */
    /* Le conteneur style "Carte" */
    .stCard {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        text-align: center;
        margin-top: 20px;
    }

    /* Titre de la question */
    .question-header { font-size: 1.5em; color: #333; margin-bottom: 20px; }

    /* Le contenu principal (Caractère + Pinyin) - TRÈS GROS */
    .main-content-box {
        display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 30px;
    }
    .huge-char { font-size: 100px; color: #1976D2; font-weight: bold; line-height: 1;}
    .huge-pinyin { font-size: 80px; color: #1976D2; font-weight: bold; line-height: 1;}

    /* Bouton RÉVÉLER (Bleu clair) */
    .stCard > div.stButton > button:contains("RÉVÉLER") {
        background-color: #E3F2FD !important; color: #1976D2 !important; font-size: 1.2em;
    }

    /* Zone de réponse */
    .answer-label { font-size: 1.5em; color: #666; margin-top: 20px; }
    .answer-text { font-size: 40px; font-weight: bold; color: #333; margin: 10px 0 30px 0;}

    /* --- BOUTONS D'ACTION FINAUX (Rouge et Vert) --- */
    /* C'est un hack CSS pour cibler les boutons dans les colonnes finales */
    /* Colonne de gauche (À REVOIR - Rouge) */
    div[data-testid="column"]:nth-of-type(1) > div > div > div > div.stButton > button:contains("À REVOIR") {
        background-color: #EF5350 !important; color: white !important; font-size: 1.2em; height: 60px;
    }
    /* Colonne de droite (MÉMORISÉ - Vert) */
    div[data-testid="column"]:nth-of-type(2) > div > div > div > div.stButton > button:contains("MÉMORISÉ") {
        background-color: #66BB6A !important; color: white !important; font-size: 1.2em; height: 60px;
    }

    /* --- PROGRESS BAR STYLE --- */
    .stProgress > div > div > div > div { background-color: #1976D2; }
    </style>
    """, unsafe_allow_html=True)


# --- DONNÉES ---
# (J'utilise un petit échantillon pour l'exemple, basé sur ton image)
if 'all_data' not in st.session_state:
    st.session_state.all_data = {
        "1-10": [("口", "kǒu", "Bouche (Rad30)")], # Exemple de l'image
        "11-20": [("火", "huǒ", "Feu (Rad86)"), ("水", "shuǐ", "Eau (Rad85)")],
        "21-30": [("大", "dà", "Grand (Rad37)")],
        "31-40": [("门", "mén", "Porte (Rad169)")],
        # Ajoute les autres séries ici...
    }

# --- GESTION DE L'ÉTAT (SESSION STATE) ---
# Initialisation des variables si elles n'existent pas
defaults = {
    'deck': [],
    'current_card': None,
    'revealed': False,
    'game_active': False,
    'total_cards_initial': 0,
    'needs_rerun': False # Hack pour forcer le rafraîchissement parfois
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Initialisation des états des checkboxes (tout coché par défaut)
for serie in st.session_state.all_data.keys():
    if f"chk_s_{serie}" not in st.session_state: st.session_state[f"chk_s_{serie}"] = True

modes_list = ["Pinyin → FR", "FR → Pinyin", "FR → Symbole", "Symbole → FR", "Pinyin → Symbole", "Symbole → Pinyin"]
for mode in modes_list:
    if f"chk_m_{mode}" not in st.session_state: st.session_state[f"chk_m_{mode}"] = True


# --- FONCTIONS LOGIQUES ---
def toggle_series(state):
    for serie in st.session_state.all_data.keys():
        st.session_state[f"chk_s_{serie}"] = state
    st.session_state.needs_rerun = True

def toggle_modes(state):
    for mode in modes_list:
        st.session_state[f"chk_m_{mode}"] = state
    st.session_state.needs_rerun = True

def start_game():
    deck = []
    selected_series = [s for s in st.session_state.all_data.keys() if st.session_state[f"chk_s_{s}"]]
    selected_modes_txt = [m for m in modes_list if st.session_state[f"chk_m_{m}"]]

    if not selected_series or not selected_modes_txt:
        st.error("Sélectionne au moins une série et un mode.")
        return

    # Création du deck
    for serie in selected_series:
        for item in st.session_state.all_data[serie]:
            # Pour simplifier l'exemple, je n'implémente que le mode de l'image (Pinyin -> FR)
            # Dans ton vrai code, tu bouclerais sur selected_modes_txt
            deck.append((item, "Pinyin → FR"))

    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.total_cards_initial = len(deck)
    st.session_state.game_active = True
    next_card()

def next_card():
    st.session_state.revealed = False
    if len(st.session_state.deck) > 0:
        st.session_state.current_card = st.session_state.deck[0]
    else:
        st.session_state.current_card = None
        st.session_state.game_active = False
        st.balloons()

def mark_ok():
    if st.session_state.deck: st.session_state.deck.pop(0)
    next_card()

def mark_ko():
    if st.session_state.deck:
        card = st.session_state.deck.pop(0)
        st.session_state.deck.append(card) # Remet à la fin
    next_card()


# =============================================
# CONSTRUCTION DE L'INTERFACE
# =============================================

# Hack pour forcer le rafraîchissement après les boutons "Tous/Aucun"
if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. CHOIX DES SÉRIES")
    c1, c2 = st.columns(2)
    c1.button("✅ Tous", key="s_all", on_click=toggle_series, args=(True,))
    c2.button("❌ Aucun", key="s_none", on_click=toggle_series, args=(False,))

    sorted_series = sorted(st.session_state.all_data.keys(), key=lambda x: int(x.split('-')[0]))
    for serie in sorted_series:
        st.checkbox(f"Série {serie}", key=f"chk_s_{serie}")

    st.markdown("---")
    st.header("2. CHOIX DES MODES")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="m_all", on_click=toggle_modes, args=(True,))
    c4.button("❌ Aucun", key="m_none", on_click=toggle_modes, args=(False,))

    for mode in modes_list:
        st.checkbox(mode, key=f"chk_m_{mode}")

    st.markdown("---")
    # Bouton principal
    st.button("🚀 LANCER LE JEU", on_click=start_game)


# --- ZONE PRINCIPALE ---

# Si le jeu n'est pas actif
if not st.session_state.game_active:
    st.info("👈 Configure tes options à gauche et clique sur LANCER LE JEU.")
    st.stop()

# Si le jeu est fini
if st.session_state.current_card is None:
    st.success("Session terminée ! Bravo !")
    if st.button("Recommencer"):
        st.session_state.game_active = False
        st.rerun()
    st.stop()


# --- AFFICHAGE DE LA CARTE ACTIVE ---
item, mode_txt = st.session_state.current_card
char, pinyin, fr = item
remaining = len(st.session_state.deck)
total = st.session_state.total_cards_initial
progress = (total - remaining) / total if total > 0 else 0

# 1. Barre supérieure (Compteur + Progress Bar)
st.markdown(f"**Cartes restantes : {remaining} / {total}**")
st.progress(progress)

# 2. Le Conteneur "Carte" (Début du HTML personnalisé)
st.markdown('<div class="stCard">', unsafe_allow_html=True)

# En-tête de la question
st.markdown(f'<div class="question-header">Question: {mode_txt}</div>', unsafe_allow_html=True)

# Contenu Principal (Caractère + Pinyin en gros)
# Note : J'adapte selon le mode. Pour l'image, c'est Pinyin -> FR, donc on affiche le Pinyin et le caractère
st.markdown(f"""
    <div class="main-content-box">
        <span class="huge-char">{char}</span>
        <span class="huge-pinyin">{pinyin}</span>
    </div>
    """, unsafe_allow_html=True)

# Zone de révélation / réponse
if not st.session_state.revealed:
    # Bouton RÉVÉLER (dans la carte)
    if st.button("RÉVÉLER", key="reveal_btn"):
        st.session_state.revealed = True
        st.rerun()
    # Espace vide pour garder la taille de la carte
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)

else:
    # Affichage de la réponse
    st.markdown('<div class="answer-label">Answer:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-text">{fr}</div>', unsafe_allow_html=True)

    # Boutons d'action (Rouge / Vert)
    # On utilise st.columns pour les mettre côte à côte DANS la carte
    col_ko, col_ok = st.columns(2)
    with col_ko:
        st.button("❌ À REVOIR", on_click=mark_ko, key="btn_ko")
    with col_ok:
        st.button("✅ MÉMORISÉ", on_click=mark_ok, key="btn_ok")

# Fin du Conteneur "Carte"
st.markdown('</div>', unsafe_allow_html=True)
