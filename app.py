import streamlit as st
import random

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Radicaux Chinois", layout="centered")

# --- CSS PERSONNALISÉ (POUR TABLETTE) ---
st.markdown("""
    <style>
    /* Gros texte pour la question */
    .huge-font { 
        font-size: 80px !important; 
        font-weight: bold; 
        text-align: center; 
        color: #1E88E5; 
        margin: 10px 0;
    }
    /* Texte moyen pour la réponse */
    .answer-text { 
        font-size: 40px !important; 
        color: #333; 
        text-align: center; 
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* === STYLE DES BOUTONS === */
    div.stButton > button {
        width: 100% !important;  /* Force la largeur maximale */
        height: 100px;           /* Hauteur confortable pour le pouce */
        font-size: 28px;         /* Texte plus gros */
        font-weight: bold;
        border-radius: 12px;     /* Coins arrondis */
    }
    
    /* Couleur spécifique pour le bouton À Revoir (Rouge) si besoin d'override */
    /* Streamlit gère ça via les keys, mais on assure la taille ici */
    </style>
    """, unsafe_allow_html=True)

# --- 1. DONNÉES ---
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
    1: "Pinyin -> FR", 2: "FR -> Pinyin", 3: "FR -> Symbole",
    4: "Symbole -> FR", 5: "Pinyin -> Symbole", 6: "Symbole -> Pinyin"
}

# --- GESTION ÉTAT (Session State) ---
if 'deck' not in st.session_state: st.session_state.deck = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'revealed' not in st.session_state: st.session_state.revealed = False
if 'game_active' not in st.session_state: st.session_state.game_active = False

# Gestion des cases à cocher (Séries)
if 'selected_series_keys' not in st.session_state:
    st.session_state.selected_series_keys = []
# Gestion des cases à cocher (Modes)
if 'selected_modes_keys' not in st.session_state:
    st.session_state.selected_modes_keys = list(GAME_MODES.keys())

# --- LOGIQUE DU JEU ---
def start_game():
    deck = []
    series_to_use = [k for k in st.session_state.all_data.keys() if st.session_state.get(f"chk_serie_{k}", False)]
    modes_to_use = [k for k in GAME_MODES.keys() if st.session_state.get(f"chk_mode_{k}", False)]
    
    if not series_to_use:
        st.error("⚠️ Il faut choisir au moins une série !")
        return
    if not modes_to_use:
        st.error("⚠️ Il faut choisir au moins un mode !")
        return

    # Construction du deck
    for serie_key in series_to_use:
        for item in st.session_state.all_data[serie_key]:
            for m in modes_to_use:
                deck.append((item, m))
    
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.game_active = True
    st.session_state.revealed = False
    next_card()

def next_card():
    if len(st.session_state.deck) > 0:
        st.session_state.current_card = st.session_state.deck[0]
        st.session_state.revealed = False
    else:
        st.session_state.current_card = None
        st.session_state.game_active = False

def mark_memorized():
    if st.session_state.deck:
        st.session_state.deck.pop(0) 
    next_card()

def mark_review():
    if st.session_state.deck:
        card = st.session_state.deck.pop(0)
        st.session_state.deck.append(card)
    next_card()

def toggle_all_series(state):
    keys = list(st.session_state.all_data.keys())
    for k in keys:
        st.session_state[f"chk_serie_{k}"] = state

def toggle_all_modes(state):
    keys = list(GAME_MODES.keys())
    for k in keys:
        st.session_state[f"chk_mode_{k}"] = state

# --- INTERFACE GRAPHIQUE ---

st.title("🀄 Radicaux Flashcards")

# === BARRE LATÉRALE : CONFIGURATION ===
with st.sidebar:
    st.header("1. CHOIX DES SÉRIES")
    
    c1, c2 = st.columns(2)
    if c1.button("✅ Tous", key="all_s"): toggle_all_series(True)
    if c2.button("❌ Aucun", key="no_s"): toggle_all_series(False)
    
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}")

    st.markdown("---")
    st.header("2. CHOIX DES MODES")
    
    c3, c4 = st.columns(2)
    if c3.button("✅ Tous", key="all_m"): toggle_all_modes(True)
    if c4.button("❌ Aucun", key="no_m"): toggle_all_modes(False)
    
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}", value=True)

    st.markdown("---")
    if st.button("🚀 LANCER LE JEU", type="primary"):
        start_game()
        st.rerun()

    if st.session_state.game_active:
        st.info(f"Cartes restantes : {len(st.session_state.deck)}")

# === ZONE PRINCIPALE : LE JEU ===

if not st.session_state.game_active:
    st.info("👈 Configure tes listes à gauche et clique sur **LANCER LE JEU**.")
    st.stop()

if st.session_state.current_card is None:
    st.balloons()
    st.success("BRAVO ! C'est terminé.")
    if st.button("Recommencer une session"):
        st.session_state.game_active = False
        st.rerun()
    st.stop()

# --- AFFICHAGE DE LA CARTE ---
item, mode = st.session_state.current_card
char, pinyin, fr = item
mode_text = GAME_MODES[mode]

st.caption(f"Question : {mode_text}")

question_html = ""
answer_html = ""

if mode == 1: # Pin -> Fr
    question_html = pinyin
    answer_html = f"{fr}<br><span style='font-size:50px; color:#1E88E5'>{char}</span>"
elif mode == 2: # Fr -> Pin
    question_html = fr
    answer_html = f"{pinyin}<br><span style='font-size:50px; color:#1E88E5'>{char}</span>"
elif mode == 3: # Fr -> Sym
    question_html = fr
    answer_html = f"<span style='font-size:80px; color:#1E88E5'>{char}</span><br>{pinyin}"
elif mode == 4: # Sym -> Fr
    question_html = char
    answer_html = f"{fr}<br>{pinyin}"
elif mode == 5: # Pin -> Sym
    question_html = pinyin
    answer_html = f"<span style='font-size:80px; color:#1E88E5'>{char}</span><br>{fr}"
elif mode == 6: # Sym -> Pin
    question_html = char
    answer_html = f"{pinyin}<br>{fr}"

# 1. QUESTION
st.markdown(f'<div class="huge-font">{question_html}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 2. LOGIQUE BOUTONS
if not st.session_state.revealed:
    # Bouton unique RÉVÉLER (Largeur 100% auto via CSS)
    if st.button("👁️ RÉVÉLER LA RÉPONSE"):
        st.session_state.revealed = True
        st.rerun()
else:
    # Affichage RÉPONSE
    st.markdown(f'<div class="answer-text">{answer_html}</div>', unsafe_allow_html=True)
    
    # Deux colonnes avec un espace MINIMUM (gap="small") pour maximiser la largeur
    c_left, c_right = st.columns([1, 1], gap="small")
    
    with c_left:
        # Bouton ROUGE
        if st.button("❌ À REVOIR", key="btn_review"):
            mark_review()
            st.rerun()
            
    with c_right:
        # Bouton VERT
        if st.button("✅ MÉMORISÉ", type="primary", key="btn_ok"):
            mark_memorized()
            st.rerun()
