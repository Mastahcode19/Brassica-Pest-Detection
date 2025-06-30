# --- Import Library Program ---
import streamlit as st
import base64
import pandas as pd
import io
import pytz
import toml
import os
import PIL
import helper
import settings
import requests
from ultralytics import YOLO
from pymongo import MongoClient
from datetime import datetime
from streamlit_option_menu import option_menu
from utils.css_loader import load_css
from streamlit_product_card import product_card
from pathlib import Path


# --- Konfigurasi Layout Awal Halaman ---
st.set_page_config(
    page_title="Brassica - Deteksi Hama Kembang Kol",
    page_icon="./assets/logo/cauli-iconic.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Kumpulan Asset Gambar ---

ICON_IMAGE = "./assets/logo/cauli-iconic.png"

HOME2_IMAGE = "https://ik.imagekit.io/mastah/cauliflower-2.jpg?updatedAt=1750140626362"
HOME3_IMAGE = "https://ik.imagekit.io/mastah/ilmiah-kol.jpeg?updatedAt=1750169351840"
HOME4_IMAGE = "https://ik.imagekit.io/mastah/grayak.jpg?updatedAt=1751268506864"
HOME5_IMAGE = "https://ik.imagekit.io/mastah/grayakhd.PNG?updatedAt=1751269410373"
HOME6_IMAGE = "https://ik.imagekit.io/mastah/ulat2.jpeg?updatedAt=1750214362020"
HOME7_IMAGE = "https://ik.imagekit.io/mastah/ulat4.jpeg?updatedAt=1750218504224"
HOME8_IMAGE = "https://ik.imagekit.io/mastah/BlurObject.png?updatedAt=1750663450502"
HOME9_IMAGE = "https://ik.imagekit.io/mastah/ClearObject.png?updatedAt=1750663451179"
BRASSICA = "https://ik.imagekit.io/mastah/brassica_logo.png?updatedAt=1749799795443"



# --- Header Navigasi ---
def header():
    st.markdown(f"""
    <div class="cauli-logo">
        <img src="{BRASSICA}" alt="Brassica Logo" style="width: auto;">
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation menggunakan option_menu
    with st.sidebar:

        # --- Mulai Kontainer Menu ---
        st.markdown('<div class="menu-container">', unsafe_allow_html=True)

        # --- Logo ---
        st.markdown('<img src="https://ik.imagekit.io/mastah/logo-jernih.png?updatedAt=1749800376538" style="margin-top: -70px;">', unsafe_allow_html=True)

        # --- Menu Navigation ---  
        selected = option_menu(
            menu_title="",
            options=["Beranda", "Profil Hama", "Panduan", "Deteksi Hama", "Riwayat"],
            icons=["house", "bug", "book", "cpu", "clock-history"],
            default_index=0,
            styles={
                "container": {"padding": "0px", "background-color": "transparent"},
                "icon": {"color": "#4c956c", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#b5c99a",
                },
                "nav-link-selected": {
                    "background-color": "#b5c99a",
                    "color": "#297c4d",
                    "font-weight": "bold",
                    "font-family": "'DM Serif Text', serif",
                },
            },
        )

        # --- Footer Versi Aplikasi ---
        st.markdown("""
        <div style="margin-top: -10px; text-align: center; font-size: 16px; color: #2c6e49;">
            <strong>Versi Aplikasi:</strong> 1.0.0<br>
            <small>&copy; 2025 by Kevin</small>
        </div>
        """, unsafe_allow_html=True)

    return selected

# --- Halaman Utama ---
def halaman_utama():
    """Menampilkan konten untuk Halaman Utama."""
    # --- Hero Section ---
    MEDIA_LINK_HOME1_IMAGE = "https://ik.imagekit.io/mastah/cauli-desktop.png?updatedAt=1749792657775"
    MEDIA_LINK_HOME2_IMAGE = "https://ik.imagekit.io/mastah/cauli-hp.png?updatedAt=1749792658526"
    st.markdown(f"""
    <div class="hero-section desktop-hero" style="background-image: url('{MEDIA_LINK_HOME1_IMAGE}')"></div>
    <div class="hero-section mobile-hero" style="background-image: url('{MEDIA_LINK_HOME2_IMAGE}')"></div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='custom-title'>Selamat Datang Di Brassica! Yuk, Kenalan Dulu👋</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cauli-desc" style='font-size: 18px; line-height: 1.7;'>
    <strong>Brassica</strong> adalah solusi cerdas berbasis <em>kecerdasan buatan (AI)</em> yang dirancang untuk membantu petani dan masyarakat umum dalam mengidentifikasikan berbagai jenis hama yang paling sering menyerang tanaman bunga kol.
    Cukup unggah gambar hama pada bunga kol, dan Brassica akan mengidentifikasi jenis hama tersebut secara <strong>realtime</strong> dan <strong>akurat</strong>.
    Sekaligus memberi tips cara pengendalian untuk masing-masing hama. 
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
    """, unsafe_allow_html=True)

    # --- Fitur Deteksi Hama --- 
    st.markdown("<div class='custom-title'>🌿 Bunga Kol ( <i>Brassica oleracea</i> L. )</div>", unsafe_allow_html=True)

    col1_img, col2_img = st.columns(2)
    with col1_img:
        st.markdown("""
        <div class="cauli-desc">
        <strong>Bunga kol</strong> atau akrab sering disebut sebagai kembang kol ini dikenal secara ilmiah sebagai <i>Brassica oleracea var. botrytis</i> L., merupakan salah satu jenis sayuran dari keluarga kubis-kubisan (<i>Brassicaceae</i>) yang populer dan banyak dikonsumsi di berbagai belahan dunia.
        <br>
        Bagian yang dimanfaatkan dari tanaman ini adalah bunga mudanya yang kaya akan nutrisi, seperti vitamin C, vitamin K, folat, serta antioksidan alami. Tidak hanya bernilai gizi tinggi, kembang kol juga memiliki nilai ekonomi penting bagi petani hortikultura.<br><br> 
    </div>
        """, unsafe_allow_html=True)
        st.image(HOME3_IMAGE, caption="Klasifikasi Ilmiah Bunga Kol", use_container_width=True)

    with col2_img:
        st.markdown(f"""
    <div style="padding: 16px; text-align: center;">
        <img src="{HOME2_IMAGE}" width="100%" height="500px" style="border-radius: 15px;">
        <p style="margin-top: 8px; font-size: 14px; color: #555; text-align: center;">
        Gambar Tanaman Bunga Kol
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
<hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
""", unsafe_allow_html=True)

    # --- Fitur Deteksi Hama ---
    st.markdown("<div class='custom-title'>🎯 Fitur Deteksi Hama Cerdas</div>", unsafe_allow_html=True)
    st.write("""
        
        """)
    st.markdown("""
        <div class="cauli-desc">
        Aplikasi ini memanfaatkan <strong>kecerdasan buatan (AI)</strong> untuk menganalisis gambar kembang kol 
        dan mendeteksi keberadaan hama secara otomatis. Dengan menggunakan <strong>algoritma YOLO</strong>, 
        sebuah model deteksi objek yang sudah dilatih akan memproses gambar dan memberikan kotak pembatas (bounding box) di sekitar hama yang terdeteksi secara tepat dan akurat.
        <br><br>Lihat perbedaan antara gambar sebelum dan sesudah diproses oleh sistem deteksi hama untuk mengetahui bagaimana objek teridentifikasi secara otomatis<br><br>
    </div>
        """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image(HOME4_IMAGE, caption="Gambar Asli", use_container_width=True)
        
    with col2:
        st.image(HOME5_IMAGE, caption="Gambar Sesudah Terdeteksi Hama", use_container_width=True)

    st.markdown("""
<hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
""", unsafe_allow_html=True)

    # --- Keunggulan Aplikasi ---
    st.markdown("<div class='custom-title'>🐛 Hama Yang Sering Menyerang</div>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        clicked_aphid = product_card(
    product_name="Aphid",
    description="Hidup di bawah daun, batang, dan bakal bunga. Mengisap cairan daun muda dan jaringan lunak tanaman.",
    product_image="https://ik.imagekit.io/mastah/aphid.jpeg?updatedAt=1750168267256",
    key="basic_card",
    picture_position="top",
    image_width_percent=50,
    image_aspect_ratio="1/1",
    image_object_fit="cover",
    font_url="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
    styles={
        "card": {
            "border-radius": "12px",
            "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
            "background-color": "#9ec272",
        },
        "title": {
            "font-family": "'Bodoni', serif",
            "font-size": "1.4em",
            "font-weight": "bold",
            "color": "#141413",
        },
        "text": {
            "font-family": "'Montserrat', sans-serif",
            "font-size": "0.9em",
            "color": "#141413"
        },
    },
    mobile_breakpoint_behavior="stack top"
)   

    with col2:
        clicked_basic = product_card(
    product_name="Spodoptera litura",
    description="Ulat ini menyerang tanaman bunga kol dengan cara melubangi bagian daun secara masif ",
    product_image="https://ik.imagekit.io/mastah/ulatgrayak5.jpg?updatedAt=1750168267117",
    key="basic_card2",
    picture_position="top",
    image_width_percent=50,
    image_aspect_ratio="1/1",
    image_object_fit="cover",
     font_url="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
    styles={
        "card": {
            "border-radius": "12px",
            "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
            "background-color": "#9ec272",
        },
        "title": {
            "font-family": "'Bodoni', serif",
            "font-size": "1.4em",
            "font-weight": "bold",
            "color": "#141413",
        },
        "text": {
            "font-family": "'Montserrat', sans-serif",
            "font-size": "0.9em",
            "color": "#141413"
        },
    },
    mobile_breakpoint_behavior="stack top"
) 

    with col3:
        clicked_basic = product_card(
    product_name="Agrotis ipsilon",
    description="Menyerang pangkal batang bunga kol, terutama pada fase bibit hingga tanaman muda",
    product_image="https://ik.imagekit.io/mastah/ulat%20tanah1.jpg?updatedAt=1750168267076",
    key="basic_card3",
    picture_position="top",
    image_width_percent=50,
    image_aspect_ratio="1/1",
    image_object_fit="cover",
     font_url="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
    styles={
        "card": {
            "border-radius": "12px",
            "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
            "background-color": "#9ec272",
        },
        "title": {
            "font-family": "'Bodoni', serif",
            "font-size": "1.4em",
            "font-weight": "bold",
            "color": "#141413",
        },
        "text": {
            "font-family": "'Montserrat', sans-serif",
            "font-size": "0.9em",
            "color": "#141413"
        },
    },
    mobile_breakpoint_behavior="stack top"
) 

    with col4:
        clicked_basic = product_card(
    product_name="Plutella xylostella",
    description="Ulat ini menyerang daun muda tanaman bunga kol, terutama di bagian bawah daun.",
    product_image="https://ik.imagekit.io/mastah/Image%205.jpeg?updatedAt=1750238441085",
    key="basic_card4",
    picture_position="top",
    image_width_percent=50,
    image_aspect_ratio="1/1",
    image_object_fit="cover",
     font_url="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap",
    styles={
        "card": {
            "border-radius": "12px",
            "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
            "background-color": "#9ec272",
        },
        "title": {
            "font-family": "'Bodoni', serif",
            "font-size": "1.4em",
            "font-weight": "bold",
            "color": "#141413",
        },
        "text": {
            "font-family": "'Montserrat', sans-serif",
            "font-size": "0.9em",
            "color": "#141413"
        },
    },
    mobile_breakpoint_behavior="stack top"

) 
    
    st.success("Lihat pada halaman profil hama untuk baca lebih lanjut")

    st.markdown("""
    <hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
    """, unsafe_allow_html=True)

     # --- Kerusakan Yang Ditimbulkan ---
    st.markdown("<div class='custom-title'>⛔ Kerusakan Yang Ditimbulkan Hama</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="cauli-desc">
        Berikut ini merupakan beberapa contoh berupa lampiran gambar yang menunjukkan kondisi tanaman bunga kol (<i>Brassica oleracea</i>) saat mengalami serangan hama.
    </div>
        """, unsafe_allow_html=True)
    st.write("")

    col1, col2= st.columns(2, gap="small")

    with col1:
        st.markdown(f"""
    <div style="padding: 16px; text-align: center;">
        <img src="{HOME6_IMAGE}" width="100%" height="390px" style="border-radius: 15px;">
        <div style="margin-top: 10px; font-size:17px;">
            <small>Kerusakan Parah Akibat Hama</small>
        </div>
    </div>
    """,unsafe_allow_html=True)
        
        
    with col2:
        st.markdown(f"""
    <div style="padding: 16px; text-align: center;">
        <img src="{HOME7_IMAGE}" width="100%" height="400px" style="border-radius: 15px;">
        <div style="margin-top: 10px; font-size:17px;">
            <small>Kerusakan Daun Akibat Hama</small>
        </div>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
    """, unsafe_allow_html=True)


    # --- Panduan Pengendalian Hama ---
    st.markdown("<div class='custom-title'>💡 Tata Cara Pengendalian Hama Umum</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="cauli-desc">
        Berbagai metode pengendalian dapat diterapkan secara terpadu agar serangan hama dapat diminimalkan dengan 
        efektif dan ramah lingkungan. Berikut ini adalah tata cara pengendalian hama umum yang meliputi pengendalian secara kultur teknis, fisik/mekanis, hayati, dan kimiawi sebagai pilihan terakhir.<br><br>
    </div>
        """, unsafe_allow_html=True)

# Membuat card pertama

    st.markdown(
    """
    <div class="card">
        <div class="card-title">1. Pengendalian Secara Kultur Teknis</div>
        <p><t>Pengendalian kultur teknis adalah usaha yang dilakukan dengan memodifikasi lingkungan atau teknik budidaya agar tidak menguntungkan bagi hama.</p>
        <div class="card-content">
            <ul>
                <li><b>Rotasi Tanaman:</b>Hindari penanaman bunga kol secara terus-menerus di lahan yang sama untuk memutus siklus hidup hama seperti Plutella xylostella.</li>
                <li><b>Sanitasi Lahan:</b>Bersihkan gulma dan sisa tanaman setelah panen untuk mencegah tempat persembunyian hama.</li>
                <li><b>Pengaturan jarak tanam:</b>Jarak tanam yang tepat mengurangi kelembaban mikro yang disukai hama dan mempermudah sirkulasi udara.</li>
                <li><b>Penanaman varietas tahan hama:</b>Gunakan varietas bunga kol yang lebih tahan terhadap serangan hama tertentu.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div class="card">
        <div class="card-title">2. Pengendalian Secara Fisik/Mekanis</div>
        <p>Teknik ini bertujuan mengurangi populasi hama secara langsung menggunakan alat atau perlakuan fisik.</p>
        <div class="card-content">
            <ul>
                <li><b>Pengambilan manual:</b>Hama seperti ulat atau telur kutu daun dapat dipungut langsung dan dimusnahkan.</li>
                <li><b>Penggunaan perangkap:</b>Pasang perangkap lem kuning untuk mengendalikan hama seperti kutu daun (aphid).</li>
                <li><b>Pemasangan mulsa plastik:</b>Mulsa dapat mengurangi kelembaban dan menghambat perkembangan telur dan larva hama.</li>
                <li><b>Penggunaan jaring pelindung:</b>Jaring kasa halus mencegah serangan hama dari luar terutama Spodoptera litura.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div class="card">
        <div class="card-title">3. Pengendalian Secara Kultur Teknis</div>
        <p>Pengendalian hayati menggunakan musuh alami (predator, parasitoid, atau patogen) untuk mengendalikan populasi hama.</p>
        <div class="card-content">
            <ul>
                <li><b>Pelepasan parasitoid:</b> Diadegma semiclausum untuk ulat daun kubis (P. xylostella).</li>
                <li><b>Aplikasi jamur entomopatogen:</b>Seperti Beauveria bassiana atau Metarhizium anisopliae untuk menginfeksi kutu daun dan ulat.</li>
                <li><b>Peningkatan populasi musuh alami:</b>Melalui konservasi habitat (menanam tanaman bunga seperti kenikir atau bayam untuk menarik predator alami seperti kepik dan laba-laba).</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
    """
    <div class="card">
        <div class="card-title">4.Pengendalian Kimiawi</div>
        <p>Penggunaan pestisida kimia dilakukan apabila cara lain tidak efektif</p>
        <div class="card-content">
            <ul>
                <li><b>Gunakan pestisida selektif:</b>Pilih insektisida yang tidak membunuh musuh alami, seperti pestisida berbahan aktif abamektin atau spinosad.</li>
                <li><b>Rotasi bahan aktif:</b>Untuk mencegah resistensi hama terhadap satu jenis insektisida.</li>
                <li><b>Hindari penyemprotan berlebihan.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

#Sumber Referensi
    with st.expander("📒 Sumber Referensi"):
        st.markdown("""
<div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
    <a class="ref-link" href="https://hortikultura.pertanian.go.id/wp-content/uploads/2024/11/JUKNIS-KUBIS_watermark.pdf"  target="_blank"><strong>hortikultura.pertanian.go</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://media.neliti.com/media/publications/225828-kultur-teknis-sebagai-dasar-pengendalian-54332347.pdf"  target="_blank"><strong>media.neliti.com</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://mplk.politanikoe.ac.id/index.php/teknik-pengendalian-opt/pengendalian-opt-secara-kultur-teknis"  target="_blank"><strong>mplk.politanikoe.ac.id</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://mirror.unpad.ac.id/bse/Kurikulum_2013/Kelas_10_SMK_Agribisnis_Tanaman_Sayuran_1.pdf"  target="_blank"><strong>mirror.unpad.ac.id</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://www.slideshare.net/slideshow/agribisnis-tanaman-sayuran-xi3pdf/255429040"  target="_blank"><strong>slideshare.net</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://repository.ub.ac.id/id/eprint/130939/"  target="_blank"><strong>repository.ub.ac.id</strong>: Pelajari lebih lanjut</a>
    <a class="ref-link" href="https://ejournal.unsrat.ac.id/v3/index.php/samrat-agrotek/article/view/54524"  target="_blank"><strong>journal.unsrat.ac.id</strong>: Pelajari lebih lanjut</a>
</div>
        """,unsafe_allow_html=True)


    with st.expander("🖼️ Sumber Gambar"):
        st.markdown("""
<div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
    <a class="ref-link" href="https://creazilla.com/media/photo/244297/food-fresh-vegetarian" target="_blank"><strong>Gambar Tanaman Bunga Kol </strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://i0.wp.com/gardengnomeacademy.com/wp-content/uploads/2024/02/cauliflower1.jpg?resize=570,285&ssl=1"  target="_blank"><strong>Gambar Thumbnail Bunga Kol </strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://horticultureunlimited.com/could-you-have-an-aphid-infestation/"  target="_blank"><strong>Gambar Aphid</strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://ik.imagekit.io/mastah/ulatgrayak5.jpg?updatedAt=1750168267117"  target="_blank"><strong>Gambar Spodoptera litura</strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://www.shutterstock.com/image-photo/larvae-cutworm-soil-most-likely-agrotis-1867792180?id=1867792180&irclickid=zUtXJ7wbxxycRboUNi3BeXeCUksVvEX1K14CSM0&irgwc=1&pl=426523-42119&utm_medium=Affiliate&utm_campaign=Elevated%20Logic%2C%20LLC&utm_source=426523&utm_term=STOCKSNAP_SEARCH-AUTHENTIC_API&utm_content=42119"  target="_blank"><strong>Gambar Agrotis ipsilon</strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://www.gardeningknowhow.com/edible/vegetables/cauliflower/controlling-cauliflower-insects.htm"  target="_blank"><strong>Gambar Plutella xylostella</strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://ik.imagekit.io/mastah/ulat2.jpeg?updatedAt=1750214362020"  target="_blank"><strong>Gambar Kerusakan Dari Hama1</strong>: Lihat Gambar</a>
    <a class="ref-link" href="https://ik.imagekit.io/mastah/ulat4.jpeg?updatedAt=1750218504224"  target="_blank"><strong>Gambar Kerusakan Dari Hama2</strong>: Lihat Gambar</a>
</div>
        """,unsafe_allow_html=True)    


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def halaman_profil_hama():
    st.markdown("<div class='custom-title'>🐛 Profil Hama Pada Bunga Kol</div>", unsafe_allow_html=True)
    st.info("✨ Halaman ini berisi informasi detail mengenai hama utama, siklus hidup, dan kerusakan yang ditimbulkannya.")

    gif_url_1 = "https://ik.imagekit.io/mastah/ulatanim1.gif?updatedAt=1751273086234"
    gif_url_2 = "https://ik.imagekit.io/mastah/daunanim.gif?updatedAt=1751273086582"

    # Ambil dan konversi GIF 1
    try:
        response_1 = requests.get(gif_url_1, stream=True)
        response_1.raise_for_status()  # Memeriksa apakah request berhasil
        contents_1 = response_1.content
        data_url_1 = base64.b64encode(contents_1).decode("utf-8")
    except Exception as e:
        st.error(f"Gagal memuat GIF dari: {gif_url_1}. Error: {str(e)}")
        data_url_1 = None

    # Ambil dan konversi GIF 2
    try:
        response_2 = requests.get(gif_url_2, stream=True)
        response_2.raise_for_status()
        contents_2 = response_2.content
        data_url_2 = base64.b64encode(contents_2).decode("utf-8")
    except Exception as e:
        st.error(f"Gagal memuat GIF dari: {gif_url_2}. Error: {str(e)}")
        data_url_2 = None

    # --- Tampilkan GIF jika berhasil dimuat ---
    if data_url_1 and data_url_2:
        st.markdown(f"""
        <div style='position: relative; width: 100%;'>
            <div style='
                position: absolute;
                top: -10px;
                left: 610px;
                text-align: center;
                z-index: 1;
            '>
                <img src="data:image/gif;base64,{data_url_1}" width="120" alt="Ulat Animation">
            </div>
            <div style='
                position: absolute;
                top: -10px;
                left: 830px;
                text-align: center;
                z-index: 1;
            '>
                <img src="data:image/gif;base64,{data_url_2}" width="90" alt="Daun Animation">
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Salah satu atau kedua GIF gagal dimuat. Periksa URL atau koneksi internet.")

    

    
# Lalu bungkus tab dan isinya dengan container luar
    with st.container():
        tab1, tab2, tab3, tab4 = st.tabs(["Aphid", "Spodoptera litura", "Agrotis ipsilon", "Plutella xylostella"])

        with tab1:
            with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 10px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/aphid.png?updatedAt=1751197173874"
                         alt="Aphid pada bunga kol"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
    """, unsafe_allow_html=True)
                

# garis pemisah
                st.markdown("""
    <hr style="height:4px;border:none;color:#28a745;background-color:#97a970;" />
""", unsafe_allow_html=True)

    
#Penjelasan Aphid**************
                st.markdown("""
<div class="tab-section">
    <p><strong>Aphid</strong> atau kutu daun adalah serangga kecil berukuran 1–2 mm yang hidup berkelompok dan mengisap cairan dari jaringan tanaman, termasuk tanaman bunga kol. Warna tubuhnya rata-rata bewarna hijau. 
    Aphid dikenal sebagai hama penting karena selain merusak tanaman secara langsung, juga berperan sebagai vektor penularan virus tanaman.</p>
    <p>Serangan aphid menyebabkan daun menjadi lengket, menggulung, dan pada kasus berat hanya menyisakan tulang daun saja. Selain itu, cairan manis yang dikeluarkan aphid dapat mengundang semut dan memicu pertumbuhan 
    jamur hitam pada daun.Karena kemampuannya mengisap cairan, aphid menyebabkan kerusakan langsung pada tanaman berupa daun yang menguning, menggulung, mengkerut, dan pertumbuhan tanaman menjadi terhambat bahkan bisa menyebabkan kematian tanaman jika serangan berat.</p>
</div>""", 
    unsafe_allow_html=True)

                st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Gejala Serangan Aphid pada Bunga Kol
</div>

<div style="font-size: 20px; color: #2f2f2f;">
        <ul>
            <li>Daun menjadi lengket dan tampak lapisan putih dari air liur aphid.</li>
            <li>Daun menggulung, menguning, dan akhirnya rusak parah.</li>
            <li>Pada serangan berat, daun hanya tersisa tulang daunnya saja.</li>
            <li>Pertumbuhan tanaman terhambat dan hasil panen menurun.</li>
        </ul>
</div>

</div>
""", unsafe_allow_html=True)
    
                st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Cara Penanganan Aphid pada Tanaman Bunga Kol
</div>

<div style="font-size: 20px; color: #2f2f2f;">
       <div class="sub-section-title">1. Pengendalian Mekanis dan Budidaya</div>
<ul>
    <li><strong>Sanitasi lahan:</strong> Bersihkan gulma dan sisa tanaman yang bisa menjadi inang aphid.</li>
    <li><strong>Rotasi tanaman:</strong> Hindari menanam bunga kol secara terus-menerus di lahan yang sama.</li>
    <li><strong>Tumpang sari:</strong> Menanam bunga kol bersama tanaman lain seperti bawang daun dapat mengurangi serangan aphid.</li>
</ul>

<div class="sub-section-title">2. Pengendalian Hayati (Biologis)</div>
<ul>
    <li><strong>Musuh alami:</strong> Lepaskan atau pelihara predator alami aphid seperti ladybug (kumbang kepik), lacewing, dan serangga bajak laut kecil di sekitar tanaman.</li>
    <li><strong>Tanaman refugia:</strong> Menanam bunga refugia di sekitar lahan dapat menarik musuh alami aphid.</li>
    <li><strong>Aplikasi biopestisida:</strong> Gunakan jamur entomopatogen seperti <em>Beauveria bassiana</em> atau <em>Metarhizium anisopliae</em> yang efektif menekan populasi aphid.</li>
</ul>

<div class="sub-section-title">3. Pengendalian Nabati (Organik)</div>
<ul>
    <li><strong>Pestisida nabati:</strong> Semprotkan ekstrak daun sirsak, daun nimba, sereh, atau pestisida nabati siap pakai seperti Naturo yang aman untuk tanaman dan lingkungan.</li>
    <li><strong>Minyak mineral dan piretrin:</strong> Minyak mineral dan senyawa piretrin dari bunga piretrum efektif membunuh aphid dengan cara mengganggu sistem pernapasan dan saraf serangga.</li>
</ul>

<div class="sub-section-title">4. Pengendalian Kimia</div>
<ul>
    <li><strong>Insektisida kimia:</strong> Gunakan insektisida berbahan aktif seperti abamektin, deltametrin, atau dimephos sesuai dosis anjuran dan hanya jika populasi aphid sudah melewati ambang ekonomi. Hindari penggunaan berlebihan agar tidak terjadi resistensi dan pencemaran lingkungan.</li>
</ul>
</div>
</div>

</div>
""", unsafe_allow_html=True)


            with st.expander("📒 Sumber Referensi"):
                    st.markdown("""

<div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
        <a class="ref-link" href="https://id.wikipedia.org/wiki/Kutu_daun"  target="_blank"><strong>id.wikipedia.org</strong>: Informasi tentang kutu daun</a>
        <a class="ref-link" href="https://journal.univetbantara.ac.id/index.php/agrisaintifika/article/download/5435/3167/22069"  target="_blank"><strong>journal.univetbantara.ac.id</strong>: Penelitian tentang aphid</a>
        <a class="ref-link" href="https://bioprotectionportal.com/id/resources/aphid-types-damage-control-methods/"  target="_blank"><strong>bioprotectionportal.com</strong>: Jenis-jenis kutu daun & metode pengendaliannya</a>
        <a class="ref-link" href="https://hortikultura.pertanian.go.id/wp-content/uploads/2016/12/Identifikasi-OPT-Kentang.pdf"  target="_blank"><strong>hortikultura.pertanian.go.id</strong>: Identifikasi hama pada tanaman kentang</a>
</div>
    """, unsafe_allow_html=True)

#Penjelasan Spodoptera**************
    with tab2:
        with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 10px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/spedopter.png?updatedAt=1751197174389"
                         alt="Aphid pada bunga kol"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
    """, unsafe_allow_html=True)
                
                st.markdown("""
<div class="tab-section">
    <p><strong>Spodoptera litura</strong>, yang dikenal sebagai ulat grayak, adalah hama penting yang menyerang berbagai tanaman, termasuk bunga kol. Larvanya sangat rakus dan memakan daun tanaman hingga berlubang dan tersisa hanya tulang daunnya, menyebabkan defoliasi berat yang menghambat pertumbuhan tanaman dan menurunkan hasil panen.
    Larva <em>S. litura</em> memiliki bintik hitam berbentuk bulan sabit pada setiap ruas abdomen dan aktif merusak tanaman terutama pada malam hari, sementara siang hari bersembunyi di tanah atau di bawah daun kering.</p>
</div>""", 
    unsafe_allow_html=True)

                st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Dampak Serangan pada Bunga Kol
</div>
<div style="font-size: 20px; color: #2f2f2f;">
<ul>
    <li>Serangan ulat grayak menyebabkan daun berlubang dan rusak parah.</li>
    <li>Pertumbuhan tanaman bunga kol terhambat dan hasil panen berkurang signifikan.</li>
    <li>Serangan pada tanaman muda dapat membuat tanaman kerdil dan buah berukuran kecil atau terlambat berkembang.</li>
</ul><br>
</div>
""", unsafe_allow_html=True)
    
                st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Cara Penanganan Spodoptera litura pada Bunga Kol
</div>

<div style="font-size: 20px; color: #2f2f2f;">
<div class="sub-section-title">1. Pengendalian Mekanis dan Budidaya</div>
<ul>
    <li><strong>Sanitasi lahan:</strong> Bersihkan gulma dan sisa tanaman yang dapat menjadi tempat persembunyian ulat.</li>
    <li><strong>Pengaturan jarak tanam:</strong> Gunakan jarak tanam optimal seperti 60 x 60 cm untuk mengurangi kelembaban mikro dan meningkatkan kesehatan tanaman.</li>
    <li><strong>Penyemprotan ekstrak daun Muntingia calabura:</strong> Dilakukan secara berkala (3 kali per minggu) untuk menurunkan intensitas serangan ulat karena kandungan alkaloid, saponin, dan flavonoid yang mengganggu pencernaan ulat.</li>
</ul>

<div class="sub-section-title">2. Pengendalian Hayati (Biologis)</div>
<ul>
    <li><strong>Bakteri entomopatogen:</strong> Gunakan isolat bakteri dari tanah seperti <em>Bacillus cereus</em> yang efektif meningkatkan mortalitas larva hingga 98%.</li>
    <li><strong>Jamur entomopatogen:</strong> Beauveria bassiana dan Metarhizium anisopliae efektif menekan populasi ulat grayak.</li>
    <li><strong>Musuh alami:</strong> Pelepasan parasitoid dan predator alami untuk pengendalian biologis yang berkelanjutan.</li>
</ul>

<div class="sub-section-title">3. Pengendalian Nabati (Organik)</div>
<ul>
    <li><strong>Pestisida nabati:</strong> Gunakan ekstrak daun kersen (<em>Muntingia calabura</em>) yang memiliki senyawa aktif untuk mengusir dan menghambat aktivitas ulat.</li>
    <li><strong>Ekstrak tanaman lain:</strong> Manfaatkan tanaman dengan efek insektisidal alami sebagai alternatif ramah lingkungan terhadap pestisida kimia.</li>
</ul>

<div class="sub-section-title">4. Pengendalian Kimia</div>
<ul>
    <li><strong>Insektisida kimia:</strong> Digunakan secara selektif dan sesuai dosis jika serangan sudah parah.</li>
    <li><strong>Rotasi bahan aktif:</strong> Untuk mencegah hama menjadi resisten terhadap satu jenis insektisida.</li>
    <li><strong>Prioritas akhir:</strong> Pengendalian kimia sebaiknya menjadi pilihan terakhir setelah metode mekanis, hayati, dan nabati telah diterapkan.</li>
</ul>
</div>
""", unsafe_allow_html=True)
                
        with st.expander("📒 Sumber Referensi"):
            st.markdown("""

    <div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
        <a class="ref-link" href="http://download.garuda.kemdikbud.go.id/article.php?article=2927094&val=16993&title=PENGARUH+JARAK+TANAM+DAN+INTERVAL+PENYEMPROTAN+EKSTRAK+DAUN+Muntingia+calabura+TERHADAP+HAMA+Spodoptera+litura+F+PADA+BUNGA+KOL+Brassica+oleracea+L"  target="_blank"><strong>download.garuda.kemdikbud.go.id</strong>: Penelitian Jarak Tanam</a>
        <a class="ref-link" href="https://journal.unsika.ac.id/agrotek/article/download/1170/pdf_17/3307"  target="_blank"><strong>journal.unsika.ac.id</strong>: Pengendalian Hama Bunga Kol</a>
        <a class="ref-link" href="https://ejournal.unsrat.ac.id/v3/index.php/eugenia/article/download/3567/3095/6719"  target="_blank"><strong>ejournal.unsrat.ac.id</strong>: Studi tentang OPT</a>
        <a class="ref-link" href="https://repository.ub.ac.id/172907/1/AGUNG%20PRASETIYO%20(2).pdf"  target="_blank"><strong>repository.ub.ac.id </strong>: Budidaya Bunga Kol</a>
    </div>
    """, unsafe_allow_html=True)

#Penjelasan Agrotis**************
    with tab3:
        with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 10px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/agrotis.png?updatedAt=1751197175286"
                         alt="Aphid pada bunga kol"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
    """, unsafe_allow_html=True)
                

        st.markdown("""
<div class="tab-section">
    <p><strong>Agrotis ipsilon</strong>, dikenal juga sebagai ulat tanah atau ulat grayak, adalah hama penting pada tanaman bunga kol dan kubis. Larvanya hidup di dalam tanah dan menyerang tanaman muda dengan cara menggigit pangkal batang hingga tanaman bisa terpotong dan mati.</p>
    <p>Serangan ulat tanah ini sangat merugikan karena dapat menyebabkan kerugian hingga <strong>75–90%</strong> pada bibit bunga kol yang baru ditanam, terutama pada awal musim kemarau. Populasi larva biasanya meningkat pada awal musim kemarau (Maret–April) dan menurun saat musim hujan. Siklus hidup ulat ini dipengaruhi oleh suhu udara; suhu rendah memperpanjang masa hidupnya dan sebaliknya.</p>

</div>""", unsafe_allow_html=True)
        
        st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Dampak Serangan pada Bunga Kol
</div>
<div style="font-size: 20px; color: #2f2f2f;">
    <ul>
        <li>Larva menyerang tanaman muda dengan cara menggigit pangkal batang.</li>
        <li>Tanaman menjadi mudah rapuh, rusak, bahkan bisa terpotong dan mati.</li>
        <li>Kerusakan paling parah terjadi pada fase awal pertumbuhan tanaman.</li>
    </ul><br></div>
""", unsafe_allow_html=True)
        

        st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Cara Penanganan Agrotis ipsilon pada Bunga Kol
</div>

<div style="font-size: 20px; color: #2f2f2f;">
<div class="sub-section-title">1. Pengendalian Mekanis dan Budidaya</div>
    <ul>
        <li><strong>Sanitasi lahan:</strong> Bersihkan sisa tanaman dan gulma yang bisa menjadi tempat persembunyian ulat.</li>
        <li><strong>Pengolahan tanah:</strong> Bajak atau gemburkan tanah untuk mengganggu pupa ulat yang berada di dalam tanah sehingga mati karena terkena sinar matahari.</li>
        <li><strong>Penanaman serempak:</strong> Tanam bunga kol secara serempak agar populasi hama lebih mudah dikendalikan.</li>
    </ul>

<div class="sub-section-title">2. Pengendalian Hayati (Biologis)</div>
    <ul>
        <li><strong>Musuh alami:</strong> Manfaatkan predator dan parasitoid ulat tanah, seperti beberapa jenis burung dan serangga pemangsa.</li>
        <li><strong>Jamur entomopatogen dan bakteri:</strong> Gunakan mikroorganisme seperti <em>Beauveria bassiana</em> dan <em>Bacillus thuringiensis</em> yang efektif mengendalikan populasi larva ulat tanah secara biologis.</li>
    </ul>

<div class="sub-section-title">3. Pengendalian Nabati (Organik)</div>
    <ul>
        <li><strong>Pestisida nabati:</strong> Gunakan ekstrak tanaman seperti <em>Tithonia diversifolia</em> (kipait/paitan) yang mengandung flavonoid, alkaloid, dan tannin yang bersifat repellent dan mempengaruhi saraf ulat.</li>
        <li><strong>Aman bagi lingkungan:</strong> Pestisida nabati ini aman bagi lingkungan dan petani serta menghasilkan produk pertanian bebas residu kimia.</li>
    </ul>

<div class="sub-section-title">4. Pengendalian Kimia</div>
    <ul>
        <li><strong>Insektisida kimia:</strong> Digunakan secara selektif dan sesuai dosis jika serangan sudah parah.</li>
        <li><strong>Pilih bahan aktif yang efektif:</strong> Pastikan insektisida yang digunakan cocok untuk ulat tanah.</li>
        <li><strong>Rotasi bahan aktif:</strong> Untuk mencegah hama menjadi resisten terhadap satu jenis insektisida.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
              
        with st.expander("📒 Sumber Referensi"):
            st.markdown("""

    <div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
        <a class="ref-link" href="hortikultura.pertanian.go.id"  target="_blank"><strong>hortikultura.pertanian.go.id</strong>: Teknologi Pengendalian OPT Kubis</a>
        <a class="ref-link" href="hortikultura.pertanian.go.id"  target="_blank"><strong>hortikultura.pertanian.go.id</strong>: PHT Pada Tanaman Kubis</a>
        <a class="ref-link" href="agronita.usxiitapanuli.ac.id"  target="_blank"><strong>agronita.usxiitapanuli.ac.id</strong>: Journal Agroteknologi Pertanian</a>
        <a class="ref-link" href="repository.unmuhjember.ac.id"  target="_blank"><strong>repository.unmuhjember.ac.id</strong>: Penyemprotan dan Konsentrasi Pestisida Nabati </a>
        <a class="ref-link" href="repository.unhas.ac.id"  target="_blank"><strong>repository.unhas.ac.id</strong>: Tindakan Penangan Hama</a>
        <a class="ref-link" href="repository.uir.ac.id"  target="_blank"><strong>repository.uir.ac.id</strong>: Pengaruh Pupuk Herbafarm</a>
    </div>
    """, unsafe_allow_html=True)

#Penjelasan Plutela**************
    with tab4:
        with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 10px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/plutela.png?updatedAt=1751197173901"
                         alt="Aphid pada bunga kol"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
    """, unsafe_allow_html=True)
                

        st.markdown("""
<div class="tab-section">
    <p><strong>Plutella xylostella</strong>, atau yang dikenal sebagai ulat tritip, adalah hama utama pada tanaman bunga kol. Larvanya berukuran sekitar 9–10 mm, berwarna hijau muda dengan tubuh silindris dan relatif licin. Ulat ini biasanya bersembunyi di bagian bawah daun dan memakan jaringan daun bagian bawah, sehingga daun tampak bernoda putih dan berlubang.</p>
    <p>Ulat ini memiliki kemampuan berkembang biak sangat cepat dan dapat ditemukan di berbagai ketinggian, dari dataran rendah hingga pegunungan. Serangan ulat tritip sering terjadi di lahan sayuran bunga kol dan menyebabkan kerusakan signifikan jika tidak dikendalikan sejak awal.</p>
</div>""", unsafe_allow_html=True)
        

        st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Dampak Serangan pada Bunga Kol
</div>
<div style="font-size: 20px; color: #2f2f2f;">
    <ul>
        <li>Larva membuat lubang-lubang pada daun akibat aktivitas menggerek jaringan daun bagian bawah.</li>
        <li>Kerusakan daun mengganggu proses fotosintesis, terutama pada daun muda dan titik tumbuh.</li>
        <li>Pertumbuhan tanaman terhambat dan pembentukan krop bunga kol menjadi tidak optimal.</li>
    </ul><br></div>
""", unsafe_allow_html=True)
        
        st.markdown("""
<div class="card-profil" style="">

<div class="section-title" style="font-size: 28px; font-weight: bold; margin-bottom: 10px;">
        Cara Penanganan Plutella xylostella pada Tanaman Bunga Kol
</div>

<div style="font-size: 20px; color: #2f2f2f;">
<div class="sub-section-title">1. Pengendalian Mekanis dan Budidaya</div>
    <ul>
        <li><strong>Pemangkasan daun terserang:</strong> Untuk mengurangi populasi larva dan cegah penyebaran lebih lanjut.</li>
        <li><strong>Penanaman secara serempak:</strong> Memudahkan pengelolaan hama dan mengurangi peluang infestasi bertahap.</li>
        <li><strong>Gunakan tanaman refugia:</strong> Menanam tanaman penarik musuh alami seperti marigold untuk menekan populasi ulat.</li>
    </ul>
<div class="sub-section-title">2. Pengendalian Hayati (Biologis)</div>
    <ul>
        <li><strong>Musuh alami:</strong> Manfaatkan predator alami seperti laba-laba, kumbang, dan parasitoid untuk kontrol biologis.</li>
        <li><strong>Bakteri dan jamur entomopatogen:</strong> Gunakan mikroba seperti <em>Bacillus thuringiensis</em> dan <em>Metarhizium anisopliae</em> yang efektif membunuh ulat secara aman dan ramah lingkungan.</li>
    </ul>

<div class="sub-section-title">3. Pengendalian Nabati (Organik)</div>
    <ul>
        <li><strong>Pestisida nabati:</strong> Gunakan ekstrak tanaman tertentu yang mengandung senyawa insektisidal alami untuk mengusir atau membunuh ulat tritip.</li>
        <li><strong>Asap cair:</strong> Sebagai alternatif ramah lingkungan yang dapat mengusir dan membunuh hama secara efektif.</li>
    </ul>
<div class="sub-section-title">4. Pengendalian Kimia</div>
    <ul>
        <li><strong>Insektisida kimia:</strong> Digunakan secara selektif dan sesuai dosis jika serangan sudah parah.</li>
        <li><strong>Pilih bahan aktif yang efektif:</strong> Pastikan insektisida bekerja baik terhadap ulat tritip.</li>
        <li><strong>Rotasi bahan aktif:</strong> Untuk mencegah hama menjadi resisten terhadap satu jenis insektisida.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

        with st.expander("📒 Sumber Referensi"):
            st.markdown("""

    <div style="font-family: 'Segoe UI', sans-serif; font-size: 16px;">
        <a class="ref-link" href="repository.polinela.ac.id"  target="_blank"><strong>repository.polinela.ac.id</strong>: Pengendalian Plutella xylostella</a>
        <a class="ref-link" href="journal.univetbantara.ac.id"  target="_blank"><strong>journal.univetbantara.ac.id</strong>: Pengendalian Hama Bunga Kol</a>
        <a class="ref-link" href="media.neliti.com"  target="_blank"><strong>media.neliti.com</strong>: Pengendalian Plutella xylostella Dengan Ekstrak Alami</a>
        <a class="ref-link" href="savana-cendana.id"  target="_blank"><strong>savana-cendana.i</strong>: Pengendalian Biologis Hama</a>
        <a class="ref-link" href="jurnal.um-tapsel.ac.id"  target="_blank"><strong>jurnal.um-tapsel.ac.id</strong>: Kajian Budidaya Sayuran Dan Pengendalian Hama</a>
        <a class="ref-link" href="jurnalfkip.unram.ac.id"  target="_blank"><strong>jurnalfkip.unram.ac.id</strong>: Penggunaan Ekstrak Tanaman Untuk Pengendalian Hama</a>
    </div>
    """, unsafe_allow_html=True)


def halaman_panduan():
    st.markdown("<div class='custom-title'>📖 Panduan Pengguna</div>", unsafe_allow_html=True)
    st.info("Berikut panduan langkah demi langkah cara menggunakan fitur deteksi hama pada aplikasi ini.")
    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/cauli-desktop.png?updatedAt=1749792657775"
                         alt="Aphid pada bunga kol"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Banner Utama
</figcaption>
                            
    """, unsafe_allow_html=True)
                
    # LANGKAH 1
    st.markdown("""
    <div class="langkah-card">
        <div class="langkah-number">1. Pilih Menu Deteksi Hama</div>
        <div class="langkah-desc">
            Langkah pertama, pililah menu "deteksi hama" disamping menu sidebar. Seperti pada instruksi gambar dibawah ini:
    </div>
    """, unsafe_allow_html=True)
    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/1.jpg?updatedAt=1751202710695"
                         alt="Banner utama"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Halaman Beranda
</figcaption>
                            
    """, unsafe_allow_html=True)

    # LANGKAH 2
    st.markdown("""
    <div class="langkah-card">
        <div class="langkah-number">2. Halaman Deteksi Hama</div>
        <div class="langkah-desc">
            Sebelum memulai melakukan deteksi gambar hama, kita pastikan terlebih dahulu bahwa terdapat keterangan status model berhasil terhubung. Hal ini penting
            untuk diperhatikan karena jika status model tidak terhubung maka tidak bisa melanjutkan pada tahap proses deteksi gambar hama. Oh iya kamu juga bisa memerhatikan 
            spesifikasi gambar yang akan diupload dan contoh gambar yang baik agar bisa di identifikasi oleh model. Berikut tampilan dibawah ini:
    </div>
    """, unsafe_allow_html=True)
    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/4574CA73-1CAB-4BF7-9E20-2F6208E5AA10.jpeg?updatedAt=1751202754320"
                         alt="halaman aplikasi"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
                    <img src="https://ik.imagekit.io/mastah/1F992F9F-035C-49B0-95D3-1AAD0BE13030.jpeg?updatedAt=1751202754368"
                         alt="spesifikasi gambar"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>         
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Halaman Aplikasi
</figcaption>
                            
    """, unsafe_allow_html=True)

    # LANGKAH 3
    st.markdown("""
    <div class="langkah-card">
        <div class="langkah-number">3. Melakukan Proses Deteksi</div>
        <div class="langkah-desc">
            Langkah berikutnya pada bagian "upload gambarmu disini" , kita klik browse file kemudian masukkan gambar hama yang ingin di deteksi. Setelah itu klik tombol “🔍 Deteksi Gambar” untuk memulai proses analisis. 
            Dan sistem model akan mengidentifikasi gambar dan memberikan hasil deteksi hama secara real-time. seperti gambar dibawah ini:
    </div>
    """, unsafe_allow_html=True)
    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/2.jpg?updatedAt=1751202710658"
                         alt="masukkan gambar"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
                    <img src="https://ik.imagekit.io/mastah/3.jpg?updatedAt=1751202710628"
                         alt="tombol deteksi"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>         
                    
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Proses Deteksi
</figcaption>
                            
    """, unsafe_allow_html=True)
                
    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/4.jpg?updatedAt=1751202710657"
                         alt="hasil deteksi gambar"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Hasil Deteksi
</figcaption>
                            
    """, unsafe_allow_html=True)

    # LANGKAH 4
    st.markdown("""
    <div class="langkah-card">
        <div class="langkah-number">4. Lihat Riwayat Deteksi</div>
        <div class="langkah-desc">
            Semua hasil deteksi otomatis tersimpan di database dan bisa dilihat kembali melalui menu "Riwayat".
            Kamu juga bisa menghapus riwayat jika dibutuhkan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
                st.markdown("""
<div class="langkah-card" style="
            background-color: #e7f1d3;
            padding: 10px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 40px;
            font-family: 'Montserrat', sans-serif;
            ">
<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 24px;">
<div style="flex: 1 1 350px;">
                    <img src="https://ik.imagekit.io/mastah/5.jpg?updatedAt=1751202709386"
                         alt="hasil riwayat deteksi"
                         style="width: 100%; height: 470px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>
</div>         
<figcaption style="text-align: center; font-style:"Bodoni", serif; margin-top: 10px; color: #555;font-size: 14px;">
        Gambar Hasil Riwayat Deteksi
</figcaption>
                            
    """, unsafe_allow_html=True)
    

    # PENUTUP
    st.markdown("""
    <div class="langkah-card" style="background-color:#e8f5e9; border-left: 6px solid #66bb6a;">
        <div class="langkah-number">🎉 Selamat Mencoba!</div>
        <div class="langkah-desc">
            Jika kamu sudah mencoba semua fitur, silakan eksplorasi submenu lain seperti Riwayat, Profil Hama, dan Statistik.
        </div>
    </div>
    """, unsafe_allow_html=True)
    

# --- KONEKSI KE MONGODB ---
def connect_mongo():
    try:
        # Ambil dari secrets.toml
        mongo_uri = st.secrets["mongo_uri"]
        mongo_db = st.secrets["mongo_db"]
        mongo_collection = st.secrets["mongo_collection"]
    except:
        # Jika tidak ada secrets.toml, baca dari file
        secrets = toml.load(".streamlit/secrets.toml")
        mongo_uri = secrets["mongo_uri"]
        mongo_db = secrets["mongo_db"]
        mongo_collection = secrets["mongo_collection"]

    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]
    return collection

def halaman_aplikasi():
    st.markdown("<div class='custom-title'>🐞 Aplikasi Deteksi Hama Bunga Kol</div>", unsafe_allow_html=True)
    st.info("Halaman ini merupakan fitur utama untuk mengunggah gambar dan mendapatkan hasil deteksi.")
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    with st.expander("📦 Status Model", expanded=True):
        model_path = Path(settings.DETECTION_MODEL)
        st.write(f"Debug: Mencoba memuat model dari: {model_path}")
        st.write(f"Debug: Direktori kerja saat ini: {os.getcwd()}")
        st.write(f"Debug: Apakah file model ada? {model_path.exists()}")
        if not model_path.exists():
            st.error(f"File model tidak ditemukan di: {model_path}")
            st.error("Pastikan file 'best6.pt' ada di direktori 'brassica/weights/' di repositori.")
            return
        try:
            model = helper.load_model(model_path)
            st.success("Model berhasil terhubung ")
            gif_path = Path("assets/image/ceklist.gif")
            if not gif_path.exists():
                st.warning(f"File GIF tidak ditemukan di: {gif_path}")
            else:
                file_ = open(gif_path, "rb")
                contents = file_.read()
                data_url = base64.b64encode(contents).decode("utf-8")
                file_.close()

                st.markdown(f"""
                    <div style='
                    display: flex;
                    margin-top: -82px;
                    margin-left: 170px;
                    '>
                <div style='text-align: center;'>
                <img src="data:image/gif;base64,{data_url}" width="80">
                </div>
                </div>
                """,
                unsafe_allow_html=True)
        except Exception as ex:
            st.error(f"Gagal memuat model dari: {model_path}")
            st.error(f"Detail error: {str(ex)}")
            return

    st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">📝 Instruksi Deteksi</h3>", unsafe_allow_html=True)
    st.markdown("""
        1. Sebelum memulai melakukan deteksi hama pada gambar, pastikan koneksi **status model** berhasil terhubung.
        2. Berikutnya silahkan **Unggah gambar** hama dalam format **`.jpg`, `.jpeg`, `.png`, atau `.webp`**.
        3. Apabila gambar berhasil di unggah maka akan muncul pada **preview gambar**.
        5. Klik tombol **🔍 Deteksi Gambar** untuk memulai proses pendeteksian hama.
        6. Jika berhasil, hasil deteksi akan ditampilkan pada bagian **hasil deteksi gambar**.
        7. Hasil langsung tersimpan, bisa ditinjau ulang melalui menu **Riwayat**.
    """)

    uploaded_file = None
    uploaded_image = None
    result_img = None

    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        with st.expander("🌌 Spesifikasi Gambar", expanded=False):
            st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">🌌 Spesifikasi Gambar</h3>", unsafe_allow_html=True)
            st.markdown("""
                1. Gambar dalam format **`.jpg`, `.jpeg`, `.png`, atau `.webp`**.
                2. Resolusi minimal gambar yang diunggah **`400×400`** piksel.
                3. Pastikan gambar **tidak buram (blur), tidak gelap, dan tidak terlalu terang**.
                4. Ambil gambar dari **jarak sedang-dekat** agar hama terlihat jelas.
            """)

    with col2:
        with st.expander("📸 Contoh Gambar Yang Sesuai", expanded=False):
            st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">📸 Contoh Gambar Yang Sesuai</h3>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.image(HOME8_IMAGE, caption="Gambar Kualitas Kurang Baik", width=200)
            with col_b:
                st.image(HOME9_IMAGE, caption="Gambar Kualitas Sangat Baik", width=200)

    st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">📤 Upload Gambarmu Disini</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Silakan unggah gambar Anda, sesuai dengan format instruksi", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file:
        uploaded_image = PIL.Image.open(uploaded_file)

    if uploaded_file and st.button("🔍 Deteksi Gambar"):
        try:
            result = model.predict(uploaded_image)
            result_img = result[0].plot()[:, :, ::-1]

            # Simpan gambar hasil deteksi sebagai base64
            buf = io.BytesIO()
            PIL.Image.fromarray(result_img).save(buf, format="PNG")
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

            # Mapping class ID ke nama hama
            CLASS_NAMES = {
                0: "Agrotis ipsilon",
                1: "Aphid",
                2: "Plutella xylostella",
                3: "Spodoptera litura"
            }

            detection_data = []
            for box in result[0].boxes:
                class_id = int(box.cls.item())  # Ambil class ID
                confidence = float(box.conf.item())  # Ambil confidence
                class_name = CLASS_NAMES.get(class_id, f"Hama Tidak Dikenal ({class_id})")
                detection_data.append(f"{class_name} (akurasi: {confidence:.2f})")

            # Simpan ke MongoDB
            collection = connect_mongo()
            detection_record = {
                "image_name": f"processed_{uploaded_file.name}",
                "detection_data": detection_data,
                "detection_time": datetime.utcnow(),
                "image_base64": image_base64
            }
            collection.insert_one(detection_record)

            st.session_state.result_img = result_img
            st.success("✅ Hasil deteksi berhasil disimpan di riwayat.")

        except Exception as ex:
            st.error("❌ Terjadi kesalahan saat deteksi.")
            st.error(ex)

    elif not uploaded_file:
        st.session_state.result_img = None
    else:
        st.session_state.result_img = None

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">🌄 Preview Gambar</h3>", unsafe_allow_html=True)
        if uploaded_file:
            st.image(uploaded_file, caption="Gambar yang Diunggah", use_container_width=True)
        else:
            st.info("Upload gambar dulu ya, baru lanjut!")

    with col_right:
        st.markdown("<h3 style=\"margin-top: 0; font-family: 'Bodoni', serif;\">🎯 Hasil Deteksi Gambar</h3>", unsafe_allow_html=True)
        if uploaded_file and st.session_state.result_img is None:
            st.info("Klik tombol '🔍 Deteksi Gambar' untuk melihat hasil.")
        elif st.session_state.result_img is not None:
            st.image(st.session_state.result_img, caption="Hasil Deteksi", use_container_width=True)


def halaman_riwayat():
    st.markdown("<div class='custom-title'>⏳ Riwayat Deteksi</div>", unsafe_allow_html=True)
    
    try:
        collection = connect_mongo()
        
        # Debug: cek apakah koneksi berhasil
        if collection is None:
            st.error("❌ Koneksi ke MongoDB gagal. Pastikan konfigurasi benar.")
            return

        results = collection.find().sort("detection_time", -1)
        local_tz = pytz.timezone("Asia/Jakarta")
        CLASS_NAMES = {
            0: "Agrotis ipsilon",
            1: "Aphid",
            2: "Plutella xylostella",
            3: "Spodoptera litura"
        }

        if not results or collection.count_documents({}) == 0:
            st.info("Belum ada hasil deteksi yang tersimpan.")
        else:
            for idx, record in enumerate(results):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown("### 📝 Info Deteksi")
                        st.markdown(f"**Nama Gambar:** {record.get('image_name', 'Tidak tersedia')}")

                        detection_time_utc = record.get('detection_time')
                        if detection_time_utc:
                            time_local = detection_time_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
                            st.markdown(f"**Waktu Deteksi:** {time_local.strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            st.markdown("**Waktu Deteksi:** Tidak tersedia")

                        st.markdown("**Hasil Deteksi:**")

                        formatted_result = []

                        for item in record.get('detection_data', []):
                            if isinstance(item, str):
                                formatted_result.append(item)
                            elif isinstance(item, list) or isinstance(item, tuple):
                                try:
                                    class_id = int(float(item[-1]))
                                    confidence = float(item[-2])
                                    nama_hama = CLASS_NAMES.get(class_id, f"Hama Tidak Dikenal (ID {class_id})")
                                    formatted_result.append(f"{nama_hama} (akurasi: {confidence:.2f})")
                                except Exception:
                                    formatted_result.append("Format data tidak dikenali")
                            else:
                                formatted_result.append("Data tidak valid")

                        if formatted_result:
                            st.markdown(", ".join(formatted_result))
                        else:
                            st.markdown("_Tidak ada hasil deteksi._")

                        if 'image_base64' in record:
                            st.image(
                                f"data:image/png;base64,{record['image_base64']}",
                                caption="Gambar Hasil Deteksi",
                                use_container_width=True
                            )
                        else:
                            st.warning("Tidak ada gambar hasil deteksi.")

                    with col2:
                        if st.button("🗑️ Hapus", key=f"hapus_{idx}_{record.get('_id', 'unknown')}"):
                            try:
                                collection.delete_one({"_id": record["_id"]})
                                st.success("Hasil deteksi dihapus.")
                                st.rerun()  # <-- Digunakan yang terbaru
                            except Exception as del_ex:
                                st.error("❌ Gagal menghapus dokumen.")
                                st.error(str(del_ex))

                    st.markdown("---")
    
    except Exception as e:
        st.error("❌ Gagal mengambil data dari MongoDB.")
        st.error(str(e))


def footer():
    st.markdown("""
    <div class="footer">
        <h6 style=\"margin-top: 0; font-family: 'Bodoni', serif;color:#3f3a3a;\">Brassica membantu mengenali hama bunga kol © 2025</h6>
    </div>
    """, unsafe_allow_html=True)


# --- Main App ---
def main():
    load_css("assets/css/style.css")
    selected_page = header()
    # Menentukan halaman yang akan ditampilkan
    if selected_page == "Beranda":
        halaman_utama()
        footer()
    elif selected_page == "Profil Hama":
        halaman_profil_hama()
    elif selected_page == "Panduan":
        halaman_panduan()
    elif selected_page == "Deteksi Hama":
        halaman_aplikasi()
    elif selected_page == "Riwayat":
        halaman_riwayat()

if __name__ == "__main__":
        main()
