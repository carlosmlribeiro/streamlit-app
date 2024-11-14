import streamlit as st
from langchain.llms import OpenAI

st.title("Chatbot")

#openai_api_key = st.sidebar.text_input("openai API key", type="password")

openai_api_key = st.secrets["OPENAI_API_KEY"]

def generate_response(input_text):
    model = OpenAI(temperature=0, api_key=openai_api_key)
    st.info(model.invoke(input_text))

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "Who is Lewis Hamilton?",
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Invalid API key")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)