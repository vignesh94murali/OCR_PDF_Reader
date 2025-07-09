import tiktoken
import streamlit as st
from datetime import datetime

def get_token_count(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))
    except:
        return len(text.split())  # fallback

def log_chat(session_key: str, user_input: str, ai_response: str, tokens_used: dict):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "chat_logs" not in st.session_state:
        st.session_state["chat_logs"] = {}

    if session_key not in st.session_state["chat_logs"]:
        st.session_state["chat_logs"][session_key] = []

    st.session_state["chat_logs"][session_key].append({
        "time": timestamp,
        "user_input": user_input,
        "ai_response": ai_response,
        "tokens": tokens_used
    })

def display_chat_history(session_key: str):
    st.subheader("Chat History")
    chats = st.session_state.get("chat_logs", {}).get(session_key, [])
    for idx, entry in enumerate(chats[::-1]):
        st.markdown(f"**{entry['time']}**")
        st.markdown(f"- **User:** {entry['user_input']}")
        st.markdown(f"- **AI:** {entry['ai_response']}")
        st.markdown(f"- **Tokens Used:** Prompt: `{entry['tokens']['prompt']}`, Docs: `{entry['tokens']['doc']}`, Response: `{entry['tokens']['response']}`, Total: `{entry['tokens']['total']}`")
        st.markdown("---")


def is_likely_legal(content: str) -> bool:
    legal_keywords = [
        "agreement", "contract", "clause", "party", "terms", "conditions",
        "witnesseth", "hereinafter", "indemnify", "governing law", "liable",
        "warranty", "termination", "non-disclosure", "nda", "intellectual property"
    ]
    content_lower = content.lower()
    match_count = sum(1 for word in legal_keywords if word in content_lower)
    return match_count >= 3  # Threshold for minimum matches
