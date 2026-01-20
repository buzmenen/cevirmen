import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

# Sayfa ayarları
st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- ARKA PLAN VE TASARIM AYARI (CSS) ---
# Yeni resim linkini buraya ekledim
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
    
    /* Yazıların olduğu kutunun şıklığı ve okunabilirliği */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.82); /* Hafif şeffaf beyaz katman */
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }}

    /* Yazı renklerini netleştirelim */
    h1, h2, h3, p, span, label {{
        color: #1e272e !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* Butonları özelleştirelim */
    .stButton>button {{
        border-radius: 10px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------

st.title("📝 Dil Asistanım")
st.write("Hoş geldin! Kelimelerini yazıp 'Enter'a basarak listeni oluşturabilirsin.")

# Hafızayı başlat
if 'kelimeler' not in st.session_state:
    st.session_state.kelimeler = []

# Giriş kutusunu sıfırlayan fonksiyon
def kelime_ekle():
    ingilizce_kelime = st.session_state.yeni_kelime.strip()
    
    if ingilizce_kelime:
        translator = GoogleTranslator(source='en', target='tr')
        try:
            turkce_kelime = translator.translate(ingilizce_kelime)
            
            # Listeye ekle (Aynı kelime yoksa)
            if not any(d['İngilizce'] == ingilizce_kelime for d in st.session_state.kelimeler):
                st.session_state.kelimeler.append({
                    "İngilizce": ingilizce_kelime, 
                    "Türkçe": turkce_kelime
                })
        except Exception:
            st.error("Çeviri yapılırken bir bağlantı sorunu oluştu.")
    
    # Kutuyu temizle
    st.session_state.yeni_kelime = ""

# Giriş alanı
st.text_input("İngilizce kelime yazın:", key="yeni_kelime", on_change=kelime_ekle, placeholder="Örn: Adventure")

# Liste varsa tabloyu ve butonları göster
if st.session_state.kelimeler:
    st.write("### 📚 Kelime Listem")
    df = pd.DataFrame(st.session_state.kelimeler)
    st.table(df)

    # Excel hazırlama
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kelimelerim')
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.download_button(
            label="📥 Excel Olarak İndir",
            data=output.getvalue(),
            file_name="kelimelerim.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with c2:
        if st.button("🗑️ Tüm Listeyi Sil"):
            st.session_state.kelimeler = []
            st.rerun()
