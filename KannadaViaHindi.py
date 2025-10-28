import streamlit as st
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from aksharamukha.transliterate import process
from gtts import gTTS
import os
from io import BytesIO

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Hindi → Kannada Learning", layout="wide", page_icon="🪔")

# --- HIDE STREAMLIT DEFAULT ELEMENTS (CLEAN VIEW FOR EMBED) ---
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    iframe[title="streamlit/share"] {display: none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- TITLE ---
st.title("🪔 Learn Kannada using Hindi Script")
st.caption("Translate Hindi → Kannada → Learn with Hindi-letter Flashcards & Audio")

# --- INPUT BOX ---
text = st.text_area("Enter Hindi sentence (e.g., क्या कर रहे हो?)", height=120)

if st.button("Translate"):
    if text.strip():
        try:
            # Hindi → Kannada full translation
            kannada_text = GoogleTranslator(source="hi", target="kn").translate(text)

            # Kannada → Hindi transliteration
            kannada_in_hindi = process('Kannada', 'Devanagari', kannada_text)

            # Kannada → English phonetics
            kannada_in_english = transliterate(kannada_text, sanscript.KANNADA, sanscript.ITRANS)

            # --- DISPLAY RESULTS ---
            st.markdown("### 🔹 Translation Summary")
            st.markdown(f"**Hindi Input:**  \n:blue[{text}]")
            st.markdown(f"**Kannada Translation (native script):**  \n:green[{kannada_text}]")
            st.markdown(f"**Kannada (in Hindi letters):**  \n:orange[{kannada_in_hindi}]")
            st.markdown(f"**Kannada (in English phonetics):**  \n`{kannada_in_english}`")

            # --- FLASHCARDS SECTION ---
            st.markdown("---")
            st.subheader("🧠 Word Flashcards (Hindi → Kannada with Audio)")

            # Split into words
            hindi_words = text.split()
            kannada_words = kannada_text.split()
            kannada_hindi_words = kannada_in_hindi.split()

            cols = st.columns(3)

            for i, (src_hi, word_kn, word_hi) in enumerate(zip(hindi_words, kannada_words, kannada_hindi_words)):
                with cols[i % 3]:
                    # Create Kannada audio for pronunciation
                    tts = gTTS(text=word_kn, lang='kn')
                    audio_fp = BytesIO()
                    tts.write_to_fp(audio_fp)
                    audio_fp.seek(0)

                    # Flashcard layout
                    card_html = f"""
                    <div style="
                        background-color:#fffbe6;
                        border-radius:15px;
                        padding:20px;
                        margin:10px;
                        text-align:center;
                        box-shadow:0 2px 8px rgba(0,0,0,0.15);
                        border:1px solid #f0d96f;">
                        <h3 style="color:#000;">{src_hi}</h3>
                        <p style="font-size:18px; color:#c77902;">→ {word_hi}</p>
                        <p style="font-size:13px; color:#555;">(Kannada Audio)</p>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    st.audio(audio_fp, format='audio/mp3')

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter some Hindi text to translate.")
