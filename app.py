# ================= AFFICHAGE DE LA CARTE =================
with st.container():
    # 1. Le contenu HTML
    # IMPORTANT : Les chaînes f-string ci-dessous sont collées à gauche 
    # pour éviter que Streamlit ne crée des blocs de code gris indésirables (</div>).
    
    st.markdown(f"""
<div class="flashcard-content">
<div class="mode-indicator">{mode_text}</div>
<div class="content-wrapper">
{q_html}
{a_html if st.session_state.revealed else ""}
</div>
</div>
""", unsafe_allow_html=True)

    # 2. Zone des boutons d'action
    if not st.session_state.revealed:
        if st.button("👁️ Révéler la réponse", key="btn_reveal"):
            st.session_state.revealed = True
            rerun()
    else:
        c_ko, c_ok = st.columns(2, gap="medium")
        with c_ko:
            if st.button("❌ À revoir", key="btn_ko"):
                mark_review()
                rerun()
        with c_ok:
            if st.button("✅ Mémorisé", key="btn_ok"):
                mark_memorized()
                rerun()
