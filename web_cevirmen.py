import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- TASARIM VE ARKA PLAN ---
arka_plan_resmi = "https://i.hizliresim.com/tbkwdlu.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    
    /* ANA BAŞLIK */
    h1 {{
        color: #1e272e !important;
        text-shadow: 2px 2px 10px rgba(255, 255, 255, 1), 
                     -2px -2px 10px rgba(255, 255, 255, 1),
                     0px 0px 20px rgba(255, 255, 255, 0.8) !important;
        font-weight: 900 !important;
        text-align: center !important;
    }}

    /* Genel Yazı Renkleri */
    h2, h3, p, span, label, .stMarkdown p {{
        color: #1e272e !important; 
        font-weight: bold !important;
    }}

    /* PANELLER VE GİRİŞ KUTUSU */
    .stMarkdown div[data-testid="stMarkdownContainer"] p, .stAlert {{
        background-color: rgba(255, 255, 255, 0.7);
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    .stTextInput input {{
        color: black !important;
        background-color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }}

    /* DOSYA YÜKLEME ALANI BEYAZLATMA */
    [data-testid="stFileUploader"] {{
        background-color: white !important;
        padding: 10px;
        border-radius: 15px;
        border: 2px dashed #3498db !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background-color: white !important;
        color: black !important;
    }}

    [data-testid="stFileUploader"] button {{
        color: #1e272e !important;
        background-color: #f1f2f6 !important;
        font-weight: bold !important;
        transition: all 0.3s ease; /* Yumuşak geçiş için */
    }}
    
    [data-testid="stFileUploader"] button:hover {{
        background-color: #ffffff !important;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(52, 152, 219, 0.5);
    }}

    /* TABLO */
    [data-testid="stTable"] {{ background-color: white !important; border-radius: 15px !important; }}
    [data-testid="stTable"] td, [data-testid="stTable"] th {{ color: black !important; background-color: white !important; }}
    
    /* --- PARLAYAN BUTON EFEKTLERİ --- */
    .stButton>button, .stDownloadButton>button {{
        color: white !important;
        background-color: #3498db !important;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease !important; /* Efektin hızı */
    }}

    /* Fare üzerine gelince (Hover) */
    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: #2980b9 !important; /* Rengi biraz koyulaşır */
        transform: translateY(-3px) scale(1.02); /* Hafif yukarı kalkar ve büyür */
        box-shadow: 0px 10px 20px rgba(52, 152, 219, 0.6) !important; /* Parlama efekti */
        cursor: pointer;
    }}

    /* Butona basılınca (Active) */
    .stButton>button:active, .stDownloadButton>button:active {{
        transform: translateY(1px);
        box-shadow: 0px 5px 10px rgba(52, 152, 219, 0.4) !important;
    }}
    
    /* Öpücük Butonuna Özel Pembe Parlama */
    div.stButton > button:first-child:contains("💋") {{
       /* Bu kısım özel seçici gerektirebilir, aşağıda butonun kendisine direkt ekledik */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- PROGRAM MANTIĞI ---
if 'kelimeler' not in st.session_state:
    st.session_state.kelimeler = []
if 'kaynak_dil' not in st.session_state:
    st.session_state.kaynak_dil = 'en'
if 'hedef_dil' not in st.session_state:
    st.session_state.hedef_dil = 'tr'

def dil_degistir():
    st.session_state.kaynak_dil, st.session_state.hedef_dil = st.session_state.hedef_dil, st.session_state.kaynak_dil

def kelime_ekle():
    giris = st.session_state.yeni_kelime.strip()
    if giris:
        translator = GoogleTranslator(source=st.session_state.kaynak_dil, target=st.session_state.hedef_dil)
        try:
            ceviri = translator.translate(giris)
            if st.session_state.kaynak_dil == 'en':
                ing, tr = giris, ceviri
            else:
                ing, tr = ceviri, giris
            st.session_state.kelimeler.append({"İngilizce": ing, "Türkçe": tr})
        except:
            st.error("Bağlantı hatası.")
    st.session_state.yeni_kelime = ""

# --- ARAYÜZ ---
st.title("📝 Karıcığımın Dil Asistanı")

st.info("""
Merhaba karıcığım bu senin için yaptığım dil asistanın. İstediğin kelimeyi çevirebilir, listeni Excel olarak indirebilir ve aşağıdan istediğin YouTube şarkısını açabilirsin!

Seni seviyorum <3
""")

# --- MÜZİK KUTUSU ---
st.write("### 🎬 Müzik Kutusu")
video_linki = st.text_input("Dinlemek istediğin YouTube linkini buraya yapıştır:", 
                            placeholder="https://www.youtube.com/watch?v=...")

if video_linki:
    st.video(video_linki)
else:
    st.video("https://www.youtube.com/watch?v=7qaHdHpSjX8")

st.write("### 📂 Eski Listeni Güncelle")
yuklenen_dosya = st.file_uploader("Dosyanı buraya bırak:", type=['xlsx'])
if yuklenen_dosya is not None:
    try:
        eski_df = pd.read_excel(yuklenen_dosya)
        if st.button("Listeye Dahil Et"):
            st.session_state.kelimeler = eski_df.to_dict('records')
            st.success("Eski liste yüklendi!")
    except:
        st.error("Excel okunamadı.")

st.divider()

# Kelime Çeviri Bölümü
kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col_dil1, col_dil2, col_dil3 = st.columns([2,1,2])
with col_dil1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col_dil2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col_dil3: st.write(f"**Hedef:** {hedef_etiket}")

st.text_input(f"{kaynak_etiket} bir kelime yazın:", key="yeni_kelime", on_change=kelime_ekle)

if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.write("### 📚 Karıcığımın Kelimeleri")
    st.table(df) 

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Bana Tıkla ve Excel İndir Bebek", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Bana Tıkla ve Sıfırla Güzelim"):
            st.session_state.kelimeler = []
            st.rerun()

# --- ÖPÜCÜK KUTUSU ---
st.divider()
st.write("### 💖 Kocandan Bir Sürpriz")
if st.button("💋 Beni Öp"):
    st.balloons() 
    st.success("Bende seni öptüm aşkım 💋😘")

