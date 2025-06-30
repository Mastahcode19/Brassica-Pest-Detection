import streamlit as st
from pathlib import Path # Import Path

def load_css(file_name):
    """Memuat file CSS eksternal."""
    # Dapatkan path absolut dari direktori file saat ini (css_loader.py)
    current_dir = Path(__file__).parent

    # Gabungkan direktori saat ini dengan jalur relatif file CSS
    # Misalnya, jika css_loader.py ada di 'utils/', dan style.css ada di 'assets/css/'
    # Anda perlu menavigasi ke atas satu level (parent), lalu ke 'assets/css/'
    # Atau, lebih sederhana, ubah parameter file_name di app.py

    # Mari kita asumsikan struktur:
    # your-app-root/
    # ├── utils/
    # │   └── css_loader.py
    # ├── assets/
    # │   └── css/
    # │       └── style.css
    # └── app.py

    # Jika app.py memanggil load_css("assets/css/style.css")
    # dan css_loader.py ada di utils/, maka path dari css_loader.py adalah 'your-app-root/utils'
    # Kita perlu naik satu level (ke 'your-app-root'), lalu masuk ke 'assets/css/'

    css_file_path = current_dir.parent / file_name # Ini akan menjadi 'your-app-root' / 'assets/css/style.css'

    with open(css_file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
