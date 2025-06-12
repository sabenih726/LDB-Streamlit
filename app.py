import streamlit as st
from ui_components import login_page, render_main_app

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
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'login_attempt' not in st.session_state:
        st.session_state.login_attempt = 0
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "user"
    if 'session_start_time' not in st.session_state:
        from datetime import datetime
        st.session_state.session_start_time = datetime.now()

def add_custom_css():
    """Add custom CSS for better mobile and desktop experience"""
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stSelectbox > div > div {
            font-size: 0.9rem;
        }
        
        .uploadfile {
            padding: 1rem !important;
        }
    }
    
    /* Better button styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border-radius: 0.75rem;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 0.5rem;
    }
    
    /* Tab styling improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 0.5rem 0.5rem 0 0;
        font-weight: 500;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: #1d4ed8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def check_session_timeout():
    """Check if user session has timed out (optional feature)"""
    if st.session_state.logged_in:
        from datetime import datetime, timedelta
        current_time = datetime.now()
        session_duration = current_time - st.session_state.session_start_time
        
        # Set timeout to 8 hours (adjust as needed)
        timeout_duration = timedelta(hours=8)
        
        if session_duration > timeout_duration:
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.warning("Session telah berakhir. Silakan login kembali.")
            st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Add custom CSS
    add_custom_css()
    
    # Check session timeout (optional)
    # check_session_timeout()
    
    # Main application logic
    try:
        if not st.session_state.logged_in:
            login_page()
        else:
            render_main_app()
            
    except Exception as e:
        st.error(f"Terjadi kesalahan dalam aplikasi: {str(e)}")
        st.info("Silakan refresh halaman atau hubungi administrator jika masalah berlanjut.")
        
        # Add debug info in development (remove in production)
        if st.checkbox("Show Debug Info (Development Only)"):
            st.exception(e)

def show_app_info():
    """Show application information in sidebar footer"""
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #64748b; font-size: 0.8rem;'>
                <p><strong>PT Laman Davindo Bahman</strong></p>
                <p>Immigration Document Extraction System</p>
                <p>Version 2.0 - 2025</p>
            </div>
            """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()
    show_app_info()
