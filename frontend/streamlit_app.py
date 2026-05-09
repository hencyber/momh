import streamlit as st
import requests

st.set_page_config(
    page_title="CSN Chatbot",
    page_icon="💬",
    layout="centered",
)

CHATBOTS = {
    "Studiestöd": {
        "title": "🎓 CSN Studiestöd",
        "description": "Ställ frågor om studiemedel, bidrag och lån",
        "url": "http://localhost:8001/chat",
        "placeholder": "Ex: Hur ansöker jag om studiemedel?",
    },
    "Återbetalning": {
        "title": "💳 CSN Återbetalning",
        "description": "Ställ frågor om återbetalning av studielån",
        "url": "http://localhost:8002/chat",
        "placeholder": "Ex: Hur fungerar återbetalning?",
    },
    "Utlandsstudier": {
        "title": "✈️ CSN Utlandsstudier",
        "description": "Ställ frågor om bidrag och lån för studier utomlands",
        "url": "http://localhost:8003/chat",
        "placeholder": "Ex: Kan jag få CSN för studier i Spanien)",
    },
}

st.markdown(
    """
<style>
.stApp {
    background-color: #121212;
    color: #E0E0E0;
}
            
h1, h2, h3 {
    color: #FFFFF !important;
}
            
.answer-container {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
}

.source-text {
    font-size: 0.85rem;
    color: #2ecc71;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("💬 CSN Chatbot")
st.write("Välj område och ställ din fråga.")

selected_chat = st.selectbox("Välj chatt", list(CHATBOTS.keys()))
chat = CHATBOTS[selected_chat]

st.subheader(chat["title"])
st.write(chat["description"])

question = st.chat_input(chat["description"])

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Hämtar information..."):
            try:
                response = requests.post(
                    chat["url"],
                    json={"question": question},
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()

                    st.markdown(
                        '<div class="answer-container">', unsafe_allow_html=True
                    )
                    st.write(data.get("answer", "Inget svar returnerades"))

                    sources = data.get("sources", [])
                    if sources:
                        st.markdown("---")
                        st.markdown("**Källor:**")
                        for source in sources:
                            st.markdown(
                                f'<p class="source-text"><a href="{source}" target="_blank">🔗 {source}</a></p>',
                                unsafe_allow_html=True,
                            )

                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.error(f"API-anropet misslyckades: {response.status_code}")
                    st.code(response.text)

            except Exception as e:
                st.error(f"Kunde inte ansluta till servern: {e}")
