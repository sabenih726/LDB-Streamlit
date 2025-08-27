import streamlit as st
from ui_components import render_main_app
import time

# Page configuration
st.set_page_config(
    page_title="Ekstraksi Dokumen Imigrasi - PT Laman Davindo Bahman",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
def initialize_session_state():
    """Initialize all required session state variables"""
    # Set logged_in selalu True untuk skip login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True
    if 'username' not in st.session_state:
        st.session_state.username = "Admin"  # Default username
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "admin"
    if 'session_start_time' not in st.session_state:
        from datetime import datetime
        st.session_state.session_start_time = datetime.now()
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"

def add_custom_css():
    """Add custom CSS (copy dari kode asli Anda)"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom variables for theming */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #10b981;
        --accent-color: #f59e0b;
        --danger-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        background: var(--bg-primary);
        border-radius: 1rem;
        box-shadow: var(--shadow-xl);
        margin: 1rem;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border-radius: 1rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .app-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), #2563eb);
        color: white;
        border: none;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
    }
    </style>
    """, unsafe_allow_html=True)

def add_app_header():
    """Add application header"""
    st.markdown("""
    <div class="app-header fade-in">
        <h1>🖥️ PT LAMAN DAVINDO BAHMAN</h1>
        <p>Sistem Ekstraksi Dokumen Imigrasi</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_cards():
    """Create dashboard metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📄 Total Dokumen",
            value="1,234",
            delta="12 hari ini",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="✅ Berhasil Diproses",
            value="1,180",
            delta="95.6%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="⏱️ Rata-rata Waktu",
            value="2.3 detik",
            delta="-0.5 detik",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="👥 Pengguna Aktif",
            value="24",
            delta="3 hari ini",
            delta_color="normal"
        )

def main():
    """Main application function - langsung ke dashboard tanpa login"""
    # Initialize session state
    initialize_session_state()
    
    # Add custom CSS
    add_custom_css()
    
    # Add app header
    add_app_header()
    
    # Main application logic - langsung render main app
    try:
        # Create dashboard metrics
        create_metric_cards()
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Render main app
        render_main_app()
        
    except Exception as e:
        st.error(f"⛔ Terjadi kesalahan dalam aplikasi: {str(e)}")
        st.info("💡 Silakan refresh halaman atau hubungi administrator jika masalah berlanjut.")
        
        # Add debug info in development
        if st.checkbox("🔧 Show Debug Info (Development Only)"):
            st.exception(e)

def show_app_info():
    """Show application information in sidebar footer"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary); font-size: 0.8rem;'>
            <p><strong>🏢 PT Laman Davindo Bahman</strong></p>
            <p>📄 Immigration Document Extraction System</p>
            <p>📄 Version 2.1 - 2025</p>
            <p>👤 User: """ + st.session_state.get('username', 'Admin') + """</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
    show_app_info()
