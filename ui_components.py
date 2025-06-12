import streamlit as st
import pandas as pd
from datetime import datetime
import time
import hashlib

# Mock user database (in production, use proper database)
USERS_DB = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "full_name": "Administrator"
    },
    "user": {
        "password": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user", 
        "full_name": "Regular User"
    }
}

def login_page():
    """Modern login page with better UX"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="custom-card fade-in" style="margin-top: 2rem;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #2563eb; margin-bottom: 0.5rem;">🔐 Login</h2>
                <p style="color: #64748b;">Masuk ke sistem ekstraksi dokumen</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            # Login form
            with st.form("login_form", clear_on_submit=False):
                st.markdown("#### 👤 Kredensial Login")
                
                username = st.text_input(
                    "Username",
                    placeholder="Masukkan username Anda",
                    help="Gunakan 'admin' atau 'user' untuk demo"
                )
                
                password = st.text_input(
                    "Password", 
                    type="password",
                    placeholder="Masukkan password Anda",
                    help="Password: admin123 atau user123"
                )
                
                col_login, col_demo = st.columns(2)
                
                with col_login:
                    login_button = st.form_submit_button(
                        "🚀 Login", 
                        use_container_width=True,
                        type="primary"
                    )
                
                with col_demo:
                    demo_button = st.form_submit_button(
                        "👁️ Demo Login",
                        use_container_width=True
                    )
            
            # Handle login
            if login_button or demo_button:
                if demo_button:
                    username = "user"
                    password = "user123"
                
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = USERS_DB[username]["role"]
                    st.session_state.session_start_time = datetime.now()
                    
                    # Show success message with animation
                    success_placeholder = st.empty()
                    with success_placeholder:
                        st.success(f"✅ Selamat datang, {USERS_DB[username]['full_name']}!")
                        time.sleep(1)
                        
                    # Show loading animation
                    with st.spinner("🔄 Memuat dashboard..."):
                        time.sleep(2)
                    
                    st.rerun()
                else:
                    st.session_state.login_attempt += 1
                    
                    if st.session_state.login_attempt >= 3:
                        st.error("🚫 Terlalu banyak percobaan login. Silakan tunggu beberapa saat.")
                        time.sleep(3)
                    else:
                        st.error(f"❌ Username atau password salah. Percobaan ke-{st.session_state.login_attempt}")
            
            # Show demo credentials
            with st.expander("🔑 Demo Credentials", expanded=False):
                st.markdown("""
                **Admin Account:**
                - Username: `admin`
                - Password: `admin123`
                
                **User Account:**
                - Username: `user`
                - Password: `user123`
                """)
            
            # Show login attempts warning
            if st.session_state.login_attempt > 0:
                attempts_left = 3 - st.session_state.login_attempt
                if attempts_left > 0:
                    st.warning(f"⚠️ {attempts_left} percobaan login tersisa")

def authenticate_user(username, password):
    """Authenticate user credentials"""
    if username in USERS_DB:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return USERS_DB[username]["password"] == hashed_password
    return False

def render_main_app():
    """Render the main application interface"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        
        # User info card
        st.markdown(f"""
        <div class="custom-card" style="margin-bottom: 1rem; padding: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                <div style="font-weight: 600; color: #2563eb;">{USERS_DB[st.session_state.username]['full_name']}</div>
                <div style="font-size: 0.8rem; color: #64748b;">{st.session_state.user_role.title()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        menu_options = [
            "📄 Ekstraksi PDF",
            "📊 Dashboard", 
            "📈 Statistik",
            "⚙️ Pengaturan"
        ]
        
        if st.session_state.user_role == "admin":
            menu_options.append("👥 Manajemen User")
        
        selected_menu = st.selectbox(
            "Pilih Menu:",
            menu_options,
            index=0
        )
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
    
    # Main content area
    if selected_menu == "📄 Ekstraksi PDF":
        render_pdf_extraction()
    elif selected_menu == "📊 Dashboard":
        render_dashboard()
    elif selected_menu == "📈 Statistik":
        render_statistics()
    elif selected_menu == "⚙️ Pengaturan":
        render_settings()
    elif selected_menu == "👥 Manajemen User" and st.session_state.user_role == "admin":
        render_user_management()

def render_pdf_extraction():
    """Render PDF extraction interface"""
    st.markdown("## 📄 Ekstraksi Teks dari PDF")
    
    # Create tabs for different extraction modes
    tab1, tab2, tab3 = st.tabs(["📤 Upload File", "🔗 URL PDF", "📁 Batch Processing"])
    
    with tab1:
        render_file_upload_extraction()
    
    with tab2:
        render_url_extraction()
    
    with tab3:
        render_batch_extraction()

def render_file_upload_extraction():
    """Render file upload extraction interface"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>📤 Upload PDF File</h4>
            <p>Pilih file PDF yang ingin diekstrak teksnya</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Pilih file PDF",
            type=['pdf'],
            help="Maksimal ukuran file: 10MB"
        )
        
        if uploaded_file is not None:
            # File info
            file_details = {
                "Nama File": uploaded_file.name,
                "Ukuran": f"{uploaded_file.size / 1024:.2f} KB",
                "Tipe": uploaded_file.type
            }
            
            st.markdown("#### 📋 Informasi File")
            for key, value in file_details.items():
                st.markdown(f"**{key}:** {value}")
            
            # Extraction options
            st.markdown("#### ⚙️ Opsi Ekstraksi")
            
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                extract_images = st.checkbox("🖼️ Ekstrak gambar", value=False)
                preserve_formatting = st.checkbox("📝 Pertahankan format", value=True)
            
            with col_opt2:
                extract_tables = st.checkbox("📊 Ekstrak tabel", value=True)
                ocr_mode = st.checkbox("🔍 Mode OCR", value=False)
            
            # Extract button
            if st.button("🚀 Mulai Ekstraksi", type="primary", use_container_width=True):
                with st.spinner("🔄 Memproses file PDF..."):
                    # Simulate processing time
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("📖 Membaca struktur PDF...")
                        elif i < 60:
                            status_text.text("🔍 Mengekstrak teks...")
                        elif i < 90:
                            status_text.text("🔧 Memproses hasil...")
                        else:
                            status_text.text("✅ Finalisasi...")
                        time.sleep(0.05)
                    
                    # Show results
                    st.success("✅ Ekstraksi berhasil!")
                    
                    # Mock extracted text
                    extracted_text = """
                    Ini adalah contoh teks yang diekstrak dari PDF.
                    
                    DOKUMEN IMIGRASI
                    Nomor: 12345/IMG/2025
                    Tanggal: 15 Januari 2025
                    
                    Nama: John Doe
                    Kewarganegaraan: Indonesia
                    Nomor Paspor: A1234567
                    
                    Status: Approved
                    Berlaku hingga: 15 Januari 2026
                    """
                    
                    # Display extracted text
                    st.markdown("#### 📝 Hasil Ekstraksi")
                    st.text_area(
                        "Teks yang diekstrak:",
                        value=extracted_text,
                        height=300,
                        help="Anda dapat menyalin teks ini"
                    )
                    
                    # Download options
                    col_dl1, col_dl2, col_dl3 = st.columns(3)
                    
                    with col_dl1:
                        st.download_button(
                            "💾 Download TXT",
                            data=extracted_text,
                            file_name=f"{uploaded_file.name}_extracted.txt",
                            mime="text/plain"
                        )
                    
                    with col_dl2:
                        # Convert to CSV format
                        csv_data = "Field,Value\nNama,John Doe\nKewarganegaraan,Indonesia\nNomor Paspor,A1234567"
                        st.download_button(
                            "📊 Download CSV",
                            data=csv_data,
                            file_name=f"{uploaded_file.name}_extracted.csv",
                            mime="text/csv"
                        )
                    
                    with col_dl3:
                        st.download_button(
                            "📄 Download JSON",
                            data='{"nama": "John Doe", "kewarganegaraan": "Indonesia", "nomor_paspor": "A1234567"}',
                            file_name=f"{uploaded_file.name}_extracted.json",
                            mime="application/json"
                        )
    
    with col2:
        # Statistics card
        st.markdown("""
        <div class="custom-card">
            <h4>📊 Statistik Hari Ini</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Mock statistics
        st.metric("📄 File Diproses", "24", "↗️ +3")
        st.metric("⏱️ Rata-rata Waktu", "2.3s", "↘️ -0.5s")
        st.metric("✅ Tingkat Sukses", "98.5%", "↗️ +1.2%")
        
        # Recent activity
        st.markdown("#### 🕒 Aktivitas Terkini")
        recent_activities = [
            "📄 document_1.pdf - Berhasil",
            "📄 immigration_form.pdf - Berhasil", 
            "📄 passport_scan.pdf - Berhasil",
            "📄 visa_application.pdf - Error"
        ]
        
        for activity in recent_activities:
            if "Error" in activity:
                st.markdown(f"🔴 {activity}")
            else:
                st.markdown(f"🟢 {activity}")

def render_url_extraction():
    """Render URL extraction interface"""
    st.markdown("### 🔗 Ekstraksi dari URL PDF")
    
    url_input = st.text_input(
        "Masukkan URL PDF:",
        placeholder="https://example.com/document.pdf",
        help="Pastikan URL dapat diakses secara publik"
    )
    
    if url_input:
        if st.button("🔍 Validasi & Ekstrak URL", type="primary"):
            with st.spinner("🔄 Memvalidasi URL..."):
                time.sleep(2)
                st.success("✅ URL valid! Memulai ekstraksi...")
                time.sleep(1)
                st.info("📄 Fitur ini akan segera tersedia!")

def render_batch_extraction():
    """Render batch extraction interface"""
    st.markdown("### 📁 Batch Processing")
    
    st.info("🚀 Fitur batch processing memungkinkan Anda memproses multiple file PDF sekaligus")
    
    uploaded_files = st.file_uploader(
        "Pilih multiple file PDF:",
        type=['pdf'],
        accept_multiple_files=True,
        help="Anda dapat memilih hingga 10 file sekaligus"
    )
    
    if uploaded_files:
        st.markdown(f"#### 📋 {len(uploaded_files)} File Dipilih")
        
        # Show file list
        for i, file in enumerate(uploaded_files, 1):
            st.markdown(f"{i}. **{file.name}** ({file.size / 1024:.2f} KB)")
        
        if st.button("🚀 Proses Semua File", type="primary"):
            st.info("📄 Fitur batch processing akan segera tersedia!")

def render_dashboard():
    """Render dashboard with analytics"""
    st.markdown("## 📊 Dashboard Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">📄 156</div>
            <div class="metric-label">Total Dokumen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">✅ 98.5%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">⚡ 2.3s</div>
            <div class="metric-label">Avg Processing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">👥 12</div>
            <div class="metric-label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 📈 Dokumen Diproses (7 Hari Terakhir)")
        
        # Mock data for chart
        chart_data = pd.DataFrame({
            'Tanggal': pd.date_range('2025-01-09', periods=7),
            'Jumlah': [23, 45, 56, 78, 32, 67, 89]
        })
        
        st.line_chart(chart_data.set_index('Tanggal'))
    
    with col_chart2:
        st.markdown("#### 🥧 Jenis Dokumen")
        
        doc_types = pd.DataFrame({
            'Jenis': ['Paspor', 'Visa', 'Permit', 'Lainnya'],
            'Jumlah': [45, 32, 28, 15]
        })
        
        st.bar_chart(doc_types.set_index('Jenis'))

def render_statistics():
    """Render detailed statistics"""
    st.markdown("## 📈 Statistik Detail")
    
    # Time range selector
    col_time1, col_time2, col_time3 = st.columns(3)
    
    with col_time1:
        start_date = st.date_input("📅 Tanggal Mulai", datetime.now().date())
    
    with col_time2:
        end_date = st.date_input("📅 Tanggal Akhir", datetime.now().date())
    
    with col_time3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data", type="secondary"):
            st.success("✅ Data berhasil diperbarui!")
    
    # Detailed statistics table
    st.markdown("#### 📋 Detail Statistik")
    
    stats_data = pd.DataFrame({
        'Tanggal': pd.date_range('2025-01-09', periods=7),
        'Total Dokumen': [23, 45, 56, 78, 32, 67, 89],
        'Berhasil': [22, 44, 55, 76, 31, 65, 87],
        'Gagal': [1, 1, 1, 2, 1, 2, 2],
        'Success Rate (%)': [95.7, 97.8, 98.2, 97.4, 96.9, 97.0, 97.8]
    })
    
    st.dataframe(
        stats_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Export options
    st.markdown("#### 💾 Export Data")
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        st.download_button(
            "📊 Export CSV",
            data=stats_data.to_csv(index=False),
            file_name="statistics.csv",
            mime="text/csv"
        )
    
    with col_exp2:
        st.download_button(
            "📄 Export JSON",
            data=stats_data.to_json(orient='records'),
            file_name="statistics.json",
            mime="application/json"
        )
    
    with col_exp3:
        if st.button("📧 Email Report"):
            st.info("📧 Laporan akan dikirim ke email Anda!")

def render_settings():
    """Render settings page"""
    st.markdown("## ⚙️ Pengaturan Sistem")
    
    # User preferences
    st.markdown("### 👤 Preferensi User")
    
    col_pref1, col_pref2 = st.columns(2)
    
    with col_pref1:
        language = st.selectbox(
            "🌐 Bahasa Interface:",
            ["Bahasa Indonesia", "English", "中文"]
        )
        
        theme = st.selectbox(
            "🎨 Tema:",
            ["Light", "Dark", "Auto"]
        )
    
    with col_pref2:
        notifications = st.checkbox("🔔 Notifikasi Email", value=True)
        auto_save = st.checkbox("💾 Auto Save", value=True)
    
    # Processing settings
    st.markdown("### 🔧 Pengaturan Pemrosesan")
    
    col_proc1, col_proc2 = st.columns(2)
    
    with col_proc1:
        max_file_size = st.slider(
            "📏 Maksimal Ukuran File (MB):",
            min_value=1,
            max_value=50,
            value=10
        )
        
        ocr_quality = st.selectbox(
            "🔍 Kualitas OCR:",
            ["Standard", "High", "Ultra High"]
        )
    
    with col_proc2:
        concurrent_jobs = st.slider(
            "⚡ Concurrent Jobs:",
            min_value=1,
            max_value=10,
            value=3
        )
        
        output_format = st.multiselect(
            "📄 Format Output Default:",
            ["TXT", "CSV", "JSON", "XML"],
            default=["TXT", "CSV"]
        )
    
    # Save settings
    if st.button("💾 Simpan Pengaturan", type="primary"):
        st.success("✅ Pengaturan berhasil disimpan!")

def render_user_management():
    """Render user management (admin only)"""
    st.markdown("## 👥 Manajemen User")
    
    if st.session_state.user_role != "admin":
        st.error("🚫 Akses ditolak. Hanya admin yang dapat mengakses halaman ini.")
        return
    
    # User list
    st.markdown("### 📋 Daftar User")
    
    users_data = pd.DataFrame({
        'Username': ['admin', 'user', 'john_doe', 'jane_smith'],
        'Full Name': ['Administrator', 'Regular User', 'John Doe', 'Jane Smith'],
        'Role': ['admin', 'user', 'user', 'user'],
        'Last Login': ['2025-01-15 10:30', '2025-01-15 09:15', '2025-01-14 16:45', '2025-01-13 14:20'],
        'Status': ['Active', 'Active', 'Active', 'Inactive']
    })
    
    st.dataframe(
        users_data,
        use_container_width=True,
        hide_index=True
    )
    
    # Add new user
    st.markdown("### ➕ Tambah User Baru")
    
    with st.form("add_user_form"):
        col_user1, col_user2 = st.columns(2)
        
        with col_user1:
            new_username = st.text_input("Username:")
            new_fullname = st.text_input("Nama Lengkap:")
        
        with col_user2:
            new_role = st.selectbox("Role:", ["user", "admin"])
            new_password = st.text_input("Password:", type="password")
        
        if st.form_submit_button("➕ Tambah User", type="primary"):
            st.success(f"✅ User '{new_username}' berhasil ditambahkan!")

def logout_user():
    """Handle user logout"""
    # Clear session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.success("👋 Anda telah berhasil logout!")
    time.sleep(1)
    st.rerun()
