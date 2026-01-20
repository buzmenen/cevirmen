import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- TASARIM VE ÖLÇEKLENDİRME (CSS) ---
arka_plan_resmi = "https://i.hizliresim.com/tbkwdlu.jpg"

st.markdown(
    f"""
    <style>
    /* Ölçeği %90 yaparak biraz daha büyütüyoruz */
    html, body, [data-testid="stAppViewContainer"] {{
        zoom: 0.9; 
        -moz-transform: scale(0.9);
        -moz-transform-origin: 0 0;
    }}

    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    
    /* Ana kutuyu biraz daha genişleterek ferahlatıyoruz (900px yaptık) */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.88); 
        padding: 3rem;
        border-radius: 25px;
        max-width: 900px; 
        margin: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}

    /* Yazıları orta boy ve net hale getirdik */
    h1 {{ font-size: 2.4rem !important; color: #1e272e !important; text-align: center; }}
    h3 {{ font-size: 1.4rem !important; color: #1e272e !important; }}
    p, span, label {{ 
        color: #1e272e !important; 
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }}

    /* Giriş kutusunu belirginleştirdik */
    .stTextInput input {{
        font-size: 1.1rem !important;
        padding: 12px !important;
        border-radius: 12px !important;
    }}

    /* Buton boyutlarını ideal seviyeye çektik */
    .stButton>button {{
        font-size: 1rem !important;
        padding: 8px 25px !important;
        border-radius: 12px;
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

st.write("### 📂 Eski Listeni Güncelle")
yuklenen_dosya = st.file_uploader("Önceki Excel dosyanı seç:", type=['xlsx'])
if yuklenen_dosya is not None:
    if st.button("Dahil Et"):
        eski_df = pd.read_excel(yuklenen_dosya)
        st.session_state.kelimeler = eski_df.to_dict('records')
        st.success("Liste başarıyla aktarıldı!")

st.divider()

# Dil Değiştirme Paneli
kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col1, col2, col3 = st.columns([2,1,2])
with col1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col3: st.write(f"**Hedef:** {hedef_etiket}")

st.text_input(f"{kaynak_etiket} bir kelime yazın:", key="yeni_kelime", on_change=kelime_ekle)

if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.write("### 📚 Kelimelerim")
    st.dataframe(df, use_container_width=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Güncel Excel İndir", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Listeyi Temizle"):
            st.session_state.kelimeler = []
            st.rerun()
