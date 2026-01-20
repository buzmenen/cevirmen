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

    /* --- DOSYA YÜKLEME ALANI (UPLOADER) DÜZENLEME --- */
    /* Dış kutuyu beyaz yapıyoruz */
    [data-testid="stFileUploader"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 15px;
        border-radius: 15px;
        border: 2px dashed #3498db !important;
    }}
    
    /* "Drag and drop file here" ve "Limit 200MB" gibi tüm iç yazıları SİYAH yapıyoruz */
    [data-testid="stFileUploader"] section {{
        color: black !important;
    }}
    
    [data-testid="stFileUploader"] label {{
        color: black !important;
    }}

    [data-testid="stFileUploader"] small {{
        color: #2c3e50 !important;
        font-weight: bold !important;
    }}
    /* ----------------------------------------------- */

    .stTextInput input {{
        color: black !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        font-weight: bold;
    }}

    .stButton>button {{
        color: white !important;
        background-color: #3498db !important;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }}
    
    .stDataFrame div {{
        color: black !important;
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

# --- FONKSİYONLAR ---
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
            st.error("Bağlantı hatası oluştu.")
    st.session_state.yeni_kelime = ""

# --- ARAYÜZ ---
st.title("📝 Karıcığımın Dil Asistanı")

st.write("### 📂 Eski Listeni Güncelle")
# Dosya yükleme alanı artık beyaz ve yazıları siyah
yuklenen_dosya = st.file_uploader("Daha önce indirdiğin Excel dosyasını buraya bırak:", type=['xlsx'])
if yuklenen_dosya is not None:
    try:
        eski_df = pd.read_excel(yuklenen_dosya)
        if st.button("Listeye Dahil Et"):
            st.session_state.kelimeler = eski_df.to_dict('records')
            st.success("Eski liste yüklendi!")
    except:
        st.error("Excel dosyası okunamadı.")

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
        st.download_button("📥 Excel Olarak İndir", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Listeyi Sıfırla"):
            st.session_state.kelimeler = []
            st.rerun()
