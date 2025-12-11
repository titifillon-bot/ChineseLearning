import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Radicaux Chinois", layout="wide")

# --- FONCTION COMPATIBLE RERUN ---
def rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- CSS ROBUSTE (Pour le look "Carte" et les couleurs) ---
st.markdown("""
    <style>
    /* Import de police jolie */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }

    /* === STYLE DE LA CARTE CENTRALE === */
    .stCard {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px auto;
        max-width: 800px;
        border: 1px solid #e0e0e0;
    }

    /* Gros texte pour le caractère */
    .huge-char { 
        font-size: 120px; 
        color: #1E88E5; 
        font-weight: bold; 
        line-height: 1.2;
        display: block;
    }
    
    /* Gros texte pour le pinyin */
    .huge-pinyin { 
        font-size: 60px; 
        color: #1565C0; 
        font-weight: bold; 
        margin-bottom: 20px;
        display: block;
    }

    /* Texte de réponse */
    .answer-text { 
        font-size: 35px; 
        color: #333; 
        background-color: #f5f5f5; 
        padding: 20px; 
        border-radius: 10px; 
        margin: 20px 0;
        font-weight: 500;
    }

    /* === STYLE DES BOUTONS === */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 60px;
        font-size: 20px;
        font-weight: bold;
        border: none;
        transition: transform 0.1s;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* --- COULEURS DES BOUTONS (Ciblage par position) --- */
    
    /* Dans la SIDEBAR : Colonne de gauche (Boutons "Tous" -> VERT) */
    [data-testid="stSidebar"] [data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #4CAF50; 
        color: white;
    }
    
    /* Dans la SIDEBAR : Colonne de droite (Boutons "Aucun" -> ROUGE) */
    [data-testid="stSidebar"] [data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #EF5350; 
        color: white;
    }

    /* Dans la ZONE PRINCIPALE (Réponse) : Colonne de gauche (À REVOIR -> ROUGE) */
    [data-testid="stVerticalBlock"] [data-testid="column"]:nth-of-type(1) div.stButton > button {
        background-color: #EF5350; 
        color: white;
        height: 80px; /* Plus haut pour faciliter le clic */
        font-size: 24px;
    }

    /* Dans la ZONE PRINCIPALE (Réponse) : Colonne de droite (MÉMORISÉ -> VERT) */
    [data-testid="stVerticalBlock"] [data-testid="column"]:nth-of-type(2) div.stButton > button {
        background-color: #66BB6A; 
        color: white;
        height: 80px;
        font-size: 24px;
    }
    
    /* Bouton REVELER (Bleu) */
    div.stButton > button.reveal-btn {
        background-color: #E3F2FD;
        color: #1976D2;
    }

    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES COMPLÈTES (Tes 100 radicaux) ---
if 'all_data' not in st.session_state:
    st.session_state.all_data = {
        "1-10": [
            ("人", "rén", "Homme / Personne (Rad9)"), ("口", "kǒu", "Bouche (Rad30)"),
            ("土", "tǔ", "Terre / Sol (Rad32)"), ("女", "nǚ", "Femme (Rad38)"),
            ("心", "xīn", "Cœur / Esprit (Rad61)"), ("手", "shǒu", "Main (Rad64)"),
            ("日", "rì", "Soleil / Jour (Rad72)"), ("月", "yuè", "Lune / Mois (Rad74)"),
            ("木", "mù", "Arbre / Bois (Rad75)"), ("氵", "shuǐ", "Eau (Rad85)"),
        ],
        "11-20": [
            ("火", "huǒ", "Feu (Rad86)"), ("纟", "mì, sī", "Soie (Rad120 var)"),
            ("糸", "mì", "Soie (Rad120)"), ("艹", "cǎo", "Herbe (Rad140 var)"),
            ("讠", "yán", "Parole (Rad149 var)"), ("辶", "chuò", "Marche / Aller (Rad162)"),
            ("金", "jīn", "Or / Métal (Rad167)"), ("刂", "dāo", "Couteau (Rad18 vert)"),
            ("宀", "mián", "Toit (Rad40)"), ("贝", "bèi", "Coquillage (Rad154)"),
            ("一", "yī", "Un / Une (Rad1)"),
        ],
        "21-30": [
            ("力", "lì", "Force (Rad19)"), ("又", "yòu", "Encore (Rad29)"),
            ("犭", "quǎn", "Chien (Rad94 var)"), ("禾", "hé", "Grain (Rad115)"),
            ("⺮", "zhú", "Bambou (Rad118 var)"), ("虫", "chóng", "Insecte (Rad142)"),
            ("阝", "fù, yì", "Tertre/Ville"), ("大", "dà, dài", "Grand (Rad37)"),
            ("广", "guǎng", "Toit pente (Rad53)"), ("田", "tián", "Champ (Rad102)"),
        ],
        "31-40": [
            ("目", "mù", "Œil"), ("石", "shí", "Pierre"), ("礻", "yì", "Vêtement"),
            ("足", "zú", "Pied"), ("马", "mǎ", "Cheval"), ("页", "yè", "Page"),
            ("巾", "jīn", "Tissu"), ("米", "mǐ", "Riz"), ("车", "chē", "Voiture"),
            ("八", "bā", "Huit"),
        ],
        "41-50": [
            ("尸", "shī", "Cadavre"), ("寸", "cùn", "Pouce"), ("山", "shān", "Montagne"),
            ("攵", "pū", "Frapper"), ("彳", "chì", "Pas (gauche)"), ("十", "shí", "Dix"),
            ("工", "gōng", "Travail"), ("方", "fāng", "Carré"), ("门", "mén", "Porte"),
            ("饣", "shí", "Manger"),
        ],
        "51-60": [
            ("欠", "qiàn", "Bâiller"), ("儿", "ér", "Fils"), ("冫", "bīng", "Glace"),
            ("子", "zǐ", "Enfant"), ("疒", "chuáng", "Maladie"), ("隹", "zhuī", "Oiseau"),
            ("斤", "jīn", "Hache"), ("亠", "tóu", "Couvercle"), ("王", "wáng", "Roi"),
            ("白", "bái", "Blanc"),
        ],
        "61-70": [
            ("立", "lì", "Debout"), ("羊", "yáng", "Mouton"), ("艮", "gěn", "Montagne/Tenace"),
            ("冖", "mì", "Toit"), ("厂", "chǎng", "Usine"), ("皿", "mǐn", "Récipient"),
            ("礻", "shì", "Esprit"), ("穴", "xué", "Trou"), ("走", "zǒu", "Marcher"),
            ("雨", "yǔ", "Pluie"),
        ],
        "71-80": [
            ("囗", "wéi", "Enceinte"), ("小", "xiǎo", "Petit"), ("戈", "gē", "Hallebarde"),
            ("几", "jī", "Combien/Table"), ("舌", "shé", "Langue"), ("干", "gān", "Sec"),
            ("殳", "shū", "Lance"), ("夕", "xī", "Coucher soleil"), ("止", "zhǐ", "Arrêter"),
            ("牛", "niú", "Vache"),
        ],
        "81-90": [
            ("皮", "pí", "Peau"), ("耳", "ěr", "Oreille"), ("辛", "xīn", "Amer"),
            ("酉", "yǒu", "Vin"), ("青", "qīng", "Bleu-Vert"), ("鸟", "niǎo", "Oiseau"),
            ("弓", "gōng", "Arc"), ("厶", "sī", "Privé"), ("户", "hù", "Foyer"),
        ],
        "91-100": [
            ("羽", "yǔ", "Plume"), ("舟", "zhōu", "Bateau"), ("里", "lǐ", "Intérieur"),
            ("匕", "bǐ", "Cuillère"), ("夂", "suī", "Aller doucement"), ("见", "jiàn", "Voir"),
            ("卩", "jié", "Sceau"), ("罒", "wǎng", "Filet"), ("士", "shì", "Erudit"),
            ("勹", "bāo", "Envelopper"),
        ]
    }

# --- MODES DE JEU ---
GAME_MODES = {
    1: "Pinyin → FR", 2: "FR → Pinyin", 3: "FR → Symbole",
    4: "Symbole → FR", 5: "Pinyin → Symbole", 6: "Symbole → Pinyin"
}

# --- ETAT (SESSION STATE) ---
if 'deck' not in st.session_state: st.session_state.deck = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'revealed' not in st.session_state: st.session_state.revealed = False
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'total_cards_initial' not in st.session_state: st.session_state.total_cards_initial = 0

# Checkbox states (initialisation)
for k in st.session_state.all_data.keys():
    if f"chk_serie_{k}" not in st.session_state: st.session_state[f"chk_serie_{k}"] = True
for k in GAME_MODES.keys():
    if f"chk_mode_{k}" not in st.session_state: st.session_state[f"chk_mode_{k}"] = True

# --- LOGIQUE ---

def toggle_all_series(state):
    for k in st.session_state.all_data.keys():
        st.session_state[f"chk_serie_{k}"] = state

def toggle_all_modes(state):
    for k in GAME_MODES.keys():
        st.session_state[f"chk_mode_{k}"] = state

def start_game():
    deck = []
    series_to_use = [k for k in st.session_state.all_data.keys() if st.session_state[f"chk_serie_{k}"]]
    modes_to_use = [k for k in GAME_MODES.keys() if st.session_state[f"chk_mode_{k}"]]
    
    if not series_to_use:
        st.sidebar.error("⚠️ Choisis au moins une série !")
        return
    if not modes_to_use:
        st.sidebar.error("⚠️ Choisis au moins un mode !")
        return

    # Construction du paquet
    for serie_key in series_to_use:
        for item in st.session_state.all_data[serie_key]:
            for m in modes_to_use:
                deck.append((item, m))
    
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.total_cards_initial = len(deck)
    st.session_state.game_active = True
    st.session_state.revealed = False
    next_card()

def next_card():
    st.session_state.revealed = False
    if len(st.session_state.deck) > 0:
        st.session_state.current_card = st.session_state.deck[0]
    else:
        st.session_state.current_card = None
        st.session_state.game_active = False

def mark_memorized():
    if st.session_state.deck: st.session_state.deck.pop(0)
    next_card()

def mark_review():
    if st.session_state.deck:
        card = st.session_state.deck.pop(0)
        st.session_state.deck.append(card) # On remet à la fin
    next_card()

# --- INTERFACE ---

# 1. SIDEBAR
with st.sidebar:
    st.header("1. CHOIX DES SÉRIES")
    c1, c2 = st.columns(2)
    c1.button("✅ Tous", key="all_s", on_click=toggle_all_series, args=(True,))
    c2.button("❌ Aucun", key="no_s", on_click=toggle_all_series, args=(False,))
    
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}")

    st.markdown("---")
    st.header("2. CHOIX DES MODES")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="all_m", on_click=toggle_all_modes, args=(True,))
    c4.button("❌ Aucun", key="no_m", on_click=toggle_all_modes, args=(False,))
    
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}")

    st.markdown("---")
    if st.button("🚀 LANCER LE JEU", type="primary"):
        start_game()
        rerun()

# 2. ZONE PRINCIPALE
if not st.session_state.game_active:
    st.info("👈 Configure tes options à gauche et clique sur **LANCER LE JEU**.")
    st.stop()

if st.session_state.current_card is None:
    st.balloons()
    st.success("BRAVO ! Session terminée !")
    if st.button("Recommencer"):
        st.session_state.game_active = False
        rerun()
    st.stop()

# --- AFFICHAGE DE LA CARTE ---
item, mode = st.session_state.current_card
char, pinyin, fr = item
mode_text = GAME_MODES[mode]

# Barre de progression
total = st.session_state.total_cards_initial
restant = len(st.session_state.deck)
st.progress((total - restant) / total if total > 0 else 0)
st.caption(f"Cartes restantes : {restant} / {total}")

# --- CONTENEUR CARTE (HTML) ---
st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.markdown(f'<div style="font-size: 20px; color: #777; margin-bottom: 20px;">Question : {mode_text}</div>', unsafe_allow_html=True)

# Contenu de la question (HTML généré selon le mode)
q_html = ""
a_html = ""

# Logique d'affichage selon le mode (On garde le style "Huge")
if mode == 1: # Pinyin -> FR
    q_html = f'<span class="huge-pinyin">{pinyin}</span>'
    a_html = f'{fr}<br><span class="huge-char">{char}</span>'
elif mode == 2: # FR -> Pinyin
    q_html = f'<span class="huge-pinyin" style="font-size:40px; color:#333">{fr}</span>'
    a_html = f'{pinyin}<br><span class="huge-char">{char}</span>'
elif mode == 3: # FR -> Symbole
    q_html = f'<span class="huge-pinyin" style="font-size:40px; color:#333">{fr}</span>'
    a_html = f'<span class="huge-char">{char}</span><br>{pinyin}'
elif mode == 4: # Symbole -> FR
    q_html = f'<span class="huge-char">{char}</span>'
    a_html = f'{fr}<br>{pinyin}'
elif mode == 5: # Pinyin -> Symbole
    q_html = f'<span class="huge-pinyin">{pinyin}</span>'
    a_html = f'<span class="huge-char">{char}</span><br>{fr}'
elif mode == 6: # Symbole -> Pinyin
    q_html = f'<span class="huge-char">{char}</span>'
    a_html = f'{pinyin}<br>{fr}'

# Affichage Question
st.markdown(q_html, unsafe_allow_html=True)

# --- ZONE ACTIONS ---
if not st.session_state.revealed:
    # Espace vide pour aérer
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    # Bouton Révéler
    if st.button("👁️ RÉVÉLER LA RÉPONSE"):
        st.session_state.revealed = True
        rerun()
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

else:
    # Affichage Réponse
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="answer-text">{a_html}</div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    # Boutons Validation (Colonnes pour le CSS rouge/vert)
    col_ko, col_ok = st.columns(2)
    with col_ko:
        if st.button("❌ À REVOIR", key="btn_ko"):
            mark_review()
            rerun()
    with col_ok:
        if st.button("✅ MÉMORISÉ", key="btn_ok"):
            mark_memorized()
            rerun()

st.markdown('</div>', unsafe_allow_html=True) # Fin stCard
