import streamlit as st 
import requests 

# 
# 1. Page configuration 

st.set_page_config(
    page_title= "CSN-Utlandsstudier",
    page_icon = "🌴" "🌏",
    layout = "centered"
)

# --- 2. UI POLISH (CSS)

st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Titlar */
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* Knappen med grön gradient */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #2ecc71, #27ae60);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.2);
    }

    /* Styling för svarsrutan (Silver/Grå kant) */
    .answer-container {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #444444;
        margin-top: 20px;
    }

    .source-text {
        font-size: 0.85rem;
        color: #2ecc71;
    }
    </style>
    """, unsafe_allow_html=True)


# 3. LAYOUT & TEXT 

st.title("✈️ Utlandsstudier Chat")
st.markdown ("Dags för ett miljöbyte!! Ställ dina frågor om bidrag och lån för studier utanför Sverige.")


# 
user_input =st.text_input("Din fråga", placeholder=" T.e.x Hur söker jag studiemedel för studier i USA ?")

# Logic 

if st.button("Skicka"):
    if user_input:
        with st.spinner('Hämtar information...'):
            try:
                response = requests.post(
                    "http://localhost:8003/chat",
                    json={"question": user_input}
                )

                if response.status_code == 200:
                    data = response.json()

                    st.markdown(
                        '<div class="answer-container">',
                        unsafe_allow_html=True
                    )

                    st.subheader("Svar:")
                    st.write(data["answer"])

                    st.markdown("---")
                    st.markdown("**Källor:**")

                    for source in data["sources"]:
                        st.markdown(
                            f'<p class="source-text">🔗 {source}</p>',
                            unsafe_allow_html=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.error("Error: API-anropet misslyckades.")

            except Exception as e:
                st.error(f"Kunde inte ansluta till servern: {e}")