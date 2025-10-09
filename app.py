import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="wide")
st.title("Learn Hindi using Kannada script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# Input from user
kannada_text = st.text_area("Enter Kannada text (e.g., ನಿನ್ನ ಹೆಸರೇನು ?)")

if st.button("Translate"):
    if kannada_text.strip() == "":
        st.warning("Please enter some Kannada text to translate.")
    else:
        try:
            # Step 1: Transliterate Kannada → Devanagari
            devanagari_text = transliterate(kannada_text, sanscript.KANNADA, sanscript.DEVANAGARI)

            # Step 2: Translate meaningfully to Hindi
            hindi_translation = GoogleTranslator(source='auto', target='hi').translate(devanagari_text)

            # Step 3: Transliterate Hindi → Kannada letters (phonetic)
            hindi_in_kannada_letters = transliterate(hindi_translation, sanscript.DEVANAGARI, sanscript.KANNADA)

            # Step 4: Transliterate Hindi → English phonetics
            hindi_in_english_phonetic = transliterate(hindi_translation, sanscript.DEVANAGARI, sanscript.ITRANS)

            # Display outputs
            st.subheader("Hindi in Kannada Letters (Phonetic)")
            st.write(hindi_in_kannada_letters)

            st.subheader("Hindi in English Phonetics")
            st.write(hindi_in_english_phonetic)

            st.subheader("Proper Hindi Translation")
            st.write(hindi_translation)

        except Exception as e:
            st.error(f"Error during translation: {e}")
