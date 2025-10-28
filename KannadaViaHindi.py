import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(
    page_title="Hindi to Kannada Learning",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

# ------------------ HIDE STREAMLIT UI ------------------ #
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------ APP CONTENT ------------------ #
st.title("📝 Learn Kannada using Hindi script")
st.subheader("हिंदी अक्षरों का उपयोग करके कन्नड़ सीखें")

# Input
text = st.text_area("Enter Hindi text here (e.g., आप कैसे हैं?)", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # Hindi → Kannada translation
            kannada = GoogleTranslator(source="hi", target="kn").translate(text)

            # Kannada → English phonetics (IAST)
            kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

            # Kannada → Hindi letters (transliteration)
            kannada_in_hindi = process('Kannada', 'Devanagari', kannada)

            # ---------------- OUTPUT ---------------- #
            st.markdown("### 🔹 Translation Results")

            # Hindi Input
            st.markdown(f"**Hindi Input:**  \n:blue[{text}]")

            # Kannada Translation
            st.markdown(f"**Kannada Translation:**  \n:green[{kannada}]")

            # Kannada in Hindi letters
            st.markdown(f"**Kannada in Hindi letters:**  \n:orange[{kannada_in_hindi}]")

            # Kannada in English phonetics
            st.markdown(f"**Kannada in English phonetics:**  \n`{kannada_english}`")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some Hindi text to translate!")
