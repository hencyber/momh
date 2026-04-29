import streamlit as st
import requests

st.title("CSN Återbetalning - Chatbot")
st.write("Ställ frågor om återbetalning av studielån")

API_URL = "http://localhost:8002/chat"

# chatt-historik
if "messages" not in st.session_state:
    st.session_state.messages = []

# visa tidigare meddelanden
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
question = st.chat_input("Ställ en fråga om återbetalning...")

if question:
    # visa användarens fråga
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    
    # skicka till backend
    with st.chat_message("assistant"):
        with st.spinner("Tänker..."):
            try:
                response = requests.post(API_URL, json={"question": question}, timeout=60)
                data = response.json()
                
                st.write(data["answer"])
                
                # visa källor
                if data.get("sources"):
                    st.write("---")
                    st.write("**Källor:**")
                    for source in data["sources"]:
                        st.write(f"- [{source}]({source})")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"]
                })
            except Exception as e:
                st.error(f"Kunde inte kontakta backend: {e}")
