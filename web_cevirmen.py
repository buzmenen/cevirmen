import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

st.title("📝 Kelime Çeviri ve Excel Oluşturucu")
st.write("Kelimeleri girin, çevirileri görün ve listenizi Excel olarak indirin.")

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
st.text_input("İngilizce kelime yazın ve Enter'a basın:", key="yeni_kelime", on_change=kelime_ekle)

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
            label="📥 Excel Dosyasını İndir",
            data=output.getvalue(),
            file_name="kelimelerim.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        if st.button("🗑️ Listeyi Temizle"):
            st.session_state.kelimeler = []
            st.rerun()
