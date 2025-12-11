import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Radicaux Chinois", layout="wide")

# --- FONCTION COMPATIBLE RERUN ---
def rerun():
    try:
        st.rerun()
    except AttributeError:
        # Fallback pour anciennes versions de Streamlit
        st.experimental_rerun()

# --- CSS ULTRA-LARGE POUR TABLETTE & AMÉLIORATIONS DE LAYOUT ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

    /* === STYLE DE LA CARTE CENTRALE (La bulle) === */
    .stCard {
        background-color: #ffffff;
        padding: 30px; /* Espace intérieur */
        border-radius: 18px; /* Coins arrondis */
        box-shadow: 0 10px 40px rgba(20,20,30,0.08);
        text-align: center;
        margin: 20px auto;
        max-width: 920px; /* Largeur max de la bulle */
        border: 1px solid #f0f2f6;
    }

    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    /* Centrage explicite du caractère/pinyin (question) */
    .huge-char, .huge-pinyin {
        display: block;
        margin: 8px auto;
        text-align: center;
        line-height: 1.05;
    }

    /* Taille et style des éléments */
    .huge-char { 
        font-size: 140px; 
        color: #1E88E5; 
        font-weight: 900; 
    }
    .huge-pinyin { 
        font-size: 70px; 
        color: #1565C0; 
        font-weight: 700; 
    }

    .question-mode {
        font-size: 22px;
        color: #868e96;
        margin-bottom: 20px;
        font-weight: 600;
        width: 100%;
        text-align: left;
    }

    .answer-text { 
        font-size: 40px; 
        color: #333; 
        background-color: #eef2f7; 
        padding: 28px; 
        border-radius: 14px; 
        margin: 20px 0;
        font-weight: 500;
        width: 100%;
    }

    /* === BOUTONS : uniformisation et taille adaptative === */
    .stCard .stButton > button {
        width: 100% !important; /* prennent la largeur du conteneur (colonne) */
        border-radius: 12px !important;
        height: 78px !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        transition: transform 0.08s ease, filter 0.12s ease;
    }
    .stCard .stButton > button:active { transform: translateY(1px) scale(0.998); }

    /* Reveal (le bouton en single column au milieu de la bulle) */
    .reveal-wrapper { width: 72%; margin: 22px auto 8px auto; }
    .reveal-wrapper .stButton > button { background-color: #1976D2 !important; height:86px !important; font-size:24px !important; }

    /* Row d'actions : colonnes côte à côte occupant toute la largeur de la bulle */
    .action-row > div { padding: 0 8px; } /* léger espacement entre colonnes */
    .action-row .stButton > button { height:86px !important; font-size:20px !important; }

    /* Couleurs remplies pour les 2 boutons d'action (gauche = rouge, droite = vert) */
    /* On cible la structure générée par st.columns lorsqu'elle est à l'intérieur de .action-row */
    .action-row > div:nth-child(1) .stButton > button { background-color: #D32F2F !important; }
    .action-row > div:nth-child(2) .stButton > button { background-color: #388E3C !important; }

    /* Ajustement des checkboxes pour la tablette */
    .stCheckbox label { font-size: 20px !important; padding: 10px 0; }

    /* Responsive: réduire un peu les tailles sur petits écrans */
    @media (max-width: 800px) {
        .huge-char { font-size: 90px; }
        .huge-pinyin { font-size: 36px; }
        .reveal-wrapper { width: 92%; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DONNÉES COMPLÈTES ---
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

GAME_MODES = {
    1: "Pinyin → FR", 2: "FR → Pinyin", 3: "FR -> Symbole",
    4: "Symbole → FR", 5: "Pinyin -> Symbole", 6: "Symbole → Pinyin"
}

# --- INITIALISATION ÉTAT ---
if 'deck' not in st.session_state: st.session_state.deck = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'revealed' not in st.session_state: st.session_state.revealed = False
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'total_cards_initial' not in st.session_state: st.session_state.total_cards_initial = 0

for k in st.session_state.all_data.keys():
    if f"chk_serie_{k}" not in st.session_state: st.session_state[f"chk_serie_{k}"] = True
for k in GAME_MODES.keys():
    if f"chk_mode_{k}" not in st.session_state: st.session_state[f"chk_mode_{k}"] = True

# --- FONCTIONS LOGIQUES ---
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
        st.session_state.deck.append(card)
    next_card()

# ================= INTERFACE =================

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. SÉRIES")
    c1, c2 = st.columns(2)
    c1.button("✅ Tous", key="all_s", on_click=toggle_all_series, args=(True,))
    c2.button("❌ Aucun", key="no_s", on_click=toggle_all_series, args=(False,))
    
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}")

    st.markdown("---")
    st.header("2. MODES")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="all_m", on_click=toggle_all_modes, args=(True,))
    c4.button("❌ Aucun", key="no_m", on_click=toggle_all_modes, args=(False,))
    
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}")

    st.markdown("---")
    if st.button("🚀 LANCER LE JEU"):
        start_game()
        rerun()

# --- ZONE PRINCIPALE ---
if not st.session_state.game_active:
    st.info("👈 Configure et lance le jeu depuis la barre latérale.")
    st.stop()

if st.session_state.current_card is None:
    st.balloons()
    st.success("🎉 Session terminée ! 🎉")
    if st.button("Recommencer"):
        st.session_state.game_active = False
        rerun()
    st.stop()

item, mode = st.session_state.current_card
char, pinyin, fr = item
mode_text = GAME_MODES[mode]

# Barre de progression
total = st.session_state.total_cards_initial
restant = len(st.session_state.deck)
st.progress((total - restant) / total if total > 0 else 0)
st.caption(f"Progression : {total - restant}/{total}")

# --- CARTE PRINCIPALE (LA BULLE) ---
# On ouvre la bulle ici et on la garde ouverte pour inclure les boutons (permet un alignement parfait)
st.markdown('<div class="stCard"><div class="centered-content">', unsafe_allow_html=True)
st.markdown(f'<div class="question-mode">{mode_text}</div>', unsafe_allow_html=True)

# Contenu HTML (Question/Réponse)
q_html = ""
a_html = ""
# Logique d'affichage (taille HUGE)
if mode == 1: # Pinyin -> FR
    q_html = f'<span class="huge-pinyin">{pinyin}</span>'
    a_html = f'{fr}<br><span class="huge-char">{char}</span>'
elif mode == 2: # FR -> Pinyin
    q_html = f'<span class="huge-pinyin" style="font-size:50px; color:#333">{fr}</span>'
    a_html = f'{pinyin}<br><span class="huge-char">{char}</span>'
elif mode == 3: # FR -> Symbole
    q_html = f'<span class="huge-pinyin" style="font-size:50px; color:#333">{fr}</span>'
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

# AFFICHER LA QUESTION (Centrée dans la bulle)
st.markdown(q_html, unsafe_allow_html=True)

# --- ZONE ACTIONS DANS LA BULLE ---
if not st.session_state.revealed:
    # Bouton RÉVÉLER : on le place à l'intérieur d'une wrapper pour contrôler sa largeur (égale à la bulle)
    st.markdown('<div class="reveal-wrapper">', unsafe_allow_html=True)
    if st.button("👁️ RÉVÉLER"):
        st.session_state.revealed = True
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # AFFICHER LA RÉPONSE (toujours dans la bulle)
    st.markdown(f'<div class="answer-text">{a_html}</div>', unsafe_allow_html=True)
    
    # Boutons Validation (Côte à côte, occupent la largeur de la bulle)
    st.markdown('<div class="action-row" style="width:100%; margin-top:8px;">', unsafe_allow_html=True)
    c_ko, c_ok = st.columns(2)
    with c_ko:
        if st.button("❌ À REVOIR", key="btn_ko"):
            mark_review()
            rerun()
    with c_ok:
        if st.button("✅ MÉMORISÉ", key="btn_ok"):
            mark_memorized()
            rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Fermer la bulle
st.markdown('</div></div>', unsafe_allow_html=True)
