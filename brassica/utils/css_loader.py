import streamlit as st
from pathlib import Path

def load_css(file_path): # Ganti parameter dari file_name menjadi file_path karena sekarang akan menerima Path object atau string absolut
    """Memuat file CSS eksternal."""
    with open(file_path, "r") as f: 
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
