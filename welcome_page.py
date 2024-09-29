import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_welcome_page():
    st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .welcome-text {
        font-size: 3rem;
        font-weight: bold;
        color: #399696;
        text-align: center;
        padding: 2rem 0;
    }
    .sub-text {
        font-size: 1.5rem;
        color: #4dc8a2;
        text-align: center;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="welcome-text">Welcome to the Clinical Decision Support System</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Please select your role:</p>', unsafe_allow_html=True)

    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json"
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=300, key="medical_animation")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("I'm a Doctor", key="doctor_button"):
            st.session_state.user_role = "doctor"
            st.session_state.page = "main"
            st.rerun()

    with col2:
        if st.button("I'm a Patient", key="patient_button"):
            st.session_state.user_role = "patient"
            st.session_state.page = "main"
            st.rerun()

if __name__ == "__main__":
    show_welcome_page()
