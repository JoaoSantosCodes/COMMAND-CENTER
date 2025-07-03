import streamlit as st

def inject_responsive_css():
    """
    Injeta CSS customizado para responsividade no Streamlit.
    """
    css = '''
    <style>
    @media (max-width: 900px) {
      .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
      }
      .stButton>button {
        font-size: 1.1em;
      }
      .stMarkdown, .stText, .stDataFrame, .stTable {
        font-size: 1.05em;
      }
      .st-expanderHeader {
        font-size: 1.1em;
      }
    }
    @media (max-width: 600px) {
      .main .block-container {
        padding-left: 0.2rem;
        padding-right: 0.2rem;
      }
      .stButton>button {
        font-size: 1.2em;
      }
      .stMarkdown, .stText, .stDataFrame, .stTable {
        font-size: 1.1em;
      }
      .st-expanderHeader {
        font-size: 1.15em;
      }
    }
    /* Contraste para inputs no tema escuro */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] > div {
      background: #23272f !important;
      color: #f4f4f5 !important;
      border: 1.5px solid #27272a !important;
      box-shadow: none !important;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
      border: 2px solid #6366f1 !important;
      background: #27272a !important;
    }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True) 