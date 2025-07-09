import streamlit as st

st.set_page_config(page_title="Document Analyser", page_icon="ey-logo-black.png")

st.logo("ey-logo-black.png", size="large")
st.title("Welcome to Document Analyser")

st.markdown("""
    <style>
    .stApp {
        background-color: #161D23;
        color: white;
        background-image: url('ey-logo-black.png');
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-size: 250px; /* Adjust size here */
        opacity: 0.98;
    }

    /* Optional overlay to reduce logo contrast further */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(22, 29, 35, 0.6); /* Dark overlay to fade logo */
        z-index: -1;
    }

    h1, h2, h3, h4, h5, h6, p, li {
        color: white;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown ul, .stMarkdown li {
        color: white;
    }

    .stButton > button, .stLinkButton button {
        background-color: #ffe600;
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #ffcc00;
        color: black;
    }

    .stSidebar {
        background-color: #1f262d;
    }

    .stSidebar .css-1v0mbdj, .stSidebar .css-1d391kg {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
This application allows you to:
- Summarize uploaded legal documents (PDF or DOCX).
- Compare two legal documents for differences.
- Extract details from Scanned PDFs
- Interact via chat with your documents using AI.

Use the sidebar to navigate between pages.
""")

# st.image("legal-doc.jpg", caption="Secure & Smart Legal AI", use_container_width=True)

col3,col4,col5 = st.columns([2.8,1,3])
with col4:
    st.page_link(page="Pages/Chat.py", label="Begin", use_container_width=True)

st.sidebar.page_link("Home.py", label="Home", icon="🏠")
st.sidebar.page_link("Pages/Chat.py", label="Chat", icon="💬")
st.sidebar.page_link("Pages/About.py", label="About", icon="❓")
