
import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍"
)

LANGUAGES = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}

st.title("🌍 Language Translation Tool")
st.write("Translate text from one language to another.")

source = st.selectbox(
    "Select source language",
    list(LANGUAGES.keys()),
    index=0
)

target = st.selectbox(
    "Select target language",
    list(LANGUAGES.keys()),
    index=1
)

text = st.text_area(
    "Enter text to translate",
    placeholder="Type your text here..."
)

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Please select different languages.")

    else:
        try:
            with st.spinner("Translating..."):
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text.strip(),
                        "langpair": (
                            f"{LANGUAGES[source]}|"
                            f"{LANGUAGES[target]}"
                        )
                    },
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

                if data.get("responseStatus") == 200:
                    result = data.get(
                        "responseData", {}
                    ).get("translatedText", "")

                    if result:
                        st.subheader("Translated Text")
                        st.write(result)

                        st.download_button(
                            "Download Translation",
                            data=result,
                            file_name="translation.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("No translation was returned.")
                else:
                    st.error("Translation failed. Please try again.")

        except requests.RequestException:
            st.error(
                "Connection error. Check your internet connection "
                "and try again."
            )
        except (ValueError, KeyError):
            st.error("Unexpected response from the service.")

st.caption("CodeAlpha AI Internship Project")
