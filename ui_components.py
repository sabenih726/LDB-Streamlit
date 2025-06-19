# Tambahkan fungsi-fungsi ini ke file ui_components.py

def initialize_session_state():
    """Initialize session state for menu navigation and theme"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False
    # Tambahkan theme state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'

def render_dark_mode_css():
    """Render CSS untuk dark mode"""
    st.markdown('''
    <style>
    /* Hide Streamlit branding and unnecessary elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Dark background */
    .stApp {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    /* Dark sidebar styling */
    .css-1d391kg {
        background-color: #1e293b !important;
        color: #f8fafc !important;
    }
    
    /* Dark header styling */
    .header {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #f8fafc !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #475569;
    }
    
    /* Dark container */
    .container {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #475569;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Dark upload area */
    .uploadfile {
        border: 2px dashed #64748b !important;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background-color: #334155 !important;
        color: #f8fafc !important;
        margin: 1rem 0;
    }
    
    .uploadfile:hover {
        border-color: #3b82f6 !important;
        background-color: #1e40af !important;
    }
    
    /* Dark cards */
    .card {
        background-color: #334155 !important;
        color: #f8fafc !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #64748b;
        margin: 0.5rem 0;
    }
    
    /* Dark alerts */
    .alert-info {
        background-color: #1e3a8a !important;
        border: 1px solid #3b82f6 !important;
        color: #dbeafe !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #92400e !important;
        border: 1px solid #f59e0b !important;
        color: #fef3c7 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Dark buttons */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: 1px solid #1d4ed8 !important;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        border-color: #1e40af !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Dark dataframe styling */
    .stDataFrame {
        border: 1px solid #64748b !important;
        border-radius: 8px;
        background-color: #1e293b !important;
    }
    
    /* Dark text inputs */
    .stTextInput > div > div > input {
        background-color: #334155 !important;
        border: 1px solid #64748b !important;
        border-radius: 6px;
        padding: 0.5rem;
        color: #f8fafc !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Dark selectbox */
    .stSelectbox > div > div > div {
        background-color: #334155 !important;
        border: 1px solid #64748b !important;
        border-radius: 6px;
        color: #f8fafc !important;
    }
    
    /* Dark file uploader */
    .stFileUploader > div {
        border: 1px solid #64748b !important;
        border-radius: 8px;
        padding: 1rem;
        background-color: #334155 !important;
        color: #f8fafc !important;
    }
    
    /* Dark typography */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    
    /* Dark divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #64748b, transparent) !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Dark sidebar elements */
    .sidebar-header {
        color: #f8fafc !important;
        background: linear-gradient(135deg, #1e40af, #3b82f6) !important;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Dark tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #334155 !important;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #3b82f6 !important;
        background-color: #1e293b !important;
    }
    
    /* Dark metrics */
    .metric-container {
        background-color: #334155 !important;
        border: 1px solid #64748b !important;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Dark scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #64748b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
    ''', unsafe_allow_html=True)

def render_light_mode_css():
    """Render CSS untuk light mode (CSS yang sudah ada)"""
    st.markdown('''
    <style>
    /* Hide Streamlit branding and unnecessary elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Clean background */
    .stApp {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
    }
    
    /* Simple header styling */
    .header {
        background-color: #2c3e50 !important;
        color: white !important;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Clean container */
    .container {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    /* Simple upload area */
    .uploadfile {
        border: 2px dashed #dee2e6 !important;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
        margin: 1rem 0;
    }
    
    .uploadfile:hover {
        border-color: #007bff !important;
        background-color: #e3f2fd !important;
    }
    
    /* Clean cards */
    .card {
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    
    /* Simple alerts */
    .alert-info {
        background-color: #d1ecf1 !important;
        border: 1px solid #bee5eb !important;
        color: #0c5460 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd !important;
        border: 1px solid #ffeaa7 !important;
        color: #856404 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Clean buttons */
    .stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #0056b3 !important;
    }
    
    /* Clean dataframe styling */
    .stDataFrame {
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        background-color: #ffffff !important;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Clean text inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 6px;
        padding: 0.5rem;
        color: #1f2937 !important;
    }
    
    /* Clean selectbox */
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        border: 1px solid #ced4da !important;
        border-radius: 6px;
        color: #1f2937 !important;  
    }
    
    /* Simple progress bar */
    .stProgress > div > div > div {
        background-color: #007bff !important;
    }
    
    /* Clean file uploader */
    .stFileUploader > div {
        border: 1px solid #dee2e6 !important;
        border-radius: 8px;
        padding: 1rem;
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Remove default margins */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Clean typography */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    /* Simple divider */
    hr {
        border: none !important;
        height: 1px !important;
        background-color: #dee2e6 !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Light scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    </style>
    ''', unsafe_allow_html=True)

def render_auto_mode_css():
    """Render CSS untuk auto mode (deteksi sistem)"""
    # Untuk auto mode, kita bisa menggunakan media query atau JavaScript
    # Untuk kesederhanaan, kita gunakan light mode sebagai default
    render_light_mode_css()

def apply_theme_css():
    """Terapkan CSS berdasarkan theme yang dipilih"""
    if st.session_state.theme == 'Dark':
        render_dark_mode_css()
    elif st.session_state.theme == 'Light':
        render_light_mode_css()
    else:  # Auto
        render_auto_mode_css()

def render_css_styles():
    """Render CSS styles berdasarkan theme yang aktif"""
    apply_theme_css()

def render_settings_page():
    """Render settings page dengan theme switching yang berfungsi"""
    st.markdown('''
    <div class="header">
        <h1 style="margin-bottom: 0.5rem;">⚙️ System Settings</h1>
        <p style="opacity: 0.8;">Konfigurasi sistem dan preferensi aplikasi</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔧 General", "📁 File Settings", "👤 User Preferences"])
    
    with tab1:
        st.markdown("### General Settings")
        st.selectbox("Default Language", ["Indonesian", "English"])
        st.selectbox("Timezone", ["Asia/Jakarta", "UTC", "Asia/Singapore"])
        st.checkbox("Enable Email Notifications", value=True)
        st.checkbox("Auto-backup Data", value=True)
    
    with tab2:
        st.markdown("### File Processing Settings")
        st.slider("Max File Size (MB)", 1, 100, 50)
        st.selectbox("Default Document Type", ["SKTT", "EVLN", "ITAS", "ITK", "Notifikasi", "DKPTKA"])
        st.checkbox("Auto-rename Files", value=True)
        st.checkbox("Create Backup Copies", value=False)
    
    with tab3:
        st.markdown("### User Preferences")
        
        # Theme selector dengan fungsionalitas
        current_theme_index = ["Light", "Dark", "Auto"].index(st.session_state.theme)
        theme_choice = st.selectbox(
            "Theme", 
            ["Light", "Dark", "Auto"],
            index=current_theme_index,
            key="theme_selector"
        )
        
        # Handle theme change
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.success(f"✅ Theme berhasil diubah ke {theme_choice} mode!")
            time.sleep(0.5)  # Brief pause untuk user feedback
            st.rerun()
        
        # Show current theme status
        theme_status = {
            'Light': '☀️ Light Mode',
            'Dark': '🌙 Dark Mode', 
            'Auto': '🔄 Auto Mode'
        }
        st.info(f"Current Theme: {theme_status[st.session_state.theme]}")
        
        st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        st.number_input("Items per Page", min_value=10, max_value=100, value=25)
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings berhasil disimpan!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Update fungsi render_main_app untuk menggunakan CSS dinamis
def render_main_app():
    """Main application render function dengan theme support"""
    # Initialize session state (termasuk theme)
    initialize_session_state()
    
    # Apply CSS styles berdasarkan theme
    render_css_styles()  # Ini akan memanggil apply_theme_css()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page based on current_page
    if st.session_state.current_page == 'Home':
        render_home_content()
    elif st.session_state.current_page == 'Document':
        render_document_page()
    elif st.session_state.current_page == 'Client':
        render_client_page()
    elif st.session_state.current_page == 'Settings':
        render_settings_page()
    else:
        # Default to home if unknown page
        st.session_state.current_page = 'Home'
        render_home_content()
