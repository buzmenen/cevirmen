import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

st.title("📝 Kelime Çeviri ve Excel Oluşturucu")
st.write("Kelimeleri girin, çevirileri görün ve listenizi Excel olarak indirin.")

# Tarayıcı oturumunda kelimeleri saklamak için (Session State)
if 'kelimeler' not in st.session_state:
    st.session_state.kelimeler = []

# Giriş alanı
ingilizce_kelime = st.text_input("İngilizce kelime yazın ve Enter'a basın:", key="input_box")

if ingilizce_kelime:
    # Çeviri işlemi
    translator = GoogleTranslator(source='en', target='tr')
    turkce_kelime = translator.translate(ingilizce_kelime)
    
    # Listeye ekle (Eğer daha önce eklenmemişse)
    if not any(d['İngilizce'] == ingilizce_kelime for d in st.session_state.kelimeler):
        st.session_state.kelimeler.append({
            "İngilizce": ingilizce_kelime, 
            "Türkçe": turkce_kelime
        })

# Eklenen kelimeleri tablo olarak göster
if st.session_state.kelimeler:
    df = pd.DataFrame(st.session_state.kelimeler)
    st.table(df)

    # Excel dosyasına dönüştürme (Hafızada tutulur)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kelimelerim')
    
    # İndirme Butonu
    st.download_button(
        label="Excel Dosyasını İndir",
        data=output.getvalue(),
        file_name="kelimelerim.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    if st.button("Listeyi Temizle"):
        st.session_state.kelimeler = []
        st.rerun()