import streamlit as st
st.set_page_config(page_title = "About", page_icon="ey-logo-black.png")
st.markdown('<style>div.block-container{padding-top:4rem;padding-left:1rem;padding-right:5rem}</style>',unsafe_allow_html=True)

col1,col2 = st.columns([1.2,10])
with col1: st.image("ey-logo-black.png", width=150)
with col2: st.title("About")
#st.title("About")
st.markdown('<hr style="border:1px solid #aaa; margin-bottom: 1rem"/>', unsafe_allow_html=True)
c1 = st.container(key="container1", border=True)
c1.write("Legal Document Analysis (LDA) is a cutting-edge platform designed to assist legal professionals in the review and analysis of complex documents. Our tool leverages advanced algorithms and machine learning techniques to identify key legal terms, clauses, and patterns, streamlining the process of legal document review.")
c1.write("Our mission is to provide a user-friendly and efficient solution for legal document analysis, saving time and reducing the potential for human error. Whether you're a lawyer, paralegal, or legal researcher, LDA is your go-to resource for accurate and thorough document analysis.")
c1.write("The LDA team is composed of legal experts, data scientists, and software engineers dedicated to delivering the best possible service to our users. We are constantly updating our platform with the latest technological advancements to ensure that our clients have access to the most innovative tools in the industry.")
#display Logo
st.logo(image="ey-logo-black.png", size="large")
#sidebar
st.sidebar.title("Legal Document Analyser")
st.sidebar.page_link(page="Home.py", label="Home", use_container_width= True, icon="🏠")
st.sidebar.page_link(page="Pages/Chat.py", label="Chat", use_container_width= True, icon="💬")
st.sidebar.page_link(page="Pages/About.py", label="About", use_container_width= True, icon="❓")



csscode = """
<style>
    .stApp {
        background-color: #2e2e38;
        
    }

    .st-emotion-cache-1104ytp h1 {
        color:white;}

    

    .st-emotion-cache-4uzi61 eu6p4el5 {
    padding-left: 20rem;
    }

    .stMarkdown {
    color: white;
    }


</style>
"""

st.markdown(csscode, unsafe_allow_html=True)