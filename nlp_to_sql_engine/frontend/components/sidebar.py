import streamlit as st

def add_sidebar():
    st.markdown(
        """
        <style>
        /* =========================
           SIDEBAR SHELL
        ========================== */
        [data-testid="stSidebar"]{
            background: linear-gradient(180deg, #F9FAFB 0%, #F5F7FB 100%);
            border-right: 1px solid rgba(17, 24, 39, 0.08);
        }
        [data-testid="stSidebar"] > div:first-child{
            padding: 1.25rem 0.9rem 1.1rem 0.9rem;
        }

        /* Kill default focus outline (we add our own) */
        [data-testid="stSidebar"] button:focus,
        [data-testid="stSidebar"] button:focus-visible{
            outline: none !important;
            box-shadow: none !important;
        }

        /* =========================
           BRAND HEADER
        ========================== */
        .sb-brand{
            display:flex;
            align-items:center;
            gap: 12px;
            padding: 0.75rem 0.75rem 1rem 0.75rem;
            margin-bottom: 0.75rem;
            border-radius: 16px;
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(17,24,39,0.06);
            box-shadow: 0 10px 26px rgba(17,24,39,0.06);
        }
        .sb-logo{
            width: 44px;
            height: 44px;
            border-radius: 14px;
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
            display:flex;
            align-items:center;
            justify-content:center;
            box-shadow: 0 10px 18px rgba(37,99,235,0.25);
            flex: 0 0 auto;
        }
        .sb-title{
            display:flex;
            flex-direction:column;
            gap: 2px;
            line-height: 1.1;
        }
        .sb-title b{
            font-size: 0.95rem;
            color: #0F172A;
            letter-spacing: 0.2px;
        }
        .sb-title span{
            font-size: 0.78rem;
            color: rgba(15,23,42,0.65);
        }

        /* =========================
           SECTION LABELS + DIVIDER
        ========================== */
        .sb-divider{
            height: 1px;
            background: rgba(17,24,39,0.08);
            margin: 0.9rem 0.25rem;
        }
        .sb-section{
            margin: 0.2rem 0.25rem 0.55rem 0.25rem;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: rgba(15,23,42,0.55);
        }

        /* =========================
           BUTTONS (Primary / Secondary)
           - Better padding
           - Icon alignment
           - Hover + active feel
        ========================== */
        [data-testid="stSidebar"] button[kind="primary"],
        [data-testid="stSidebar"] button[kind="secondary"]{
            border-radius: 14px !important;
            padding: 0.85rem 0.95rem !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            width: 100% !important;
            transition: transform .12s ease, box-shadow .12s ease, background .12s ease, border-color .12s ease !important;
        }

        /* Primary */
        [data-testid="stSidebar"] button[kind="primary"]{
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            color: white !important;
            box-shadow: 0 12px 26px rgba(37,99,235,0.22) !important;
            margin-bottom: 0.6rem !important;
        }
        [data-testid="stSidebar"] button[kind="primary"]:hover{
            transform: translateY(-1px) !important;
            box-shadow: 0 16px 34px rgba(37,99,235,0.28) !important;
            filter: brightness(1.02);
        }
        [data-testid="stSidebar"] button[kind="primary"]:active{
            transform: translateY(0px) scale(0.99) !important;
        }

        /* Secondary */
        [data-testid="stSidebar"] button[kind="secondary"]{
            background: rgba(255,255,255,0.82) !important;
            border: 1px solid rgba(17,24,39,0.10) !important;
            color: #0F172A !important;
            box-shadow: 0 6px 16px rgba(17,24,39,0.06) !important;
            margin-bottom: 0.5rem !important;
            text-align: left !important;
        }
        [data-testid="stSidebar"] button[kind="secondary"]:hover{
            transform: translateY(-1px) !important;
            border-color: rgba(37,99,235,0.22) !important;
            box-shadow: 0 10px 22px rgba(17,24,39,0.08) !important;
            background: rgba(255,255,255,0.92) !important;
        }
        [data-testid="stSidebar"] button[kind="secondary"]:active{
            transform: translateY(0px) scale(0.99) !important;
        }

        /* Make emoji icons align nicer */
        [data-testid="stSidebar"] button[kind="primary"] p,
        [data-testid="stSidebar"] button[kind="secondary"] p{
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            margin: 0 !important;
        }

        /* =========================
           EXPANDERS (clean card style)
        ========================== */
        [data-testid="stSidebar"] .streamlit-expanderHeader{
            background: rgba(255,255,255,0.82) !important;
            border: 1px solid rgba(17,24,39,0.10) !important;
            border-radius: 14px !important;
            color: #0F172A !important;
            padding: 0.8rem 0.95rem !important;
            font-weight: 600 !important;
            box-shadow: 0 6px 16px rgba(17,24,39,0.06) !important;
        }
        [data-testid="stSidebar"] .streamlit-expanderHeader:hover{
            transform: translateY(-1px);
            border-color: rgba(37,99,235,0.22) !important;
            box-shadow: 0 10px 22px rgba(17,24,39,0.08) !important;
        }
        [data-testid="stSidebar"] .streamlit-expanderContent{
            background: rgba(255,255,255,0.86) !important;
            border: 1px solid rgba(17,24,39,0.10) !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            padding: 0.75rem 0.85rem !important;
            margin-top: -0.55rem !important;
            box-shadow: 0 10px 22px rgba(17,24,39,0.06) !important;
        }

        /* Info blocks inside expanders */
        [data-testid="stSidebar"] .stAlert{
            background: rgba(15,23,42,0.03) !important;
            border: 1px solid rgba(15,23,42,0.08) !important;
            border-radius: 12px !important;
            color: rgba(15,23,42,0.70) !important;
            font-size: 0.86rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # --- Brand header (clean + professional)
        st.markdown(
            """
            <div class="sb-brand">
                <div class="sb-logo">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                         xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <path d="M12 2a10 10 0 1 0 0 20a10 10 0 0 0 0-20Z" stroke="white" stroke-width="2"/>
                        <path d="M7.5 12h9" stroke="white" stroke-width="2" stroke-linecap="round"/>
                        <path d="M12 7.5v9" stroke="white" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="sb-title">
                    <b>Conversational BI</b>
                    <span>Ask questions • Get SQL • See insights</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Primary action
        if st.button("✨ New conversation", type="primary", use_container_width=True, key="start_new"):
            st.toast("New conversation started", icon="✨")
            if "messages" in st.session_state:
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": "Hi! I'm your Conversational BI Agent. Ask me any data question and I'll help you explore your insights through natural language."
                }]
            st.rerun()

        # --- Secondary actions
        if st.button("🧹 Clear chat", type="secondary", use_container_width=True, key="clear_chat"):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Hi! I'm your Conversational BI Agent. Ask me any data question and I'll help you explore your insights through natural language."
            }]
            st.rerun()

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-section">History</div>', unsafe_allow_html=True)
        with st.expander("🗂️ Conversation history", expanded=False):
            st.info("Coming soon: saved conversations, pinned chats, and search.")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-section">Data</div>', unsafe_allow_html=True)

        if st.button("🧾 View schema", type="secondary", use_container_width=True, key="view_schema"):
            st.toast("Schema panel coming soon", icon="🧾")

        with st.expander("📌 KPIs", expanded=False):
            st.info("Coming soon: curated KPIs (Orders, Revenue, AOV, On-time delivery, etc.).")
