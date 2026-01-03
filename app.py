import streamlit as st
from PIL import Image
import pytesseract
import requests

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Universal Translator", page_icon="🌐")
st.title("🌐 Universal Translator")

# ---------------- MORSE DICTIONARY ----------------
MORSE = {
    'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
    'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---',
    'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---',
    'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
    'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 'y':'-.--',
    'z':'--..', '0':'-----', '1':'.----', '2':'..---',
    '3':'...--', '4':'....-', '5':'.....', '6':'-....',
    '7':'--...', '8':'---..', '9':'----.', ' ':' / '
}
REVERSE_MORSE = {v: k for k, v in MORSE.items()}

# ---------------- TRANSLATION FUNCTION ----------------
def translate_text(text, source, target):
    url = "https://libretranslate.de/translate"
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }
    try:
        res = requests.post(url, data=payload, timeout=10).json()
        return res.get("translatedText", "Translation failed")
    except:
        return "Translation failed"

# ---------------- MAIN MODE SELECTION ----------------
main_mode = st.radio(
    "Select Translator Type:",
    ["🌍 Language Translator", "📡 Morse Code"]
)

# =====================================================
# 🌍 LANGUAGE TRANSLATOR
# =====================================================
if main_mode == "🌍 Language Translator":

    st.markdown("""
    Translate **text or images** between languages:
    English, Russian, Japanese, Chinese, German, Spanish,
    French, Italian, Persian, Urdu, Hindi
    """)

    mode = st.radio("Input Type:", ["Text Input", "Image Input"])

    languages = {
        "English": "en",
        "Russian": "ru",
        "Japanese": "ja",
        "Chinese": "zh",
        "German": "de",
        "Spanish": "es",
        "French": "fr",
        "Italian": "it",
        "Persian": "fa",
        "Urdu": "ur",
        "Hindi": "hi"
    }

    if mode == "Text Input":
        source_lang = st.selectbox("From", languages.keys(), index=0)
        target_lang = st.selectbox("To", languages.keys(), index=1)
        text = st.text_input("Enter text")

        if text:
            translated = translate_text(text, languages[source_lang], languages[target_lang])
            st.success(f"✅ Translation:\n{translated}")

    else:
        source_lang = st.selectbox("From (OCR language)", languages.keys(), index=0)
        target_lang = st.selectbox("To", languages.keys(), index=1)
        uploaded_file = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            try:
                extracted_text = pytesseract.image_to_string(image)
                st.info(f"📄 Extracted Text:\n{extracted_text}")

                if extracted_text.strip():
                    translated = translate_text(
                        extracted_text,
                        languages[source_lang],
                        languages[target_lang]
                    )
                    st.success(f"✅ Translation:\n{translated}")
            except Exception as e:
                st.error(f"OCR Failed: {e}")

# =====================================================
# 📡 MORSE CODE TRANSLATOR
# =====================================================
elif main_mode == "📡 Morse Code":

    st.subheader("📡 Morse Code Translator")

    morse_mode = st.radio(
        "Mode",
        ["English → Morse", "Morse → English"]
    )

    text = st.text_area("Enter text")

    if text:
        if morse_mode == "English → Morse":
            result = " ".join(MORSE.get(c.lower(), "") for c in text)
        else:
            result = "".join(REVERSE_MORSE.get(c, "") for c in text.split())

        st.success(result)
