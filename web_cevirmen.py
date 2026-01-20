import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO
import time

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
    
    h1 {{
        color: #1e272e !important;
        text-shadow: 2px 2px 10px rgba(255, 255, 255, 1) !important;
        font-weight: 900 !important;
        text-align: center !important;
    }}

    h2, h3, p, span, label, .stMarkdown p {{
        color: #1e272e !important; 
        font-weight: bold !important;
    }}

    /* --- DOSYA YÜKLEME ALANI TAM DÜZELTME --- */
    [data-testid="stFileUploader"] {{
        background-color: white !important;
        padding: 15px !important;
        border-radius: 15px !important;
        border: 2px dashed #3498db !important;
    }}

    /* Sürükleme alanı içindeki genel yazılar */
    [data-testid="stFileUploaderDropzoneInstructions"] div,
    [data-testid="stFileUploaderDropzoneInstructions"] span {{
        color: black !important;
        font-weight: bold !important;
    }}

    /* BROWSE FILES BUTONU VE İÇİNDEKİ YAZI */
    [data-testid="stFileUploader"] button {{
        background-color: #f1f2f6 !important;
        border: 1px solid #ccc !important;
        color: black !important; /* Yazı rengini siyah yap */
    }}
    
    /* Butonun içindeki metne direkt müdahale */
    [data-testid="stFileUploader"] button div p {{
        color: black !important;
        font-weight: bold !important;
    }}

    /* YÜKLENEN DOSYA İSMİ VE DETAYLAR */
    [data-testid="stFileUploaderFileData"] div, 
    [data-testid="stFileUploaderFileData"] span,
    [data-testid="stFileUploaderFileName"],
    .st-emotion-cache-1erivf3 {{ 
        color: black !important;
        font-weight: bold !important;
    }}

    /* Dosya silme (X) butonu rengi */
    [data-testid="stFileUploaderFileData"] button {{
        color: black !important;
    }}

    /* Giriş kutusu (Input) siyahlığı engelleme */
    .stTextInput input {{
        color: black !important;
        background-color: white !important;
        font-weight: bold !important;
    }}

    /* --- BUTONLAR --- */
    .stButton>button, .stDownloadButton>button {{
        color: white !important;
        background-color: #3498db !important;
        border-radius: 12px;
        font-weight: bold;
        transition: all 0.3s ease !important;
    }}

    .stButton>button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0px 10px 20px rgba(52, 152, 219, 0.6) !important;
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
if 'yuklenen_dosya_adi' not in st.session_state:
    st.session_state.yuklenen_dosya_adi = None

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

st.info("Seni seviyorum karıcığım, iyi çalışmalar! <3")

st.write("### 🎬 Müzik Kutusu")
video_linki = st.text_input("Şarkı linkini buraya at atgum:", placeholder="https://www.youtube.com/watch?v=...")
st.video(video_linki if video_linki else "https://www.youtube.com/watch?v=7qaHdHpSjX8")

st.write("### 📂 Eski Listeni Güncelleyebilirsin Bebeğim")
yuklenen_dosya = st.file_uploader("Dosyanı buraya bırak ben alırım atgum:", type=['xlsx'])

dosya_mesaj_alani = st.empty()

if yuklenen_dosya is not None:
    if st.button("Listeye Dahil Et"):
        if st.session_state.yuklenen_dosya_adi == yuklenen_dosya.name:
            dosya_mesaj_alani.warning("Karıcığımmm zaten dahil ettin bunu 🤭")
            time.sleep(4)
            dosya_mesaj_alani.empty()
        else:
            try:
                eski_df = pd.read_excel(yuklenen_dosya)
                st.session_state.kelimeler = eski_df.to_dict('records')
                st.session_state.yuklenen_dosya_adi = yuklenen_dosya.name
                dosya_mesaj_alani.success("Eski liste yüklendi aferin karıcığım! ✅")
                time.sleep(5)
                dosya_mesaj_alani.empty()
            except:
                dosya_mesaj_alani.error("Excel okunamadı atgum.")
                time.sleep(3)
                dosya_mesaj_alani.empty()

st.divider()

kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col1, col2, col3 = st.columns([2,1,2])
with col1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col3: st.write(f"**Hedef:** {hedef_etiket}")

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
            st.session_state.yuklenen_dosya_adi = None
            st.rerun()

st.divider()
st.write("### 💖 Kocandan Bir Sürpriz")
opucuk_mesaj_alani = st.empty()

if st.button("💋 Beni Öp"):
    st.balloons()
    opucuk_mesaj_alani.success("Bende seni öptüm aşkım 💋😘")
    time.sleep(5)
    opucuk_mesaj_alani.empty()
