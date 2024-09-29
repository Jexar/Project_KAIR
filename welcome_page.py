import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_welcome_page():
    # Custom CSS
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

    # Welcome message
    st.markdown('<p class="welcome-text">Welcome, Doctor!</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-text">Your Clinical Decision Support System awaits.</p>', unsafe_allow_html=True)

    # Load and display a medical-themed Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json"  # A medical-themed animation
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=400, key="medical_animation")

    # Add a button to proceed to the main application
    if st.button("Enter Clinical Decision Support System", key="enter_app"):
        st.session_state.page = "main"
        st.rerun()

if __name__ == "__main__":
    show_welcome_page()
