import streamlit as st 
import requests


st.title("Utlandsstudier Chat")

user_input= st.text_input("Ställ dina frågor kring utlandsstudier")

if st.button("Skicka"):
    if user_input:
        response = requests.post(
            "http://localhost:8003/chat",
            json={"question":user_input}
        )

        if response.status_code == 200:
            data=response.json()

            st.subheader("Svar:")
            st.write(data["answer"])
            st.subheader("källor:")
            for source in data ["sources"]:
                 st.write("-"+ source)
        else:
             st.error("Error, API-call failed")






    