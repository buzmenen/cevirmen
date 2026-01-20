import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝", layout="wide") # Layout wide yaparak alanı genişlettik

# --- TASARIM VE ARKA PLAN ---
arka_plan_resmi = "https://i.hizliresim.com/tbkwdlu.jpg"

st.markdown(
    f"""
    <style>
    /* Arka Plan */
    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}

    /* TÜM İÇERİĞİ SOLA YASLAMA */
    .block-container {{
        margin-left: 0 !important;
        padding-left: 2rem !important;
        max-width: 800px !important; /* Çok yayılmaması için genişliği sınırladık */
    }}
    
    /* ANA BAŞLIK - Sola Yaslı ve Belirgin */
    h1 {{
        color: #1e272e !important;
        text-shadow: 2px 2px 10px rgba(255, 255, 255, 1), 
                     -2px -2px 10px rgba(255, 255, 255, 1) !important;
        font-weight: 900 !important;
        text-align: left !important; /* Sola yasladık */
        padding-bottom: 10px;
    }}

    /* Genel Yazı Renkleri */
    h2, h3, p, span, label, .stMarkdown p {{
        color: #1e272e !important; 
        font-weight: bold !important;
        text-align: left !important;
    }}

    /* --- PANELLER (CAM EFEKTİ) --- */
    .stAlert, [data-testid="stHorizontalBlock"], .stTextInput {{
        background-color: rgba(255, 255, 255, 0.7) !important;
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}

    /* --- DOSYA YÜKLEME ALANI --- */
    [data-testid="stFileUploader"] {{
        background-color: white !important;
        padding: 10px;
        border-radius: 15px;
        border: 2px dashed #3498db !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background-color: white !important;
    }}

    /* --- TABLO (LİSTE) BEYAZ VE SİYAH YAZILI --- */
    [data-testid="stTable"] {{
        background-color: white !important;
        border-radius: 15px !important;
        border: 1px solid #ddd !important;
    }}

    [data-testid="stTable"] td, [data-testid="stTable"] th {{
        background-color: white !important;
        color: black !important;
    }}

    /* --- BUTONLAR --- */
    .stButton>button, .stDownloadButton>button {{
        color: white !important;
        background-color: #3498db !important;
        border-radius: 12px;
        font-weight: bold;
        border: none;
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
Merhaba karıcığım bu senin için yaptığım dil asistanın. Artık zorlanmadan istediğin gibi Türkçeden İngilizce hatta İngilizceden Türkçeye çeviri bile yapabilirsin. 

Ama unutma eğer yazdığın kelimenin karşılığı olmazsa tabloya aynen o kelime tekrar yazılır. Lütfen buna dikkat et. 

Seni seviyorum, iyi çalışmalar <3
""")

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
    st.table(df) 

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Excel İndir", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Sıfırla"):
            st.session_state.kelimeler = []
            st.rerun()
