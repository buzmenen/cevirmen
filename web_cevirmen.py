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
    
    /* Genel Yazı Renkleri */
    h1, h2, h3, p, span, label, .stMarkdown p {{
        color: #1e272e !important; 
        font-weight: bold !important;
    }}

    /* --- TÜM PANELLERİ ŞEFFAF BEYAZ YAPMA (Liste ve Butonlar Dahil) --- */
    /* Orta bölümdeki tüm ana blokları hedefler */
    [data-testid="stVerticalBlock"] > div {{
        background-color: rgba(255, 255, 255, 0.65); /* Hafif saydam beyaz */
        padding: 10px 20px;
        border-radius: 20px;
        margin-bottom: 10px;
        backdrop-filter: blur(8px); /* Cam efekti */
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* --- DOSYA YÜKLEME ALANI --- */
    [data-testid="stFileUploader"] {{
        background-color: white !important;
        padding: 10px;
        border-radius: 15px;
    }}

    [data-testid="stFileUploader"] section {{
        background-color: white !important;
        color: black !important;
    }}

    [data-testid="stFileUploaderDropzoneInstructions"] div {{
        color: black !important;
    }}
    
    [data-testid="stFileUploader"] button {{
        color: white !important;
        background-color: #2c3e50 !important;
    }}

    /* --- GİRİŞ KUTUSU --- */
    .stTextInput input {{
        color: black !important;
        background-color: white !important;
        font-weight: bold;
    }}

    /* --- TABLO (LİSTE) DÜZENLEME --- */
    /* Tablonun siyah kalmasını engellemek için */
    [data-testid="stDataFrame"] {{
        background-color: white !important;
        border-radius: 10px;
    }}
    
    /* Tablo içindeki yazıların siyah olması */
    [data-testid="stTable"] td, [data-testid="stTable"] th {{
        color: black !important;
    }}

    /* --- BUTONLARIN HEPSİNİ MAVİ YAPMA --- */
    .stButton>button, .stDownloadButton>button {{
        color: white !important;
        background-color: #3498db !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
        padding: 10px;
    }}

    .stButton>button:hover, .stDownloadButton>button:hover {{
        background-color: #2980b9 !important;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
)

# --- HAFIZA YÖNETİMİ ---
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

kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col_dil1, col_dil2, col_dil3 = st.columns([2,1,2])
with col_dil1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col_dil2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col_dil3: st.write(f"**Hedef:** {hedef_etiket}")

st.text_input(f"{kaynak_etiket} bir kelime yazın:", key="yeni_kelime", on_change=kelime_ekle)

if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.write("### 📚 Kaydedilen Kelimeler")
    st.dataframe(df, use_container_width=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        # İndirme butonu artık mavi
        st.download_button("📥 Excel İndir", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        # Sıfırla butonu da mavi
        if st.button("🗑️ Sıfırla"):
            st.session_state.kelimeler = []
            st.rerun()
