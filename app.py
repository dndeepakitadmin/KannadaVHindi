import streamlit as st
import whisper
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# -------------------------------
# Load Whisper model (speech-to-text)
# -------------------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("small")  # small = balance of accuracy + speed

whisper_model = load_whisper()

# -------------------------------
# Load IndicTrans2 model (translation)
# -------------------------------
@st.cache_resource
def load_indictrans():
    model_name = "ai4bharat/indictrans2-indic-indic-1B"  # for Indian ↔ Indian langs
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
    return tokenizer, model

tokenizer, trans_model = load_indictrans()

def translate(text, src_lang="hin_Deva", tgt_lang="kan_Knda"):
    # IndicTrans2 expects input format with lang codes
    batch = tokenizer(
        [f"<2{tgt_lang}> {text}"],
        return_tensors="pt"
    )
    with torch.no_grad():
        generated = trans_model.generate(
            **batch,
            num_beams=5,
            max_length=256
        )
    output = tokenizer.batch_decode(generated, skip_special_tokens=True)
    return output[0]

# -------------------------------
# Streamlit App UI
# -------------------------------
st.set_page_config(page_title="Hindi ↔ Kannada Translator", page_icon="🌐", layout="centered")

st.title("🌐 Learn Hindi via Kannada - Free AI App")
st.write("Upload audio or enter text in **Kannada/Hindi**, get transcription + translation.")

# Input method
option = st.radio("Choose input method:", ["🎤 Upload Audio", "⌨️ Enter Text"])

input_text = ""

if option == "🎤 Upload Audio":
    uploaded_file = st.file_uploader("Upload an audio file (MP3/WAV/M4A)", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        with open("temp_audio.mp3", "wb") as f:
            f.write(uploaded_file.read())
        st.info("⏳ Transcribing with Whisper...")
        result = whisper_model.transcribe("temp_audio.mp3")
        input_text = result["text"]
        st.success("✅ Transcription done!")
        st.write("**Transcribed Text:**", input_text)

elif option == "⌨️ Enter Text":
    input_text = st.text_area("Enter Hindi/Kannada text:")

# Translation
if input_text:
    st.markdown("---")
    st.subheader("🔄 Translation")

    direction = st.radio("Choose translation direction:", ["Hindi → Kannada", "Kannada → Hindi"])

    if st.button("Translate"):
        if direction == "Hindi → Kannada":
            translated = translate(input_text, src_lang="hin_Deva", tgt_lang="kan_Knda")
        else:
            translated = translate(input_text, src_lang="kan_Knda", tgt_lang="hin_Deva")

        st.success("✅ Translation complete!")
        st.write("**Translated Text:**", translated)
