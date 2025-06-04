import streamlit as st
from ui_components import login_page, render_main_app

st.set_page_config(
    page_title="Ekstraksi Dokumen Imigrasi",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'login_attempt' not in st.session_state:
    st.session_state.login_attempt = 0

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        render_main_app()

if __name__ == "__main__":
    main()