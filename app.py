import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Learn Hindi using Kannada Script", layout="wide")
st.title("Learn Hindi using Kannada script - ಕನ್ನಡ ಅಕ್ಷರ ಬಳಸಿ ಹಿಂದಿ ಕಲಿಯಿರಿ")

# -------------------------------
# Predefined phonetic mappings
# -------------------------------

# Kannada input → Hindi phonetic in Kannada letters
kannada_to_phonetic = {
    "ನಿನ್ನ ಹೆಸರೇನು ?": "ಆಪಕಾ ನಾಮ್ ಕ್ಯಾ ಹೈ ?",
    "ನೀವು ಹೇಗಿದ್ದೀರಾ ?": "ಆಪ್ ಕೈಸೆ ಹೈನ್ ?",
    "ಧನ್ಯವಾದ": "ಶುಕ್ರಿಯಾ",
    "ಮೇಲಾಗಿದೆಯಾ ?": "ಏ ಪಾಠ್ ಹೈ ?",
}

# Hindi → English phonetic
hindi_to_english_phonetic = {
    "तुम्हारा नाम क्या है?": "apaka naam kya hai?",
    "आप कैसे हैं?": "aap kaise hain?",
    "धन्यवाद": "dhanyavaad",
    "मौहाल कैसा है?": "maahaal kaisa hai?",
}

# -------------------------------
# Streamlit Input
# -------------------------------

kannada_text = st.text_area("Enter Kannada text (e.g., ನಿನ್ನ ಹೆಸರೇನು ?):")

if st.button("Generate Hindi Learning Output"):
    if kannada_text.strip() == "":
        st.warning("Please enter some Kannada text to translate.")
    else:
        try:
            # 1️⃣ Translate Kannada → Hindi using Google Translator
            hindi_translation = GoogleTranslator(source='kn', target='hi').translate(kannada_text)

            # 2️⃣ Kannada letters (phonetic) → from mapping
            kannada_phonetic = kannada_to_phonetic.get(
                kannada_text, "Phonetic not available for this sentence."
            )

            # 3️⃣ English phonetic → from mapping
            english_phonetic = hindi_to_english_phonetic.get(
                hindi_translation, "Phonetic not available for this sentence."
            )

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
