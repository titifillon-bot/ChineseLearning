import streamlit as st
import random
import json
from pathlib import Path

# --- CONFIG PAGE ---
st.set_page_config(page_title="Radicaux Chinois", layout="wide", initial_sidebar_state="expanded")

# --- FILES ---
FAV_FILE = Path("favoris.json")
SESSION_FILE = Path("session.json")

# --- RERUN ---
def rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- FAVORIS: LOAD/SAVE ---
def load_favorites_from_disk():
    if FAV_FILE.exists():
        try:
            data = json.loads(FAV_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                st.session_state.favorites = data
        except Exception as e:
            st.sidebar.warning(f"Favoris: impossible de charger: {e}")

def save_favorites_to_disk():
    try:
        FAV_FILE.write_text(json.dumps(st.session_state.favorites, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        st.sidebar.warning(f"Favoris: impossible d'écrire: {e}")

# --- SESSION: LOAD/SAVE ---
def load_session_from_disk(show_toast: bool = False):
    if SESSION_FILE.exists():
        try:
            data = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            st.session_state.deck = [
                ((d["char"], d["pinyin"], d["fr"]), d["mode"]) for d in data.get("deck", [])
            ]
            st.session_state.current_card = st.session_state.deck[0] if st.session_state.deck else None
            st.session_state.revealed = bool(data.get("revealed", False))
            st.session_state.game_active = bool(data.get("game_active", False))
            st.session_state.total_cards_initial = int(data.get("total_cards_initial", len(st.session_state.deck)))
            st.session_state.use_favorites_only = bool(data.get("use_favorites_only", False))
            # restaure checkboxes
            for k, v in data.get("series_flags", {}).items():
                st.session_state[k] = bool(v)
            for k, v in data.get("mode_flags", {}).items():
                st.session_state[k] = bool(v)
            if show_toast and not st.session_state.get("_toast_restored_shown", False):
                st.toast("🧯 Session restaurée", icon="✅")
                st.session_state._toast_restored_shown = True
        except Exception as e:
            st.sidebar.warning(f"Session: impossible de charger: {e}")

def save_session_to_disk():
    try:
        payload = {
            "deck": [
                {"char": it[0][0], "pinyin": it[0][1], "fr": it[0][2], "mode": it[1]}
                for it in st.session_state.deck
            ],
            "revealed": st.session_state.get("revealed", False),
            "game_active": st.session_state.get("game_active", False),
            "total_cards_initial": st.session_state.get("total_cards_initial", 0),
            "use_favorites_only": st.session_state.get("use_favorites_only", False),
            "series_flags": {f"chk_serie_{k}": st.session_state.get(f"chk_serie_{k}", True) for k in st.session_state.all_data.keys()},
            "mode_flags": {f"chk_mode_{k}": st.session_state.get(f"chk_mode_{k}", True) for k in GAME_MODES.keys()},
        }
        SESSION_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        st.sidebar.warning(f"Session: impossible d'écrire: {e}")

# --- CSS (CORRECTION HAUTEUR & PLACEMENT) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

/* Layout général */
.stApp { background-color: #f0f2f5; }
.main .block-container { max-width: 900px; padding-top: 1rem; padding-bottom: 5rem; }

/* Progression */
.stProgress > div > div > div { height: 10px !important; }
div[data-testid="stCaptionContainer"] { margin-bottom: -10px; text-align: center; font-weight: 600; color: #6c757d; }

/* --- BARRE DU HAUT (Retour/Fav) --- */
/* Pour éviter qu'ils ne soient affectés par le style géant, on les cible spécifiquement */
div[data-testid="column"] .stButton button {
    width: 100%;
    border-radius: 12px;
    font-weight: 700;
    border-width: 2px;
    padding: 0.5rem 1rem;
    height: auto !important; /* Garder taille normale en haut */
}

/* --- CARTE --- */
.flashcard-content {
  background-color: #ffffff;
  padding: 20px 30px;
  border-radius: 24px 24px 0 0;
  box-shadow: 0 15px 35px rgba(50,50,93,0.1), 0 5px 15px rgba(0,0,0,0.07);
  text-align: center; 
  margin-top: 15px; 
  height: 500px !important; 
  display: flex; flex-direction: column; justify-content: flex-start; align-items: center;
  overflow: hidden; position: relative; z-index: 1;
  width: 100%; box-sizing: border-box;
  margin-bottom: 0 !important; /* Pas de marge en bas pour coller aux boutons */
}
.mode-indicator { margin-top: 50px; font-size: 16px; text-transform: uppercase; letter-spacing: 1.5px; color: #adb5bd; font-weight: 700; }
.content-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; margin-top: 20px; }
.huge-char { font-size: 110px; line-height: 1.2; color: #2c3e50; font-weight: 900; margin: 0; }
.huge-pinyin { font-size: 45px; color: #3498db; font-weight: 700; margin: 5px 0; }
.huge-fr { font-size: 30px; color: #505c6e; font-weight: 600; margin: 5px 0; }
.answer-container { background-color: #f8f9fa; border-radius: 16px; padding: 10px 25px; margin-top: 10px; min-width: 60%; animation: fadeIn 0.3s ease-in; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* --- BOUTONS GÉANTS (Révéler / Choix) --- */

/* 1. Zone Révéler (Bleu) */
.area-reveal {
    margin-top: -10px !important; /* Remonte vers la carte */
}
.area-reveal .stButton button {
    height: 300px !important;      /* FORCE LA HAUTEUR */
    width: 100% !important;
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
    color: white !important; 
    border-radius: 0 0 24px 24px !important;
    font-size: 40px !important; 
    font-weight: 900 !important; 
    border: none !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
}
.area-reveal .stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 25px rgba(0,0,0,0.15) !important;
}

/* 2. Zone Choix (Rouge / Vert) */
/* Cible les boutons à l'intérieur des colonnes de la zone 'area-choices' */
.area-choices .stButton button {
    height: 300px !important;      /* FORCE LA HAUTEUR */
    width: 100% !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    border-radius: 16px !important;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    border: 3px solid transparent !important;
    margin-top: 10px !important;
}

/* Bouton "À revoir" (premier bouton trouvé dans area-choices, souvent le rouge si c'est la 1ère colonne) */
/* Astuce : on cible via CSS spécifique injecté dans le python pour être sûr */

</style>
""", unsafe_allow_html=True)

# --- DATA ---
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

GAME_MODES = { 1: "Pinyin → FR", 2: "FR → Pinyin", 3: "FR -> Symbole",
               4: "Symbole → FR", 5: "Pinyin -> Symbole", 6: "Symbole → Pinyin" }

# --- STATE ---
if 'deck' not in st.session_state: st.session_state.deck = []
if 'current_card' not in st.session_state: st.session_state.current_card = None
if 'revealed' not in st.session_state: st.session_state.revealed = False
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'total_cards_initial' not in st.session_state: st.session_state.total_cards_initial = 0
if 'favorites' not in st.session_state: st.session_state.favorites = []
if 'use_favorites_only' not in st.session_state: st.session_state.use_favorites_only = False
if '_toast_restored_shown' not in st.session_state: st.session_state._toast_restored_shown = False
if 'history' not in st.session_state: st.session_state.history = []

# silent load at startup
load_favorites_from_disk()
load_session_from_disk(show_toast=False)

# init checkboxes
for k in st.session_state.all_data.keys():
    if f"chk_serie_{k}" not in st.session_state: st.session_state[f"chk_serie_{k}"] = True
for k in GAME_MODES.keys():
    if f"chk_mode_{k}" not in st.session_state: st.session_state[f"chk_mode_{k}"] = True

# --- LOGIC ---
def toggle_all_series(state: bool):
    for k in st.session_state.all_data.keys():
        st.session_state[f"chk_serie_{k}"] = state

def toggle_all_modes(state: bool):
    for k in GAME_MODES.keys():
        st.session_state[f"chk_mode_{k}"] = state

def is_current_favorite() -> bool:
    if st.session_state.current_card is None: return False
    (char, pinyin, fr), _ = st.session_state.current_card
    return any(f["char"] == char and f["pinyin"] == pinyin and f["fr"] == fr for f in st.session_state.favorites)

def toggle_favorite():
    if st.session_state.current_card is None: return
    (char, pinyin, fr), _ = st.session_state.current_card
    if is_current_favorite():
        st.session_state.favorites = [f for f in st.session_state.favorites
                                      if not (f["char"] == char and f["pinyin"] == pinyin and f["fr"] == fr)]
        st.toast("🗑️ Retiré des favoris", icon="🗑️")
    else:
        st.session_state.favorites.append({"char": char, "pinyin": pinyin, "fr": fr})
        st.toast("⭐ Ajouté aux favoris", icon="⭐")
    save_favorites_to_disk()

def start_game():
    deck = []
    modes_to_use = [k for k in GAME_MODES.keys() if st.session_state.get(f"chk_mode_{k}", True)]
    if not modes_to_use:
        st.sidebar.error("⚠️ Choisis au moins un mode !")
        return

    if st.session_state.use_favorites_only:
        if not st.session_state.favorites:
            st.sidebar.error("⭐ Ajoute des favoris avant de lancer ce mode.")
            return
        for fav in st.session_state.favorites:
            item = (fav["char"], fav["pinyin"], fav["fr"])
            for m in modes_to_use:
                deck.append((item, m))
    else:
        series_to_use = [k for k in st.session_state.all_data.keys() if st.session_state.get(f"chk_serie_{k}", True)]
        if not series_to_use:
            st.sidebar.error("⚠️ Choisis au moins une série !")
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
    st.session_state.current_card = st.session_state.deck[0] if st.session_state.deck else None
    st.session_state.history = [] # Reset history
    save_session_to_disk()

def push_history():
    state_snapshot = {
        'deck': list(st.session_state.deck),
        'current_card': st.session_state.current_card,
        'revealed': st.session_state.revealed,
        'total_cards_initial': st.session_state.total_cards_initial
    }
    st.session_state.history.append(state_snapshot)

def undo_last_action():
    if st.session_state.history:
        prev = st.session_state.history.pop()
        st.session_state.deck = prev['deck']
        st.session_state.current_card = prev['current_card']
        st.session_state.revealed = prev['revealed']
        st.session_state.total_cards_initial = prev['total_cards_initial']
        st.session_state.game_active = True
        save_session_to_disk()

def next_card():
    st.session_state.revealed = False
    if len(st.session_state.deck) > 0:
        st.session_state.current_card = st.session_state.deck[0]
    else:
        st.session_state.current_card = None
        st.session_state.game_active = False
    save_session_to_disk()

def mark_memorized():
    push_history()
    if st.session_state.deck: st.session_state.deck.pop(0)
    next_card()

def mark_review():
    push_history()
    if st.session_state.deck:
        card = st.session_state.deck.pop(0)
        st.session_state.deck.append(card)
    next_card()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎴 Configuration")
    st.subheader("Source du deck")
    st.checkbox("🎯 Mode Favoris (utiliser uniquement les cartes favorites)", key="use_favorites_only")
    st.caption(f"Favoris actuels : **{len(st.session_state.favorites)}**")

    st.subheader("1. Séries")
    c1, c2 = st.columns(2)
    c1.button("✅ Toutes", key="all_s", on_click=toggle_all_series, args=(True,))
    c2.button("❌ Aucune", key="no_s", on_click=toggle_all_series, args=(False,))
    sorted_keys = sorted(list(st.session_state.all_data.keys()), key=lambda x: int(x.split('-')[0]))
    for key in sorted_keys:
        st.checkbox(f"Série {key}", key=f"chk_serie_{key}", disabled=st.session_state.use_favorites_only)

    st.markdown("---")
    st.subheader("2. Modes de jeu")
    c3, c4 = st.columns(2)
    c3.button("✅ Tous", key="all_m", on_click=toggle_all_modes, args=(True,))
    c4.button("❌ Aucun", key="no_m", on_click=toggle_all_modes, args=(False,))
    for m_id, m_name in GAME_MODES.items():
        st.checkbox(m_name, key=f"chk_mode_{m_id}")

    st.markdown("---")
    st.subheader("⭐ Favoris")
    with st.expander("Gérer mes favoris"):
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites):
                cols = st.columns([4, 3, 3, 2])
                cols[0].markdown(f"**{fav['char']}**")
                cols[1].markdown(f"*{fav['pinyin']}*")
                cols[2].markdown(f"{fav['fr']}")
                if cols[3].button("Retirer", key=f"fav_rm_{i}"):
                    st.session_state.favorites.pop(i)
                    save_favorites_to_disk()
                    st.toast("Favori retiré.", icon="🗑️")
                    rerun()
        else:
            st.caption("Aucun favori pour l'instant.")
    st.download_button("⬇️ Télécharger favoris.json",
                       data=json.dumps(st.session_state.favorites, ensure_ascii=False, indent=2),
                       file_name="favoris.json", mime="application/json", use_container_width=True)
    up_fav = st.file_uploader("📥 Importer favoris.json", type=["json"], key="uploader_favs")
    if up_fav is not None:
        try:
            imported = json.loads(up_fav.read().decode("utf-8"))
            if isinstance(imported, list) and all(set(x.keys()) >= {"char", "pinyin", "fr"} for x in imported):
                st.session_state.favorites = imported
                save_favorites_to_disk()
                st.success(f"Import favoris réussi : {len(imported)} éléments.")
            else:
                st.error("Format invalide: attendu liste d'objets {char,pinyin,fr}.")
        except Exception as e:
            st.error(f"Erreur d'import favoris : {e}")

    st.markdown("---")
    st.subheader("💾 Sauvegarde globale de la session")
    cols_s = st.columns(2)
    if cols_s[0].button("💾 Sauvegarder la session (manuel)", use_container_width=True):
        save_session_to_disk()
        st.success("Session sauvegardée dans session.json.")
    if cols_s[1].button("↩️ Restaurer la dernière session (manuel)", use_container_width=True):
        st.session_state._toast_restored_shown = False
        load_session_from_disk(show_toast=True)
        rerun()

    st.download_button("⬇️ Télécharger session.json",
                       data=SESSION_FILE.read_text(encoding="utf-8") if SESSION_FILE.exists() else json.dumps({}, indent=2),
                       file_name="session.json", mime="application/json", use_container_width=True)
    up_sess = st.file_uploader("📥 Importer session.json", type=["json"], key="uploader_session")
    if up_sess is not None:
        try:
            imported = json.loads(up_sess.read().decode("utf-8"))
            SESSION_FILE.write_text(json.dumps(imported, ensure_ascii=False, indent=2), encoding="utf-8")
            st.session_state._toast_restored_shown = False
            load_session_from_disk(show_toast=True)
            st.success("Session importée et restaurée.")
            rerun()
        except Exception as e:
            st.error(f"Erreur d'import session : {e}")

    st.markdown("---")
    if st.button("🚀 LANCER UNE SESSION", type="primary", use_container_width=True):
        start_game()
        rerun()

# --- MAIN ---
if not st.session_state.game_active:
    st.markdown("""
        <div style='text-align: center; padding: 50px; color: #6c757d;'>
            <h1>👋 Bienvenue !</h1>
            <p style='font-size: 1.2rem;'>Configure ta source (Favoris ou Séries) et tes modes dans la barre latérale,<br>puis clique sur "Lancer une session" pour commencer.</p>
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
        save_session_to_disk()
        rerun()
    st.stop()

(item, mode) = st.session_state.current_card
(char, pinyin, fr) = item
mode_text = GAME_MODES[mode]

# Progression
total = st.session_state.total_cards_initial
restant = len(st.session_state.deck)
progress_val = (total - restant) / total if total > 0 else 0
st.progress(progress_val)
st.caption(f"Progression : {total - restant} / {total}")

# HTML contenu
def format_answer(top, bottom=None):
    html = f'<div class="answer-container"><div class="{top[1]}">{top[0]}</div>'
    if bottom:
        html += f'<div class="{bottom[1]}">{bottom[0]}</div>'
    html += '</div>'
    return html

if mode == 1:  # Pinyin → FR
    q_html = f'<div class="huge-pinyin">{pinyin}</div>'
    a_html = format_answer((char, "huge-char"), (fr, "huge-fr"))
elif mode == 2:  # FR → Pinyin
    q_html = f'<div class="huge-fr" style="font-size: 50px;">{fr}</div>'
    a_html = format_answer((char, "huge-char"), (pinyin, "huge-pinyin"))
elif mode == 3:  # FR -> Symbole
    q_html = f'<div class="huge-fr" style="font-size: 50px;">{fr}</div>'
    a_html = format_answer((char, "huge-char"), (pinyin, "huge-pinyin"))
elif mode == 4:  # Symbole → FR
    q_html = f'<div class="huge-char">{char}</div>'
    a_html = format_answer((pinyin, "huge-pinyin"), (fr, "huge-fr"))
elif mode == 5:  # Pinyin -> Symbole
    q_html = f'<div class="huge-pinyin">{pinyin}</div>'
    a_html = format_answer((char, "huge-char"), (fr, "huge-fr"))
elif mode == 6:  # Symbole → Pinyin
    q_html = f'<div class="huge-char">{char}</div>'
    a_html = format_answer((pinyin, "huge-pinyin"), (fr, "huge-fr"))

# --- AFFICHAGE PRINCIPAL ---
with st.container():
    
    # 1. Barre du HAUT
    c_back, c_spacer, c_fav = st.columns([1, 3, 1])
    
    with c_back:
        if st.session_state.history:
            if st.button("⬅️ Retour", key="btn_back", help="Annuler la dernière action"):
                undo_last_action()
                rerun()
        else:
            st.markdown('<button style="width:100%; background:#f0f2f5; border:2px solid #e0e0e0; color:#a0a0a0; padding:0.5rem; border-radius:12px; font-weight:700; cursor:not-allowed;">⬅️ Retour</button>', unsafe_allow_html=True)

    with c_fav:
        is_fav = is_current_favorite()
        label_fav = "★ Retirer" if is_fav else "⭐ Favoris"
        if st.button(label_fav, key="btn_fav", type="primary" if is_fav else "secondary", help="Ajouter/retirer des favoris"):
            toggle_favorite()
            save_session_to_disk()
            rerun()

    # 2. La Carte
    st.markdown(f"""
    <div class="flashcard-content">
      <div class="mode-indicator">{mode_text}</div>
      <div class="content-wrapper">
        {q_html}
        {a_html if st.session_state.revealed else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Les Boutons d’action GÉANTS
    # On utilise des DIV wrappers (.area-reveal et .area-choices) pour que le CSS cible bien les boutons à l'intérieur
    if not st.session_state.revealed:
        # WRAPPER POUR RÉVÉLER
        st.markdown('<div class="area-reveal">', unsafe_allow_html=True)
        if st.button("👁️ Révéler la réponse", key="btn_reveal", use_container_width=True):
            st.session_state.revealed = True
            save_session_to_disk()
            rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # WRAPPER POUR CHOIX
        st.markdown('<div class="area-choices">', unsafe_allow_html=True)
        
        # Injection CSS spécifique aux couleurs ici pour être sûr de surcharger
        st.markdown("""
        <style>
        /* Force couleur Rouge pour colonne 1 de area-choices */
        .area-choices div[data-testid="column"]:nth-of-type(1) .stButton button {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important; 
            color: #ffffff !important;
        }
        .area-choices div[data-testid="column"]:nth-of-type(1) .stButton button:hover {
            background: #ffffff !important; color: #c0392b !important; border: 3px solid #c0392b !important;
        }
        /* Force couleur Verte pour colonne 2 de area-choices */
        .area-choices div[data-testid="column"]:nth-of-type(2) .stButton button {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important; 
            color: #ffffff !important;
        }
        .area-choices div[data-testid="column"]:nth-of-type(2) .stButton button:hover {
            background: #ffffff !important; color: #27ae60 !important; border: 3px solid #27ae60 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        c_ko, c_ok = st.columns(2, gap="small")
        with c_ko:
            if st.button("❌ À revoir", key="btn_ko", use_container_width=True):
                mark_review()
                save_session_to_disk()
                rerun()
        with c_ok:
            if st.button("✅ Mémorisé", key="btn_ok", use_container_width=True):
                mark_memorized()
                save_session_to_disk()
                rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
