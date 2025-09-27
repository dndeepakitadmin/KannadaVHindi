import streamlit as st
from googletrans import Translator
from indic_transliteration.sanscript import transliterate, DEVANAGARI, IAST

# Initialize translator
translator = Translator()

# App title
st.set_page_config(page_title="Kannada → Hindi Learning App", page_icon="🌐")
st.title("🌐 Kannada → Hindi Helper")
st.markdown("Type a sentence in Kannada and get translations in Hindi + Roman script.")

# Input box
kannada_text = st.text_area("✍️ Enter Kannada text:", "")

if st.button("Translate") and kannada_text.strip():
    try:
        # Translate Kannada → Hindi
        translation = translator.translate(kannada_text, src="kn", dest="hi")
        hindi_text = translation.text

        # Romanized Hindi
        hindi_roman = transliterate(hindi_text, DEVANAGARI, IAST)

        # Show results
        st.success("✅ Translation complete!")
        st.write("**Kannada (Original):** ", kannada_text)
        st.write("**Hindi (Devanagari):** ", hindi_text)
        st.write("**Hindi (Romanized English):** ", hindi_roman)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
