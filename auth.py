import streamlit as st

from users import users

# =====================================================
# LOGIN FUNCTION
# =====================================================

def login():

    # =================================================
    # CSS
    # =================================================

    st.markdown("""
    <style>

    /* =================================================
    BACKGROUND
    ================================================= */

    .stApp{

        background:
            linear-gradient(
                135deg,
                #020817 0%,
                #071224 50%,
                #0F172A 100%
            );
    }

    /* =================================================
    REMOVE STREAMLIT DEFAULT
    ================================================= */

    header[data-testid="stHeader"]{

        background:transparent;
    }

    #MainMenu{

        visibility:hidden;
    }

    footer{

        visibility:hidden;
    }

    .stDeployButton{

        display:none;
    }

    /* =================================================
    LAYOUT
    ================================================= */

    .main .block-container{

        padding-top:4rem;

        max-width:1000px;
    }

    /* =================================================
    LOGIN CARD
    ================================================= */

    .login-card{

        background:
            rgba(15,23,42,0.95);

        border:
            1px solid rgba(255,255,255,0.06);

        border-radius:24px;

        padding:40px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.45);
    }

    /* =================================================
    HEADINGS
    ================================================= */

    h1{

        color:white !important;

        font-size:58px !important;

        font-weight:800 !important;

        margin-bottom:10px !important;
    }

    h3{

        color:#CBD5E1 !important;

        font-weight:500 !important;

        line-height:1.4 !important;

        margin-bottom:30px !important;
    }

    /* =================================================
    LABELS
    ================================================= */

    .stTextInput label{

        color:#E2E8F0 !important;

        font-weight:600 !important;

        font-size:15px !important;
    }

    /* =================================================
    INPUT BOX
    ================================================= */

    .stTextInput input{

        background:#0F172A !important;

        color:white !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        border-radius:14px !important;

        padding:14px !important;

        font-size:15px !important;
    }

    /* =================================================
    PASSWORD ICON FIX
    ================================================= */

    [data-testid="stBaseButton-secondary"]{

        background:#0F172A !important;

        border:none !important;
    }

    /* =================================================
    BUTTON
    ================================================= */

    .stButton button{

        width:100%;

        background:
            linear-gradient(
                90deg,
                #0066FF,
                #0050D4
            ) !important;

        color:white !important;

        border:none !important;

        border-radius:14px !important;

        padding:14px !important;

        font-size:16px !important;

        font-weight:700 !important;

        margin-top:15px !important;
    }

    .stButton button:hover{

        transform:translateY(-2px);

        box-shadow:
            0 10px 24px rgba(0,102,255,0.35);
    }

    /* =================================================
    MOBILE
    ================================================= */

    @media screen and (max-width:768px){

        .login-card{

            padding:25px;
        }

        h1{

            font-size:42px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

    # =================================================
    # CENTER LAYOUT
    # =================================================

    left, center, right = st.columns([1.2,1.6,1.2])

    with center:

        st.markdown(
        """
        <h1 style="
            color:white;
            font-size:72px;
            font-weight:800;
            margin-bottom:10px;
        ">
            NexusIQ
        </h1>

        <h3 style="
            color:#CBD5E1;
            font-size:22px;
            font-weight:500;
            line-height:1.5;
            margin-bottom:40px;
        ">
            Enterprise Decision Intelligence Platform
        </h3>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in users:

            if users[username]["password"] == password:

                st.session_state.authenticated = True

                st.session_state.username = username

                st.session_state.role = users[username]["role"]

                st.rerun()

            else:

                st.error("Invalid Password")

        else:

            st.error("User Not Found")

# =====================================================
# LOGOUT FUNCTION
# =====================================================

def logout():

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()