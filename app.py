import streamlit as st
from deep_translator import GoogleTranslator
from aksharamukha.transliterate import process

st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="wide")
st.title("Learn Hindi using Kannada script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

kannada_text = st.text_area("Enter Kannada text (e.g., ನಿನ್ನ ಹೆಸರೇನು ?):")

if st.button("Generate Hindi Learning Output"):
    if kannada_text.strip() == "":
        st.warning("Please enter some Kannada text to translate.")
    else:
        try:
            # Step 1: Translate Kannada → Hindi
            hindi_translation = GoogleTranslator(source='kn', target='hi').translate(kannada_text)

            # Step 2: Hindi → Kannada letters (phonetic)
            hindi_in_kannada_letters = process(hindi_translation, 'Devanagari', 'Kannada')

            # Step 3: Hindi → English phonetic
            hindi_in_english_phonetic = process(hindi_translation, 'Devanagari', 'IAST')

            st.subheader("Hindi in Kannada Letters (Phonetic)")
            st.write(hindi_in_kannada_letters)

            st.subheader("Hindi in English Phonetics")
            st.write(hindi_in_english_phonetic)

            st.subheader("Proper Hindi Translation")
            st.write(hindi_translation)

        except Exception as e:
            st.error(f"Error: {e}")
