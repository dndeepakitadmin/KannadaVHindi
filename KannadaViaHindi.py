import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from aksharamukha.transliterate import process
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import base64, tempfile, os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Hindi–Kannada Flashcards", layout="wide")
hide_st_style = """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🎴 Learn Kannada Through Hindi")
st.subheader("👉 Type any Hindi sentence and see word-by-word Kannada flashcards with audio")

# ---------------- USER INPUT ----------------
text = st.text_area("Enter Hindi sentence here:", "क्या कर रहा है वहां", height=100)

if st.button("Generate Flashcards"):
    words = text.strip().split()
    if not words:
        st.warning("Please enter some Hindi text.")
    else:
        cols = st.columns(3)
        for i, word in enumerate(words):
            try:
                # Translation: Hindi → Kannada
                kannada = GoogleTranslator(source="hi", target="kn").translate(word)
                
                # Kannada → Hindi script (transliteration)
                kannada_in_hindi = process('Kannada', 'Devanagari', kannada)
                
                # Kannada → English phonetic
                kannada_english = transliterate(kannada, sanscript.KANNADA, sanscript.ITRANS)

                # Generate audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts = gTTS(kannada, lang="kn")
                    tts.save(fp.name)
                    fp.seek(0)
                    audio_bytes = fp.read()
                b64 = base64.b64encode(audio_bytes).decode()
                os.remove(fp.name)
                audio_html = f'<audio controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

                # Flashcard layout
                with cols[i % 3]:
                    st.markdown(
                        f"""
                        <div style="
                            border-radius: 15px;
                            background-color: #fff8e7;
                            padding: 20px;
                            margin: 12px;
                            text-align: center;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                            transition: transform 0.3s;
                        ">
                            <h3 style="color:#000;">🪔 {word}</h3>
                            <hr style="border:1px solid #ffcc66;"/>
                            <p><b>Kannada:</b> <span style="color:#0a9396;">{kannada}</span></p>
                            <p><b>Kannada in Hindi:</b> <span style="color:#b45309;">{kannada_in_hindi}</span></p>
                            <p><b>Phonetic (English):</b> <i>{kannada_english}</i></p>
                            {audio_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception as e:
                st.error(f"❌ Error for word '{word}': {e}")
