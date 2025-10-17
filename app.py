import streamlit as st
from kokoro import KPipeline
import soundfile as sf
import io

st.set_page_config(page_title="Kokoro Multilingual Voice Generator", page_icon="🎙️")

st.title("🎙️ Kokoro Multilingual TTS (Male Voices Included)")
st.write("Generate unlimited multilingual speech using Kokoro TTS directly in your browser.")

lang = st.selectbox(
    "Choose language",
    ["en", "es", "fr", "hi", "it", "pt", "ja", "zh"],
    index=0,
    help="Language code: English, Spanish, French, Hindi, Italian, Portuguese, Japanese, Chinese."
)

voice = st.selectbox(
    "Select voice style",
    ["af_heart", "am_calm", "am_firm", "am_warm", "am_power", "am_deep"],
    help="af = female, am = male; choose accordingly."
)

text = st.text_area("Enter text to generate voice", "Hello there! Welcome to Kokoro TTS.")

if st.button("Generate Voice"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            pipeline = KPipeline(lang_code=lang)
            generator = pipeline(text, voice=voice)

            audio_data = None
            for _, _, audio in generator:
                audio_data = audio

            if audio_data is not None:
                buf = io.BytesIO()
                sf.write(buf, audio_data, 24000, format='WAV')
                st.audio(buf.getvalue(), format="audio/wav")

                st.download_button(
                    label="Download Audio",
                    data=buf.getvalue(),
                    file_name="kokoro_output.wav",
                    mime="audio/wav"
                )
            else:
                st.error("No audio generated. Try different input text.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Made with ❤️ using [Kokoro TTS](https://github.com/hexgrad/kokoro) and Streamlit.")
