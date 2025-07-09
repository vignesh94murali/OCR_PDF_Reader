import streamlit as st
import numpy as np
import pandas as pd
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
#from mygraph import createGraph
from Pages.mygraph import createGraph
import uuid
import os
import tempfile
from Pages.utils import get_token_count, log_chat, display_chat_history


# Streamlit UI
#setting page title and logo
st.set_page_config(page_title = "Document Analyser", page_icon="ey-logo-black.png")
#adding padding using css
st.logo(image="ey-logo-black.png", size="large")
st.markdown('<style>div.block-container{padding-top:4rem;padding-left:1rem;padding-right:5rem}</style>',unsafe_allow_html=True)
col1,col2 = st.columns([1.2,10])
with col1: st.image("ey-logo-black.png", width=150)
with col2: st.title("Document Analyser")
# Add a horizontal line after the header
st.markdown('<hr style="border:1px solid #aaa; margin-bottom: 1rem"/>', unsafe_allow_html=True)
st.write("")

tab1, tab2, tab3 = st.tabs(["Summarize", "Compare", "Read Scanned PDFs"])

#defining tab1 contents
with tab1:
    with st.container(border=True, key="con1") as con1:
        graph = createGraph()
        user_query = st.text_input("Ask a question to summarize or compare documents:",
                                   placeholder="Input prompt here", )
        col3, col4, col5 = st.columns([1, 1, 1.7])
        with col5:
            uploaded_files = st.file_uploader("Upload documents to compare or summarize:", ["pdf", "docx"], True,
                                              key="Attach")
        with col3:
            submit = st.button("Submit", use_container_width=True)

    if submit:
        path = r'C:\Users\UL318UZ\Python_POC\UC_Legal-Document-Analyser-main\temp_docs'
        os.makedirs(path, exist_ok=True)

        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            file_paths.append(file_path)

        if user_query and len(file_paths) != 0:
            query = user_query + f" file_path:{file_paths}"
            st.write('User:', query)
            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                # Token tracking
                from Pages.utils import get_token_count, log_chat, display_chat_history

                prompt_tokens = get_token_count(query)
                doc_tokens = sum(get_token_count(open(p, 'r', errors="ignore").read()) for p in file_paths)
                response_tokens = get_token_count(ai_msg)
                total = prompt_tokens + doc_tokens + response_tokens
                log_chat("summarize", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": doc_tokens,
                    "response": response_tokens,
                    "total": total
                })
        elif user_query:
            query = user_query
            st.write('User:', query)
            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                prompt_tokens = get_token_count(query)
                response_tokens = get_token_count(ai_msg)
                log_chat("summarize", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": 0,
                    "response": response_tokens,
                    "total": prompt_tokens + response_tokens
                })
        else:
            st.warning("Please enter a query and upload files.")

    # Always show chat history at the bottom of tab1
    display_chat_history("summarize")

with tab2:
    from Pages.utils import log_chat, get_token_count, display_chat_history  # Assuming these utils exist

    with st.container(border=True, key="con2") as con2:
        graph = createGraph()
        compare_query = st.text_input("Compare the two uploaded documents:", placeholder="Enter a comparison prompt",
                                      key="compare_prompt")
        col6, col7, col8 = st.columns([1, 1, 1.7])
        with col8:
            compare_files = st.file_uploader("Upload exactly 2 documents to compare:", ["pdf", "docx"],
                                             accept_multiple_files=True, key="compare_upload")
        with col6:
            submit_compare = st.button("Compare", use_container_width=True, key="compare_button")

    if submit_compare:
        compare_path = r'C:\Users\UL318UZ\Python_POC\UC_Legal-Document-Analyser-main\temp_docs'
        os.makedirs(compare_path, exist_ok=True)
        file_paths = []

        for uploaded_file in compare_files:
            file_path = os.path.join(compare_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            file_paths.append(file_path)

        # st.write("Uploaded files : ", file_paths)

        if compare_query and len(file_paths) == 2:
            query = compare_query + f" file_path:{file_paths}"
            st.write('User:', query)

            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                # Token tracking
                prompt_tokens = get_token_count(query)
                doc_tokens = sum(get_token_count(open(p, 'r', errors="ignore").read()) for p in file_paths)
                response_tokens = get_token_count(ai_msg)
                total = prompt_tokens + doc_tokens + response_tokens

                log_chat("compare", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": doc_tokens,
                    "response": response_tokens,
                    "total": total
                })
        elif len(file_paths) != 2:
            st.warning("Please upload exactly two documents for comparison.")
        else:
            st.warning("Please enter a prompt and upload files.")

    # Always display chat history at the end of compare tab
    display_chat_history("compare")

with tab3:
    st.subheader("Extract Text from Scanned PDF")
    scanned_file = st.file_uploader("Upload a scanned PDF/TIFF file", type=["pdf", "tif", "tiff"], key="scanned_pdf")
    extract_button = st.button("Extract Text", key="extract_button")

    if extract_button:
        if scanned_file:
            temp_dir = r'C:\Users\UL318UZ\Python_POC\UC_Legal-Document-Analyser-main\temp_docs'
            os.makedirs(temp_dir, exist_ok=True)

            # Save uploaded PDF
            file_path = os.path.join(temp_dir, scanned_file.name)
            with open(file_path, "wb") as f:
                f.write(scanned_file.getvalue())

            
            # Run OCR
            from Pages.ocr_reader import extract_text_from_scanned_pdf, extract_text_from_tiff, check_pdf_image_dpi, send_outlook_email

            # Determine file type
            file_ext = scanned_file.name.lower().split('.')[-1]

            with st.spinner("Performing OCR on scanned PDF..."):
                try:
                    check_pdf_image_dpi(file_path, min_required_dpi=72)
                    if file_ext == 'pdf':
                        extracted_text = extract_text_from_scanned_pdf(file_path, save_images=False)
                    elif file_ext in ["tif", "tiff"]:
                        extracted_text = extract_text_from_tiff(file_path)
                    else:
                        raise ValueError("Unsupported file type.")
                    
                    if extracted_text.strip():
                        st.success("Text extraction complete!")
                        st.text_area("Extracted Text", extracted_text, height=400)
                        # Download button
                        st.download_button("Download Extracted Text",
                                           data=extracted_text,
                                           file_name="extracted_text.txt",
                                           mime="text/plain")
                    else:
                        st.warning("No text was extracted. Ensure the PDF is clearly scanned and meets the DPI requirement (≥ 72 DPI).")
                    
                except Exception as e:
                    st.error(f"OCR scanning failed : {str(e)}")
                    # Optional: notify team
                    subject = "<Important> OCR Extraction Failed"
                    body = f"""Dear Team,
                    The OCR process failed for file: {file_path}
                Reason:
                    {str(e)}
                    Please review the file and reupload a higher-quality scan.
                Regards,
                OCR Bot, HSBC
                    """
                    recipients = ["Vignesh.Murali@in.ey.com"]
                    send_outlook_email(subject, body, recipients)
                else:
                    st.warning("Please upload a scanned PDF before extracting.")


#creating data for chat history:
chats = {

    "Chats": ["Prompt1", "Prompt2", "Prompt3"]
}
df = pd.DataFrame(data=chats)

#sidebar
#Page Links in sidebar:
st.sidebar.title("Document Analyser")
st.sidebar.page_link(page="Home.py", label="Home", use_container_width= True, icon="🏠")
st.sidebar.page_link(page="Pages/Chat.py", label="Chat", use_container_width= True, icon="💬")
st.sidebar.page_link(page="Pages/About.py", label="About", use_container_width= True, icon="❓")

#container for chat history
# sbcnt = st.sidebar.container(height=300,border=True)
# with sbcnt:
#     sbcnt.subheader("Chat History:")
#     sbcnt.dataframe(df)

#Footer Links (paste footer controls here)


st.caption("Disclaimer: This response was generated by an AI and is intended for informational purposes only. While efforts have been made to ensure accuracy, the information provided may not be complete or up-to-date. Always verify critical information independently and consult with a qualified professional if necessary. The AI does not have personal experiences or emotions and its responses are based on patterns in data.")

#CSS code for the page
# csscode = """
#     <style>
#     /* Set background color for the entire app */
#     .stApp {
#         background-color: #161D23;
#         color: white;
#     }
#     .stTextInput>div>div>input {
#         background-color: #2c2f33;
#         color: white;
#         border: 1px solid #555;
#     }
#     .stTextInput {
#              padding-left:2rem
#     }
#     .stButton>button {
#         background-color: #ffe600;
#         color: black;
#         border: none;
#         font-weight: bold;
#     }
#     .stButton {
#             padding: 2rem;
#     }
#     .st-emotion-cache-1104ytp {

#             color:white;
#     }
#     .st-emotion-cache-wq5ihp {
#             color:white
#     }
#     .stcon1{
#             padding: 6 rem;
#             }

#     .stColumn st-emotion-cache-t74pzu eu6p4el2{
#             padding: 4rem;
#             }

#     .st-emotion-cache-1uixxvy{
#             color: white;
#             }
#     .stMarkdown {
#         color: white;
#     }
# </style>
# """

csscode = """
    <style>
    /* Set background color for the entire app */
    .stApp {
        background-color: #161D23;
        color: white; /* Default text color */
    }

    /* Text Input box styling */
    .stTextInput > div > div > input {
        background-color: #2c2f33;
        color: white;
        border: 1px solid #555;
    }

    .stTextInput {
        padding-left: 2rem;
    }

    /* Button styling */
    .stButton > button {
        background-color: #ffe600;
        color: black;
        border: none;
        font-weight: bold;
    }

    .stButton {
        padding: 2rem;
    }

    /* Markdown and other common text elements */
    .stMarkdown, .stMarkdown p {
        color: white;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }

    /* Generic div text */
    div {
        color: white;
    }

    /* Fix for padding typo */
    .stcon1 {
        padding: 6rem;
    }

    /* Optional: Table, DataFrame styling */
    .css-1d391kg { 
        background-color: #2c2f33; 
        color: white;
    }

    /* Input labels */
    label {
        color: white !important;
    }

    .stSidebar {
        background-color: #1f262d;
    }

    .stSidebar .css-1v0mbdj, .stSidebar .css-1d391kg {
        color: white;
    }

    /* Make tabs more readable on dark background */
    [data-testid="stTabs"] > div > div {
    background-color: #2c2f33 !important;  /* Dark background for tab header */
    border-radius: 8px;
    }

    [data-testid="stTab"] {
    color: white !important;  /* Unselected tab text */
    font-weight: bold;
    padding: 10px 20px;
    }

    [data-testid="stTab"]:hover {
    color: #ffe600 !important;  /* Hover color for better UX */
    cursor: pointer;
    }

    [data-testid="stTab"][aria-selected="true"] {
    background-color: #ffe600 !important;
    color: black !important;  /* Selected tab styling */
    border-radius: 8px 8px 0 0;
    }

    </style>
"""

# Custom CSS for background color
st.markdown(csscode, unsafe_allow_html=True)
