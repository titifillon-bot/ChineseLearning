
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
# --- CSS AVANCÉ (Carte Fixe + Boutons collés/alignés) ---
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

/* --- 1. LAYOUT PRINCIPAL --- */
.stApp { background-color: #f0f2f5; }
.main .block-container {
    max-width: 900px;                /* largeur carte + boutons */
    padding-top: 2rem;
    padding-bottom: 5rem;
}

/* --- Progress bar --- */
.stProgress > div > div > div { height: 10px !important; }
div[data-testid="stCaptionContainer"] {
    margin-bottom: -20px;
    text-align: center;
    font-weight: 600;
    color: #6c757d;
}

/* --- 2. LA CARTE (Fixe) --- */
.flashcard-content {
    background-color: #ffffff;
    padding: 20px 30px;
    border-radius: 24px 24px 0 0; /* Arrondi seulement en haut */
    box-shadow: 0 15px 35px rgba(50,50,93,0.1), 0 5px 15px rgba(0,0,0,0.07);
    text-align: center;
    margin-top: 25px;

    height: 450px !important;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    overflow: hidden; position: relative; z-index: 1;
    width: 100%; box-sizing: border-box;
}

/* --- 3. TYPO INTERNE --- */
.mode-indicator {
    position: absolute; top: 30px; left: 0; right: 0;
    font-size: 16px; text-transform: uppercase; letter-spacing: 1.5px;
    color: #adb5bd; font-weight: 700;
}
.content-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; }
.huge-char { font-size: 130px; line-height: 1.2; color: #2c3e50; font-weight: 900; margin: 0; }
.huge-pinyin { font-size: 50px; color: #3498db; font-weight: 700; margin: 5px 0; }
.huge-fr { font-size: 35px; color: #505c6e; font-weight: 600; margin: 5px 0; }

.answer-container {
    background-color: #f8f9fa; border-radius: 16px; padding: 10px 25px;
    margin-top: 15px; min-width: 60%;
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* ========================================================================
   --- 4. STYLISATION DES BOUTONS ---
======================================================================= */

/* Style générique */
.main .stButton button {
    width: 100%;
    border: none !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.main .stButton button:hover { transform: translateY(-3px); box-shadow: 0 15px 25px rgba(0,0,0,0.12); }
.main .stButton button:active { transform: translateY(2px); box-shadow: 0 5px 10px rgba(0,0,0,0.1); }

/* --- Bouton "RÉVÉLER" : même largeur que la carte et collé en bas --- */
/* ⚠️ Descendant (pas '>') pour contourner les wrappers internes de Streamlit */
.main div:not([data-testid="column"]) .stButton button {
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
    color: white !important;
    border-radius: 0 0 24px 24px !important; /* ferme visuellement la carte */
    margin-top: -24px !important;           /* colle au bas arrondi de la carte */
    width: 100% !important;
    height: 160px !important;
    font-size: 45px !important;
    font-weight: 900 !important;
    z-index: 0;
}

/* --- Zone des deux choix : largeur = carte, très petit écart central --- */
.choice-row { width: 100%; box-sizing: border-box; }

/* Réduction du gutter des colonnes exclusivement pour cette rangée */
.choice-row [data-testid="column"] {
    padding-left: 0 !important; padding-right: 0 !important;
}
.choice-row [data-testid="column"]:first-of-type { padding-right: 4px !important; }  /* ~4px de gap central */
.choice-row [data-testid="column"]:last-of-type  { padding-left: 4px !important; }

/* Boutons dans colonnes */
.choice-row .stButton button {
    border-radius: 16px !important;
    height: 100px !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    margin-top: 20px;
}

/* Couleurs spécifiques */
.choice-row [data-testid="column"]:nth-of-type(1) .stButton button {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
    color: white !important;
}
.choice-row [data-testid="column"]:nth-of-type(2) .stButton button {
    background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
    color: white !important;
}

/* Sidebar propre (optionnel) */
.css-1d391kg { background-color: #ffffff; }
.st-emotion-cache-16txtl3 { padding: 2rem 1rem; }
</style>
""", unsafe_allow_html=True)

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

with st.sidebar:
    st.header("🎴 Configuration")
    st.subheader("1. Séries")
    c1, c2 = st.columns(2)
    c1.button("✅ Toutes", key="all_s", on_click=toggle_all_series, args=(True,))
    c2.button("❌ Aucune", key="no_s", on_click=toggle_all_series, args=(False,))
    
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}")

    st.markdown("---")
    st.subheader("2. Modes de jeu")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="all_m", on_click=toggle_all_modes, args=(True,))
    c4.button("❌ Aucun", key="no_m", on_click=toggle_all_modes, args=(False,))
    
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}")

    st.markdown("---")
    if st.button("🚀 LANCER UNE SESSION", type="primary", use_container_width=True):
        start_game()
        rerun()

# --- ZONE PRINCIPALE ---
if not st.session_state.game_active:
    st.markdown("""
        <div style='text-align: center; padding: 50px; color: #6c757d;'>
            <h1>👋 Bienvenue !</h1>
            <p style='font-size: 1.2rem;'>Configure tes séries et tes modes dans la barre latérale,<br>puis clique sur "Lancer une session" pour commencer.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

if st.session_state.current_card is None:
    st.balloons()
    st.markdown("""
        <div style='text-align: center; padding: 50px; background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
            <h1 style='color: #2ecc71; font-size: 3rem;'>Session terminée ! 🎉</h1>
            <p style='font-size: 1.5rem; color: #6c757d;'>Beau travail.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Recommencer une session", type="primary", use_container_width=True):
        st.session_state.game_active = False
        rerun()
    st.stop()

item, mode = st.session_state.current_card
char, pinyin, fr = item
mode_text = GAME_MODES[mode]

# Barre de progression
total = st.session_state.total_cards_initial
restant = len(st.session_state.deck)
progress_val = (total - restant) / total if total > 0 else 0
st.progress(progress_val)
st.caption(f"Progression : {total - restant} / {total}")

# --- PRÉPARATION DU CONTENU HTML ---
q_html = ""
a_html = ""

# Helper pour formater la réponse
def format_answer(top, bottom=None):
    html = f'<div class="answer-container"><div class="{top[1]}">{top[0]}</div>'
    if bottom:
        html += f'<div class="{bottom[1]}">{bottom[0]}</div>'
    html += '</div>'
    return html

if mode == 1: # Pinyin → FR
    q_html = f'<div class="huge-pinyin">{pinyin}</div>'
    a_html = format_answer((char, "huge-char"), (fr, "huge-fr"))
elif mode == 2: # FR → Pinyin
    q_html = f'<div class="huge-fr" style="font-size: 50px;">{fr}</div>'
    a_html = format_answer((char, "huge-char"), (pinyin, "huge-pinyin"))
elif mode == 3: # FR -> Symbole
    q_html = f'<div class="huge-fr" style="font-size: 50px;">{fr}</div>'
    a_html = format_answer((char, "huge-char"), (pinyin, "huge-pinyin"))
elif mode == 4: # Symbole → FR
    q_html = f'<div class="huge-char">{char}</div>'
    a_html = format_answer((pinyin, "huge-pinyin"), (fr, "huge-fr"))
elif mode == 5: # Pinyin -> Symbole
    q_html = f'<div class="huge-pinyin">{pinyin}</div>'
    a_html = format_answer((char, "huge-char"), (fr, "huge-fr"))
elif mode == 6: # Symbole → Pinyin
    q_html = f'<div class="huge-char">{char}</div>'
    a_html = format_answer((pinyin, "huge-pinyin"), (fr, "huge-fr"))

# ================= AFFICHAGE DE LA CARTE =================
with st.container():
    # Carte
    st.markdown(f"""
<div class="flashcard-content">
  <div class="mode-indicator">{mode_text}</div>
  <div class="content-wrapper">
    {q_html}
    {a_html if st.session_state.revealed else ""}
  </div>
</div>
""", unsafe_allow_html=True)

    # Boutons
    if not st.session_state.revealed:
        # Bouton Révéler : largeur carte
        if st.button("👁️ Révéler la réponse", key="btn_reveal", use_container_width=True):
            st.session_state.revealed = True
            rerun()
    else:
        # Deux choix : côte à côte, petit écart central, largeur carte
        choice_wrap = st.container()
        with choice_wrap:
            st.markdown('<div class="choice-row">', unsafe_allow_html=True)
            c_ko, c_ok = st.columns(2, gap="small")
            with c_ko:
                if st.button("❌ À revoir", key="btn_ko", use_container_width=True):
                    mark_review()
                    rerun()
            with c_ok:
                if st.button("✅ Mémorisé", key="btn_ok", use_container_width=True):
                    mark_memorized()
                    rerun()
            st.markdown('</div>', unsafe_allow_html=True)
