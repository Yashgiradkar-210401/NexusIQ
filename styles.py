import streamlit as st

def load_css():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL APP
        ===================================================== */

        .stApp {
            background-color: #0F172A;
            color: #F8FAFC;
            font-family: 'Segoe UI', sans-serif;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }

        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1F2937;
        }

        section[data-testid="stSidebar"] * {
            color: #F9FAFB !important;
        }

        /* =====================================================
           HEADINGS
        ===================================================== */

        h1 {
            color: #F8FAFC !important;
            font-size: 48px !important;
            font-weight: 700 !important;
            margin-bottom: 10px !important;
        }

        h2 {
            color: #E2E8F0 !important;
            font-size: 32px !important;
            font-weight: 600 !important;
        }

        h3 {
            color: #CBD5E1 !important;
            font-size: 24px !important;
            font-weight: 600 !important;
        }

        /* =====================================================
           KPI CARDS
        ===================================================== */

        div[data-testid="metric-container"] {

            background: linear-gradient(
                145deg,
                #1E293B,
                #0F172A
            );

            border: 1px solid #334155;

            padding: 22px;

            border-radius: 18px;

            box-shadow:
                0px 6px 20px rgba(0,0,0,0.35);

            transition: all 0.3s ease-in-out;
        }

        div[data-testid="metric-container"]:hover {

            transform: translateY(-4px);

            border: 1px solid #3B82F6;

            box-shadow:
                0px 10px 25px rgba(59,130,246,0.25);
        }

        /* KPI LABEL */

        div[data-testid="metric-container"] label {

            color: #94A3B8 !important;

            font-size: 14px !important;

            font-weight: 500 !important;
        }

        /* KPI VALUE */

        div[data-testid="metric-container"] div {

            color: #F8FAFC !important;

            font-size: 30px !important;

            font-weight: 700 !important;
        }

        /* =====================================================
           CHART CONTAINERS
        ===================================================== */

        .element-container {

            border-radius: 18px;
        }

        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton>button {

            background-color: #2563EB;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;

            transition: 0.3s;
        }

        .stButton>button:hover {

            background-color: #1D4ED8;
            transform: scale(1.02);
        }

        /* =====================================================
           SELECTBOX
        ===================================================== */

        .stSelectbox div[data-baseweb="select"] {

            background-color: #1E293B;
            border-radius: 12px;
            border: 1px solid #334155;
        }

        /* =====================================================
           DATAFRAME
        ===================================================== */

        .stDataFrame {

            border: 1px solid #334155;
            border-radius: 15px;
            overflow: hidden;
        }

        /* =====================================================
           ALERT BOXES
        ===================================================== */

        .stAlert {

            border-radius: 15px;
        }

        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #0F172A;
        }

        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }

        /* =====================================================
           HORIZONTAL LINE
        ===================================================== */

        hr {

            border: none;
            height: 1px;s
            background-color: #334155;
            margin-top: 25px;
            margin-bottom: 25px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )