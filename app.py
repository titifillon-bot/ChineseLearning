# --- AFFICHAGE ---
with st.container():
    
    # 1. Barre du HAUT : Retour & Favoris (AU-DESSUS de la carte)
    c_back, c_spacer, c_fav = st.columns([1, 3, 1])
    
    with c_back:
        if st.session_state.history:
            if st.button("⬅️ Retour", key="btn_back", help="Annuler la dernière action"):
                undo_last_action()
                rerun()
        else:
            # Bouton désactivé visuel
            st.markdown('<button style="width:100%; background:#e0e0e0; border:none; color:#a0a0a0; padding:0.5rem; border-radius:12px; font-weight:700; cursor:not-allowed;">⬅️ Retour</button>', unsafe_allow_html=True)

    with c_fav:
        is_fav = is_current_favorite()
        label_fav = "★ Retirer" if is_fav else "⭐ Favoris"
        # Astuce couleur : on injecte du style inline via arguments si on veut, 
        # ou on laisse le style par défaut Streamlit qui est propre.
        # Pour le style jaune spécifique, on peut cibler via CSS global ou laisser standard.
        if st.button(label_fav, key="btn_fav", type="primary" if is_fav else "secondary", help="Ajouter/retirer des favoris"):
            toggle_favorite()
            save_session_to_disk()
            rerun()

    # 2. La Carte (Juste en dessous)
    st.markdown(f"""
    <div class="flashcard-content">
      <div class="mode-indicator">{mode_text}</div>
      <div class="content-wrapper">
        {q_html}
        {a_html if st.session_state.revealed else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Les Boutons d’action (Révéler / Choix)
    if not st.session_state.revealed:
        st.markdown('<div class="reveal-btn">', unsafe_allow_html=True)
        if st.button("👁️ Révéler la réponse", key="btn_reveal", use_container_width=True):
            st.session_state.revealed = True
            save_session_to_disk()
            rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="choice-row">', unsafe_allow_html=True)
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
