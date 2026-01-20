import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- TASARIM VE OKUNABİLİRLİK AYARI (CSS) ---
arka_plan_resmi = "https://i.hizliresim.com/tbkwdlu.jpg"

st.markdown(
    f"""
    <style>
    /* Ölçek ayarı */
    html, body, [data-testid="stAppViewContainer"] {{
        zoom: 0.95; 
        -moz-transform: scale(0.95);
        -moz-transform-origin: 0 0;
    }}

    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    
    /* ANA PANEL: Opaklığı artırarak arkadaki resmin yazıları boğmasını engelledik */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.94); /* Daha az şeffaf, daha okunaklı */
        padding: 3rem;
        border-radius: 30px;
        max-width: 850px; 
        margin: auto;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}

    /* BAŞLIKLAR: Çok daha keskin ve gölgeli hale getirildi */
    h1 {{ 
        font-size: 2.6rem !important; 
        color: #111111 !important; 
        text-align: center;
        text-shadow: 2px 2px 4px rgba(255,255,255,1); /* Beyaz parlama ile öne çıkardık */
        margin-bottom: 20px !important;
    }}
    
    h3 {{ 
        font-size: 1.5rem !important; 
        color: #1e272e !important; 
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }}

    /* METİNLER VE ETİKETLER: Kalın ve koyu renk */
    p, span, label, .stMarkdown p {{ 
        color: #000000 !important; 
        font-size: 1.15rem !important;
        font-weight: 800 !important; /* Ekstra kalın yapıldı */
    }}

    /* GİRİŞ KUTUSU: İçindeki yazı tam siyah */
    .stTextInput input {{
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #1e272e !important;
        font-weight: 600 !important;
    }}

    /* BUTONLAR: Belirgin renkler */
    .stButton>button {{
        color: white !important;
        background-color: #2c3e50 !important;
        border-radius: 15px;
        font-weight: bold;
        border: 2px solid #1e272e;
    }}
    
    /* Tablo verileri */
    [data-testid="stTable"] td {{
        color: #000000 !important;
        font-weight: 500;
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
            st.error("Çeviri hatası!")
    st.session_state.yeni_kelime = ""

# --- ARAYÜZ ---
st.title("📝 Karıcığımın Dil Asistanı")

st.write("### 📂 Eski Listeni Güncelle")
yuklenen_dosya = st.file_uploader("Excel dosyasını buraya sürükle:", type=['xlsx'])
if yuklenen_dosya is not None:
    if st.button("Listeye Ekle"):
        eski_df = pd.read_excel(yuklenen_dosya)
        st.session_state.kelimeler = eski_df.to_dict('records')
        st.success("Veriler başarıyla çekildi!")

st.divider()

# Dil Seçimi
kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col1, col2, col3 = st.columns([2,1,2])
with col1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col2: st.button("🔄 Yer Değiştir", on_click=dil_degistir)
with col3: st.write(f"**Target:** {hedef_etiket}")

st.text_input(f"{kaynak_etiket} kelimeyi yaz ve Enter'a bas:", key="yeni_kelime", on_change=kelime_ekle)

if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.write("### 📚 Kaydedilen Kelimeler")
    st.table(df) # Daha net bir görünüm için dataframe yerine table kullandık

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Excel Olarak Kaydet", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Listeyi Sıfırla"):
            st.session_state.kelimeler = []
            st.rerun()
