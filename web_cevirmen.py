import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- TASARIM VE ARKA PLAN AYARI ---
# Yeni seçtiğin resmin doğrudan linki
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
    
    /* Yazıları KOYU LACİVERT yapıyoruz (Bu resimde en iyi bu görünür) */
    h1, h2, h3, p, span, label, .stMarkdown p {{
        color: #2c3e50 !important; 
        font-weight: 800 !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8); /* Yazıların arkasına hafif aydınlık */
    }}

    /* Dosya yükleme alanı açıklamaları */
    .stFileUploader label, .stFileUploader small {{
        color: #2c3e50 !important;
    }}

    /* Giriş kutusu tasarımı */
    .stTextInput input {{
        color: black !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #5d6d7e !important;
        border-radius: 10px;
    }}

    /* Butonlar (Resimle uyumlu yumuşak bir ton) */
    .stButton>button {{
        color: white !important;
        background-color: #5d6d7e !important;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }}
    
    .stButton>button:hover {{
        background-color: #2c3e50 !important;
        transform: scale(1.03);
    }}
    
    /* Tablo verileri siyah kalsın */
    .stDataFrame div {{
        color: black !important;
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
            st.error("Çeviri sırasında bir hata oluştu.")
    st.session_state.yeni_kelime = ""

# --- ARAYÜZ ---
st.title("📝 Karıcığımın Dil Asistanı")

st.write("### 📂 Eski Listeni Güncelle")
yuklenen_dosya = st.file_uploader("Daha önce indirdiğin Excel'i yükle:", type=['xlsx'])
if yuklenen_dosya is not None:
    if st.button("Listeye Dahil Et"):
        try:
            eski_df = pd.read_excel(yuklenen_dosya)
            st.session_state.kelimeler = eski_df.to_dict('records')
            st.success("Liste başarıyla güncellendi!")
        except:
            st.error("Dosya okunurken bir hata oluştu.")

st.divider()

# Dil Değiştirme Alanı
kaynak_etiket = "İngilizce" if st.session_state.kaynak_dil == 'en' else "Türkçe"
col_dil1, col_dil2, col_dil3 = st.columns([2,1,2])
with col_dil1: st.write(f"**Kaynak:** {kaynak_etiket}")
with col_dil2: st.button("🔄 Değiştir", on_click=dil_degistir)
with col_dil3: st.write(f"**Hedef:** {'Türkçe' if st.session_state.hedef_dil == 'tr' else 'İngilizce'}")

# Kelime Giriş Alanı
st.text_input(f"{kaynak_etiket} bir kelime yazın:", key="yeni_kelime", on_change=kelime_ekle)

# Liste ve İndirme Butonları
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
