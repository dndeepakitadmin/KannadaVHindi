import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# ------------------ Functions ------------------

def translate_to_hindi(kannada_text):
    try:
        return GoogleTranslator(source='kn', target='hi').translate(kannada_text)
    except Exception as e:
        return f"(Translation Error: {e})"

def hindi_to_kannada_script(hindi_text):
    try:
        return transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.KANNADA)
    except Exception as e:
        return f"(Transliteration Error: {e})"

def hindi_to_roman(hindi_text):
    try:
        return transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS)
    except Exception as e:
        return f"(Transliteration Error: {e})"

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Kannada → Hindi Helper", layout="centered")
st.title("Kannada → Hindi Learning App")
st.write("Enter Kannada text, get Hindi translation, Kannada script, and Roman phonetics.")

input_text = st.text_area("Enter Kannada Text:", height=120)

if st.button("Translate & Transliterate"):
    if not input_text.strip():
        st.warning("Please enter some Kannada text.")
    else:
        hindi_text = translate_to_hindi(input_text)
        kannada_output = hindi_to_kannada_script(hindi_text)
        roman_output = hindi_to_roman(hindi_text)

        st.subheader("Hindi Translation")
        st.text(hindi_text)

        st.subheader("Hindi in Kannada Script")
        st.text(kannada_output)

        st.subheader("Roman Phonetic (English letters)")
        st.text(roman_output)

st.markdown("---")
st.caption("Free app by LearnHindiVKannada | Powered by Streamlit, Deep Translator & Indic Transliteration")
