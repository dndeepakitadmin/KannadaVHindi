import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="wide")
st.title("Learn Hindi using Kannada script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# -------------------------------
# Kannada input → Kannada-letters Hindi phonetic (predefined)
# -------------------------------
kannada_to_phonetic = {
    "ನಿನ್ನ ಹೆಸರೇನು ?": "ಆಪಕಾ ನಾಮ್ ಕ್ಯಾ ಹೈ ?",
    "ನೀವು ಹೇಗಿದ್ದೀರಾ ?": "ಆಪ್ ಕೈಸೆ ಹೈನ್ ?",
    "ಧನ್ಯವಾದ": "ಶುಕ್ರಿಯಾ",
}

# -------------------------------
# Simple Devanagari → English phonetic mapping
# -------------------------------
# This is very basic; covers vowels and consonants commonly used in beginner sentences
devanagari_to_roman = {
    "अ": "a", "आ": "aa", "इ": "i", "ई": "ee", "उ": "u", "ऊ": "oo",
    "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au", "क": "k", "ख": "kh",
    "ग": "g", "घ": "gh", "च": "ch", "छ": "chh", "ज": "j", "झ": "jh",
    "ट": "t", "ठ": "th", "ड": "d", "ढ": "dh", "त": "t", "थ": "th",
    "द": "d", "ध": "dh", "न": "n", "प": "p", "फ": "ph", "ब": "b",
    "भ": "bh", "म": "m", "य": "y", "र": "r", "ल": "l", "व": "v",
    "श": "sh", "ष": "sh", "स": "s", "ह": "h", "ा": "aa", "ि": "i",
    "ी": "ee", "ु": "u", "ू": "oo", "े": "e", "ै": "ai", "ो": "o",
    "ौ": "au", "ं": "n", "ः": "h", "्": "",
    "?": "?", ".": ".", ",": ","
}

def devanagari_to_english(text):
    result = ""
    for char in text:
        result += devanagari_to_roman.get(char, char)
    # Replace double letters for simple readability
    result = result.replace("aa", "a").replace("ee", "i").replace("oo", "u")
    return result

# -------------------------------
# Streamlit Input
# -------------------------------
kannada_text = st.text_area("Enter Kannada text (e.g., ನಿನ್ನ ಹೆಸರೇನು ?):")

if st.button("Generate Hindi Learning Output"):
    if kannada_text.strip() == "":
        st.warning("Please enter some Kannada text to translate.")
    else:
        try:
            # 1️⃣ Hindi Translation
            hindi_translation = GoogleTranslator(source='kn', target='hi').translate(kannada_text)

            # 2️⃣ Kannada letters phonetic
            kannada_phonetic = kannada_to_phonetic.get(
                kannada_text, "Phonetic not available for this sentence."
            )

            # 3️⃣ English phonetic automatically
            english_phonetic = devanagari_to_english(hindi_translation)

            # -------------------------------
            # Display Results
            # -------------------------------
            st.subheader("Hindi in Kannada Letters (Phonetic)")
            st.write(kannada_phonetic)

            st.subheader("Hindi in English Phonetics")
            st.write(english_phonetic)

            st.subheader("Proper Hindi Translation")
            st.write(hindi_translation)

        except Exception as e:
            st.error(f"Error: {e}")
