import streamlit as st
from ui_components import login_page, render_main_app
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Ekstraksi Dokumen Imigrasi - PT Laman Davindo Bahman",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
def initialize_session_state():
    """Initialize all required session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'login_attempt' not in st.session_state:
        st.session_state.login_attempt = 0
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "user"
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "light"

def add_modern_css():
    """Add modern CSS styling with animations and better UX"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #2563eb;
        --primary-hover: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 10px 25px rgba(0,0,0,0.1);
        --border-radius: 12px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, var(--primary-color), var(--primary-hover));
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-hover);
    }
    
    /* Header styling */
    .app-header {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .app-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .app-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--card-shadow);
        border: 1px solid rgba(0,0,0,0.05);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .custom-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--background-gradient);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background: var(--primary-hover);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed var(--primary-color);
        border-radius: var(--border-radius);
        background: linear-gradient(45deg, rgba(37, 99, 235, 0.05), rgba(37, 99, 235, 0.1));
        padding: 2rem;
        text-align: center;
        transition: var(--transition);
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-hover);
        background: linear-gradient(45deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.15));
        transform: scale(1.02);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: var(--background-gradient);
        border-radius: 10px;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(45deg, rgba(5, 150, 105, 0.1), rgba(5, 150, 105, 0.05));
        border: 1px solid var(--success-color);
        border-radius: var(--border-radius);
        color: var(--success-color);
    }
    
    .stError {
        background: linear-gradient(45deg, rgba(220, 38, 38, 0.1), rgba(220, 38, 38, 0.05));
        border: 1px solid var(--error-color);
        border-radius: var(--border-radius);
        color: var(--error-color);
    }
    
    .stWarning {
        background: linear-gradient(45deg, rgba(217, 119, 6, 0.1), rgba(217, 119, 6, 0.05));
        border: 1px solid var(--warning-color);
        border-radius: var(--border-radius);
        color: var(--warning-color);
    }
    
    .stInfo {
        background: linear-gradient(45deg, rgba(37, 99, 235, 0.1), rgba(37, 99, 235, 0.05));
        border: 1px solid var(--primary-color);
        border-radius: var(--border-radius);
        color: var(--primary-color);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0,0,0,0.02);
        padding: 0.5rem;
        border-radius: var(--border-radius);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: var(--transition);
        border: none;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(37, 99, 235, 0.1);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--card-shadow);
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
        border-right-color: var(--primary-color) !important;
    }
    
    /* Metric styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        text-align: center;
        transition: var(--transition);
        border-left: 4px solid var(--primary-color);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--secondary-color);
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    .slide-up {
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .app-header h1 {
            font-size: 2rem;
        }
        
        .custom-card {
            padding: 1.5rem;
        }
        
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background: var(--success-color);
    }
    
    .status-processing {
        background: var(--warning-color);
    }
    
    .status-error {
        background: var(--error-color);
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Footer styling */
    .app-footer {
        margin-top: 3rem;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(45deg, #f8fafc, #f1f5f9);
        border-radius: var(--border-radius);
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    
    .app-footer p {
        margin: 0.25rem 0;
        color: var(--secondary-color);
        font-size: 0.9rem;
    }
    
    /* Custom select box */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid rgba(0,0,0,0.1);
        transition: var(--transition);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid rgba(0,0,0,0.1);
        transition: var(--transition);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Show a beautiful loading animation"""
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <div style="
            width: 50px; 
            height: 50px; 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #2563eb; 
            border-radius: 50%; 
            animation: spin 1s linear infinite;
        "></div>
    </div>
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def show_app_header():
    """Display modern app header"""
    st.markdown("""
    <div class="app-header fade-in">
        <h1>📄 Sistem Ekstraksi Dokumen Imigrasi</h1>
        <p>PT Laman Davindo Bahman - Advanced Document Processing System</p>
    </div>
    """, unsafe_allow_html=True)

def show_status_card(title, value, icon="📊"):
    """Display a modern status card"""
    st.markdown(f"""
    <div class="metric-card slide-up">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def check_session_timeout():
    """Check if user session has timed out with better UX"""
    if st.session_state.logged_in:
        current_time = datetime.now()
        session_duration = current_time - st.session_state.session_start_time
        timeout_duration = timedelta(hours=8)
        
        # Show warning 30 minutes before timeout
        warning_time = timeout_duration - timedelta(minutes=30)
        
        if session_duration > warning_time and session_duration < timeout_duration:
            remaining_time = timeout_duration - session_duration
            minutes_left = int(remaining_time.total_seconds() / 60)
            
            st.warning(f"⚠️ Sesi akan berakhir dalam {minutes_left} menit. Simpan pekerjaan Anda!")
            
            if st.button("🔄 Perpanjang Sesi"):
                st.session_state.session_start_time = datetime.now()
                st.success("✅ Sesi berhasil diperpanjang!")
                st.rerun()
        
        elif session_duration > timeout_duration:
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.error("🔒 Sesi telah berakhir. Silakan login kembali untuk keamanan.")
            time.sleep(2)
            st.rerun()

def show_system_status():
    """Show system status in sidebar"""
    with st.sidebar:
        st.markdown("### 🖥️ Status Sistem")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="status-indicator status-online"></span>**Online**', unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{datetime.now().strftime('%H:%M')}**")
        
        if st.session_state.logged_in:
            session_duration = datetime.now() - st.session_state.session_start_time
            hours = int(session_duration.total_seconds() / 3600)
            minutes = int((session_duration.total_seconds() % 3600) / 60)
            
            st.markdown(f"**Durasi Sesi:** {hours}j {minutes}m")
            st.markdown(f"**User:** {st.session_state.username}")
            st.markdown(f"**Role:** {st.session_state.user_role.title()}")

def main():
    """Main application function with modern UI"""
    # Initialize session state
    initialize_session_state()
    
    # Add modern CSS
    add_modern_css()
    
    # Check session timeout
    check_session_timeout()
    
    # Show system status in sidebar
    show_system_status()
    
    # Main application logic
    try:
        if not st.session_state.logged_in:
            # Show header even on login page
            show_app_header()
            login_page()
        else:
            # Show header for logged in users
            show_app_header()
            
            # Show main app
            render_main_app()
            
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan dalam aplikasi: {str(e)}")
        
        with st.expander("🔧 Informasi Debug", expanded=False):
            st.code(str(e))
            st.info("💡 Silakan refresh halaman atau hubungi administrator jika masalah berlanjut.")
        
        # Recovery options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh Halaman"):
                st.rerun()
        with col2:
            if st.button("🏠 Kembali ke Home"):
                st.session_state.clear()
                st.rerun()
        with col3:
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.rerun()

def show_app_footer():
    """Show modern app footer"""
    st.markdown("""
    <div class="app-footer">
        <p><strong>PT Laman Davindo Bahman</strong></p>
        <p>Immigration Document Extraction System</p>
        <p>Version 2.0 - 2025 | Powered by Streamlit & Python</p>
        <p style="font-size: 0.8rem; opacity: 0.7;">
            🔒 Secure • 🚀 Fast • 📱 Responsive
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
    show_app_footer()
