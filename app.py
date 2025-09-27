import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration.sanscript import transliterate, DEVANAGARI, KANNADA, ITRANS

st.set_page_config(page_title="Kannada → Hindi Helper", layout="centered")

st.title("📖 Kannada → Hindi Learning App")
st.write("Enter Kannada text, and see Hindi translation, Kannada-script transliteration, and English phonetics.")

# Input box
input_text = st.text_area("Enter Kannada text:", height=150)

def translate_to_hindi(text):
    try:
        return GoogleTranslator(source="kn", target="hi").translate(text)
    except Exception as e:
        return f"(Translation Error: {e})"

def transliterate_to_kannada(hindi_text):
    try:
        return transliterate(hindi_text, DEVANAGARI, KANNADA)
    except Exception as e:
        return f"(Transliteration Error: {e})"

def transliterate_to_english(hindi_text):
    try:
        return transliterate(hindi_text, DEVANAGARI, ITRANS)
    except Exception as e:
        return f"(Transliteration Error: {e})"

if st.button("Translate & Transliterate"):
    if not input_text.strip():
        st.warning("⚠️ Please enter Kannada text.")
    else:
        # Step 1: Kannada → Hindi
        hindi_text = translate_to_hindi(input_text)

        # Step 2: Hindi → Kannada script
        kannada_output = transliterate_to_kannada(hindi_text)

        # Step 3: Hindi → Roman English phonetics
        english_output = transliterate_to_english(hindi_text)

        st.subheader("Hindi Translation")
        st.text(hindi_text)

        st.subheader("Hindi in Kannada Script")
        st.text(kannada_output)

        st.subheader("Roman English Phonetics")
        st.text(english_output)
