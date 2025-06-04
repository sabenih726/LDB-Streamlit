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

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='color:#f7901e;'>📑 PT LAMAN DAVINDO BAHMAN</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:bold;'>{get_greeting()}</p>", unsafe_allow_html=True)

        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()

def render_upload_form():
    st.markdown("## Upload Dokumen PDF")
    uploaded_files = st.file_uploader("Upload file", type=["pdf"], accept_multiple_files=True)
    doc_type = st.selectbox("Jenis Dokumen", ["SKTT", "EVLN", "ITAS", "ITK", "Notifikasi"])
    use_name = st.checkbox("Gunakan Nama untuk Rename", value=True)
    use_passport = st.checkbox("Gunakan Nomor Paspor untuk Rename", value=True)
    return uploaded_files, doc_type, use_name, use_passport

def render_main_app():
    render_sidebar()
    st.title("📑 Extraction of Immigration Documents")
    uploaded_files, doc_type, use_name, use_passport = render_upload_form()

    if uploaded_files:
        if st.button("Proses File PDF", type="primary"):
            from file_handler import process_pdfs
            df, excel_path, renamed_files, zip_path, temp_dir = process_pdfs(uploaded_files, doc_type, use_name, use_passport)

            st.success("Ekstraksi berhasil!")
            st.dataframe(df)
            with open(excel_path, "rb") as f:
                st.download_button("Download Excel", data=f, file_name="Hasil_Ekstraksi.xlsx")
            with open(zip_path, "rb") as f:
                st.download_button("Download ZIP", data=f, file_name="Renamed_Files.zip")
            import shutil
            shutil.rmtree(temp_dir)
