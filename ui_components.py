import streamlit as st
from auth import logout
from helpers import get_greeting

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 style="text-align:center;">🖥️ PT LAMAN DAVINDO BAHMAN</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;">Sistem Ekstraksi Dokumen Imigrasi</p>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")

            if st.session_state.login_attempt > 0:
                st.error(f"Username atau password salah! (Percobaan ke-{st.session_state.login_attempt})")

            submit = st.form_submit_button("Login")
            if submit:
                from auth import login
                login()

def render_header():
    st.markdown('''
    <style>
    body {
        background-color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    .modern-header {
        background-color: #1d4ed8;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .upload-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .modern-button {
        background: linear-gradient(to right, #1d4ed8, #2563eb);
        color: white;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        border-radius: 0.375rem;
        transition: background 0.3s ease;
    }
    .modern-button:hover {
        background: linear-gradient(to right, #2563eb, #1e40af);
    }
    </style>
    <div class="modern-header">
        <h1 style="margin: 0;">📑 Immigration Document Extraction</h1>
        <p style="margin: 0; opacity: 0.9;">Upload your PDF and let the system extract key data automatically</p>
    </div>
    ''', unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='color:#1d4ed8;'>📌 Main Menu</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:bold;'>{get_greeting()}</p>", unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

def render_upload_section():
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    st.subheader("Upload PDF Files")
    uploaded_files = st.file_uploader("Choose one or more PDF files", type=["pdf"], accept_multiple_files=True)
    doc_type = st.selectbox("Document Type", ["SKTT", "EVLN", "ITAS", "ITK", "Notifikasi"])
    use_name = st.checkbox("Use Name for Filename", value=True)
    use_passport = st.checkbox("Use Passport Number for Filename", value=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_files, doc_type, use_name, use_passport

def render_process_button(label="Proses File PDF"):
    st.markdown('<div style="text-align:center; margin-top: 1rem;">', unsafe_allow_html=True)
    return st.button(label, key="modern_process_button")

def render_loader():
    st.markdown("""
    <div style="text-align:center; padding: 2rem;">
        <img src="https://i.imgur.com/llF5iyg.gif" width="60" />
        <p style="margin-top: 1rem; color: #475569;">Processing your documents, please wait...</p>
    </div>
    """, unsafe_allow_html=True)

def render_main_app():
    render_sidebar()
    render_header()
    uploaded_files, doc_type, use_name, use_passport = render_upload_section()

    if uploaded_files:
        if render_process_button():
            from file_handler import process_pdfs
            render_loader()
            df, excel_path, renamed_files, zip_path, temp_dir = process_pdfs(uploaded_files, doc_type, use_name, use_passport)
            st.success("Ekstraksi berhasil!")
            st.dataframe(df)
            with open(excel_path, "rb") as f:
                st.download_button("Download Excel", data=f, file_name="Hasil_Ekstraksi.xlsx")
            with open(zip_path, "rb") as f:
                st.download_button("Download ZIP", data=f, file_name="Renamed_Files.zip")
            import shutil
            shutil.rmtree(temp_dir)
