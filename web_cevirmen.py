import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

st.title("📝 Karımın Çeviri Asistanı")
st.write("Bu kod sayesinde istediğin kelimenin ingilizce halini çevirebilir ve excele kaydedebilirsin karıcığım. İngilizce karşılığı yoksa olduğu gibi kaydeder.")

# Hafızayı başlat
if 'kelimeler' not in st.session_state:
    st.session_state.kelimeler = []

# Giriş kutusunu sıfırlamak için kullanılan fonksiyon
def kelime_ekle():
    ingilizce_kelime = st.session_state.yeni_kelime.strip()
    
    if ingilizce_kelime and ingilizce_kelime.lower() != 'q':
        # Çeviri işlemi
        translator = GoogleTranslator(source='en', target='tr')
        turkce_kelime = translator.translate(ingilizce_kelime)
        
        # Listeye ekle (Eğer daha önce eklenmemişse)
        if not any(d['İngilizce'] == ingilizce_kelime for d in st.session_state.kelimeler):
            st.session_state.kelimeler.append({
                "İngilizce": ingilizce_kelime, 
                "Türkçe": turkce_kelime
            })
    
    # Giriş kutusunu temizle
    st.session_state.yeni_kelime = ""

# Giriş alanı (on_change kullanarak Enter'a basıldığında fonksiyonu çağırıyoruz)
st.text_input("Karıcığım lütfen istediğin kelimeyi yaz ve entera bas:", key="yeni_kelime", on_change=kelime_ekle)

# Eklenen kelimeleri tablo olarak göster
if st.session_state.kelimeler:
    st.write("### Kaydedilen Kelimeler")
    df = pd.DataFrame(st.session_state.kelimeler)
    st.table(df)

    # Excel dosyasına dönüştürme
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kelimelerim')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 EXCEL İÇİN BANA TIKLA BEBEĞİM OW YEAHHH",
            data=output.getvalue(),
            file_name="kelimelerim.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        if st.button("🗑️ Listeyi Temizleyebilirsin karıcığım <3"):
            st.session_state.kelimeler = []
            st.rerun()

