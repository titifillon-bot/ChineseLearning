import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Radicaux Chinois", layout="wide", initial_sidebar_state="expanded")

# --- FONCTION COMPATIBLE RERUN ---
def rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# ==============================================================================
# --- CSS ROBUSTE (CORRIGÉ POUR ÉCRASER LES STYLES PAR DÉFAUT) ---
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap');
    
    /* Appliquer la police partout */
    html, body, [class*="css"], button, input {
        font-family: 'Nunito', sans-serif !important;
    }

    /* --- 1. FOND ET CONTENEUR --- */
    .stApp {
        background-color: #f0f2f5;
    }

    /* Centrer et limiter la largeur de la zone principale */
    .main .block-container {
        max-width: 800px;  /* Largeur fixe idéale pour une flashcard */
        padding-top: 2rem;
        padding-bottom: 5rem;
        margin: 0 auto;    /* Centrage horizontal */
    }

    /* --- 2. LA CARTE (Cadre blanc) --- */
    .flashcard-content {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 24px 24px 0 0; /* Arrondi haut */
        box-shadow: 0 -10px 25px rgba(0,0,0,0.05); /* Ombre légère */
        text-align: center;
        margin-top: 20px;
        
        /* HAUTEUR FIXE POUR ÉVITER LES SAUTS */
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        border-bottom: 1px solid #eee;
    }

    /* --- 3. TYPOGRAPHIE --- */
    .mode-indicator {
        position: absolute;
        top: 20px;
        left: 0; right: 0;
        text-align: center;
        font-size: 14px;
        font-weight: 700;
        color: #adb5bd;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .huge-char { font-size: 120px; line-height: 1.2; color: #2c3e50; font-weight: 900; }
    .huge-pinyin { font-size: 48px; color: #3498db; font-weight: 700; margin-bottom: 10px; }
    .huge-fr { font-size: 32px; color: #505c6e; font-weight: 600; }

    /* Zone réponse grisée */
    .answer-container {
        background-color: #f8f9fa;
        padding: 15px 30px;
        border-radius: 12px;
        margin-top: 15px;
        animation: fadeIn 0.4s ease;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* ========================================================================
       --- 4. BOUTONS (LA PARTIE IMPORTANTE) ---
    ======================================================================== */
    
    /* Ciblage très large pour forcer le style sur tous les boutons principaux */
    .stButton button {
        width: 100%;
        border: none !important;
        outline: none !important;
        color: white !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: transform 0.1s ease, box-shadow 0.1s ease !important;
    }
    
    .stButton button:active {
        transform: scale(0.98);
    }

    /* --- LE BOUTON "RÉVÉLER" (Bleu) --- */
    /* On utilise une astuce : le bouton qui est seul dans sa rangée */
    div[data-testid="stVerticalBlock"] > div > .stButton button {
        height: 100px !important;       /* Hauteur fixe */
        font-size: 28px !important;     /* Gros texte */
        border-radius: 0 0 24px 24px !important; /* Arrondi bas seulement */
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3) !important;
        margin-top: -18px !important;   /* REMONTE LE BOUTON POUR LE COLLER À LA CARTE */
        z-index: 1;
    }

    /* --- LES BOUTONS DE CHOIX (Rouge/Vert) --- */
    /* Ceux-ci sont dans des colonnes */
    div[data-testid="column"] .stButton button {
        height: 80px !important;
        font-size: 20px !important;
        border-radius: 16px !important;
        margin-top: 20px !important; /* Espace normal */
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
    }

    /* Bouton À REVOIR (Colonne 1) */
    div[data-testid="column"]:nth-of-type(1) .stButton button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5253 100%) !important;
    }

    /* Bouton MÉMORISÉ (Colonne 2) */
    div[data-testid="column"]:nth-of-type(2) .stButton button {
        background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%) !important;
    }

    /* Nettoyage interface */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stProgress > div > div > div { height: 8px !important; background-color: #3498db; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DONNÉES ---
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

# --- ETAT ---
if 'deck' not in st.session_state: st.session_state.deck = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'revealed' not in st.session_state: st.session_state.revealed = False
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'total_cards_initial' not in st.session_state: st.session_state.total_cards_initial = 0

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
    
    if not series_to_use or not modes_to_use:
        st.sidebar.error("⚠️ Sélectionne au moins une série et un mode.")
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

# --- SIDEBAR ---
with st.sidebar:
    st.title("🀄 Paramètres")
    st.markdown("---")
    st.subheader("Séries")
    c1, c2 = st.columns(2)
    c1.button("✅ Toutes", key="all_s", on_click=toggle_all_series, args=(True,))
    c2.button("❌ Aucune", key="no_s", on_click=toggle_all_series, args=(False,))
    
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}")

    st.markdown("---")
    st.subheader("Modes")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="all_m", on_click=toggle_all_modes, args=(True,))
    c4.button("❌ Aucun", key="no_m", on_click=toggle_all_modes, args=(False,))
    
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}")

    st.markdown("---")
    if st.button("LANCER LA SESSION", type="primary", use_container_width=True):
        start_game()
        rerun()

# --- MAIN PAGE ---
if not st.session_state.game_active:
    st.markdown("<br><br><h2 style='text-align: center; color: #7f8c8d;'>Configure et lance une session via le menu latéral 👈</h2>", unsafe_allow_html=True)
    st.stop()

if st.session_state.current_card is None:
    st.balloons()
    st.markdown("<br><br><h1 style='text-align: center; color: #27ae60;'>🎉 Terminé !</h1>", unsafe_allow_html=True)
    if st.button("Recommencer", type="primary", use_container_width=True):
        st.session_state.game_active = False
        rerun()
    st.stop()

# --- PRÉPARATION DU CONTENU ---
item, mode = st.session_state.current_card
char, pinyin, fr = item
mode_text = GAME_MODES[mode]

# Progression
total = st.session_state.total_cards_initial
restant = len(st.session_state.deck)
st.progress((total - restant) / total if total > 0 else 0)
st.caption(f"Cartes restantes : {restant}")

# Génération HTML propre (variable python)
q_div = ""
a_div = ""

def make_answer(top_text, top_cls, bot_text=None, bot_cls=None):
    html = f'<div class="answer-container"><div class="{top_cls}">{top_text}</div>'
    if bot_text:
        html += f'<div class="{bot_cls}">{bot_text}</div>'
    html += '</div>'
    return html

if mode == 1: # Pinyin → FR
    q_div = f'<div class="huge-pinyin">{pinyin}</div>'
    a_div = make_answer(char, "huge-char", fr, "huge-fr")
elif mode == 2: # FR → Pinyin
    q_div = f'<div class="huge-fr">{fr}</div>'
    a_div = make_answer(char, "huge-char", pinyin, "huge-pinyin")
elif mode == 3: # FR -> Symbole
    q_div = f'<div class="huge-fr">{fr}</div>'
    a_div = make_answer(char, "huge-char", pinyin, "huge-pinyin")
elif mode == 4: # Symbole → FR
    q_div = f'<div class="huge-char">{char}</div>'
    a_div = make_answer(pinyin, "huge-pinyin", fr, "huge-fr")
elif mode == 5: # Pinyin -> Symbole
    q_div = f'<div class="huge-pinyin">{pinyin}</div>'
    a_div = make_answer(char, "huge-char", fr, "huge-fr")
elif mode == 6: # Symbole → Pinyin
    q_div = f'<div class="huge-char">{char}</div>'
    a_div = make_answer(pinyin, "huge-pinyin", fr, "huge-fr")

# --- RENDU DE LA CARTE ---
# Construction de la chaîne HTML EN UNE SEULE FOIS pour éviter le bug </div>
final_html = f"""
<div class="flashcard-content">
    <div class="mode-indicator">{mode_text}</div>
    {q_div}
    {a_div if st.session_state.revealed else ""}
</div>
"""
st.markdown(final_html, unsafe_allow_html=True)

# --- BOUTONS D'ACTION ---
# On place les boutons juste après le markdown. Le CSS (margin-top négatif) va les remonter.

if not st.session_state.revealed:
    # Le CSS cible ce bouton unique pour le rendre bleu et collé
    if st.button("👁️ RÉVÉLER LA RÉPONSE", key="reveal_btn"):
        st.session_state.revealed = True
        rerun()
else:
    # Colonnes pour les choix
    c1, c2 = st.columns(2)
    with c1:
        if st.button("❌ À REVOIR", key="ko_btn"):
            mark_review()
            rerun()
    with c2:
        if st.button("✅ MÉMORISÉ", key="ok_btn"):
            mark_memorized()
            rerun()
