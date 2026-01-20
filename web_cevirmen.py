import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- TASARIM VE ARKA PLAN ---
arka_plan_resmi = "https://i.hizliresim.com/j0r8m0l.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.7); /* Koyu tema daha şık durur */
        padding: 3rem;
        border-radius: 25px;
        margin-top: 2rem;
    }}
    /* Tüm yazıları beyaz yapıyoruz */
    h1, h2, h3, p, span, label, .stMarkdown {{
        color: white !important;
    }}
    /* Buton metinlerini beyaz yapıyoruz */
    .stButton>button {{
        color: white !important;
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid white;
    }}
    /* Tablo içindeki yazıların okunması için */
    .stDataFrame div, table {{
        color: white !important;
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
        ceviri = translator.translate(giris)
        
        # Excel'de karışıklık olmaması için her zaman İngilizce-Türkçe eşleşmesi yapıyoruz
        if st.session_state.kaynak_dil == 'en':
            ing, tr = giris, ceviri
        else:
            ing, tr = ceviri, giris
            
        st.session_state.kelimeler.append({"İngilizce": ing, "Türkçe": tr})
    st.session_state.yeni_kelime = ""

# --- ARAYÜZ ---
st.title("📝 Karıcığımın Dil Asistanı")

# Dosya Yükleme (Var olan Excel'i güncellemek için)
st.write("### 📂 Eski Listeni Güncelle")
yuklenen_dosya = st.file_uploader("Daha önce indirdiğin Excel dosyasını buraya bırak:", type=['xlsx'])
if yuklenen_dosya is not None:
    eski_df = pd.read_excel(yuklenen_dosya)
    if st.button("Listeye Dahil Et"):
        st.session_state.kelimeler = eski_df.to_dict('records')
        st.success("Eski liste başarıyla yüklendi!")

st.divider()

# Dil Değiştirme Bölümü
kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
hedef_etiket = "Türkçe" if st.session_state.hedef_dil == 'tr' else "İngilizce"

col_dil1, col_dil2, col_dil3 = st.columns([2,1,2])
with col_dil1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col_dil2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col_dil3: st.write(f"**Hedef:** {hedef_etiket}")

# Kelime Girişi
st.text_input(f"{kaynak_etiket} bir kelime yazın:", key="yeni_kelime", on_change=kelime_ekle)

# Liste Gösterimi
if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.write("### 📚 Kelimelerim")
    st.dataframe(df, use_container_width=True)

    # Excel Hazırlama
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Güncel Listeyi İndir", data=output.getvalue(), file_name="kelimelerim.xlsx")
    with c2:
        if st.button("🗑️ Listeyi Sıfırla"):
            st.session_state.kelimeler = []
            st.rerun()
