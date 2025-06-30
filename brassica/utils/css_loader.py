import streamlit as st
from pathlib import Path

def load_css(file_name):
    """Memuat file CSS eksternal."""
    file_path = Path(__file__).parent.parent / file_name
    if not file_path.exists():
        st.error(f"File CSS tidak ditemukan di: {file_path}")
        return
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
