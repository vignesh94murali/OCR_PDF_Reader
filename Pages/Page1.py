import streamlit as st

# Custom CSS to set the background color to black
# st.markdown("""
#     <style>
#     .stApp {
#         background-color: #161D23;
#     }
#     .rounded-container {
#         background-color: white;
#         border-radius: 15px;
#         padding: 20px;
#         margin: 10px 0;
#     }
#     .stTextInput label, .stButton>button {
#         color: white;
#     }
#     .stTextInput div[data-baseweb="input"] {
#         background-color: white;
#     }
#     .stTextInput div[data-baseweb="input"] input {
#         color: white;
#     }
#     .css-1cpxqw2, .st-bx, .st-bw, .st-ae {
#         color: white;
#     }
#     </style>
#     """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background-color: #161D23;
        color: white;
    }

    .rounded-container {
        background-color: #2c2f33;  /* Dark card-style background */
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
    }

    /* Input label and text color */
    .stTextInput label,
    .stButton>button {
        color: white;
    }

    /* Text input background and text */
    .stTextInput div[data-baseweb="input"] {
        background-color: #2c2f33;
    }

    .stTextInput div[data-baseweb="input"] input {
        color: white;
    }

    /* Fix other default element text colors */
    .css-1cpxqw2, .st-bx, .st-bw, .st-ae {
        color: white;
    }

    /* Ensure headers and paragraphs are white */
    h1, h2, h3, h4, h5, h6, p {
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

# Title of the web page
st.title('Agentic AI Agent Interface')

# Description
st.write('Enter a prompt for the AI agent to process.')

# Text input for the prompt
prompt = st.text_input('Enter your prompt here:', key="prompt_input")

# Upload button for attachments
uploaded_file = st.file_uploader("Upload an attachment:", type=['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'])

# Handle the uploaded file
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write("Uploaded file:")
    # To display the uploaded file name:
    st.write(uploaded_file.name)
    # You can add additional processing here depending on the file type 

# Container to hold buttons
col1, col2 = st.columns(2)

# Submit button to process the prompt
submit = col1.button('Submit')

# Clear button to erase the text input
clear = col2.button('Clear')

# If submit is clicked, process the prompt
if submit:
    #result = process_prompt(prompt)
    st.success('The AI agent has processed your prompt:')
    #st.write(result)

# If clear is clicked, erase the text input
if clear:
    # This will clear the text input and the output
    #st.session_state.prompt_input = ""
    #st.text_input(1).clear
    print("Clear Pressed")
