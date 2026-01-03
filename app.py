import streamlit as st
from PIL import Image
import pytesseract
import requests

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Universal Translator", page_icon="🌐")

st.title("🌐 Universal Translator")
st.write("Translate text or images + Morse Code")

# ---------------- TRANSLATION FUNCTION ----------------
def translate_text(text, source, target):
    url = "https://translate.argosopentech.com/translate"
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        return res.json().get("translatedText", "Translation failed")
    except:
        return "Translation failed"

# ---------------- MORSE ----------------
MORSE = {
    'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
    'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---',
    'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---',
    'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
    'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 'y':'-.--',
    'z':'--..', ' ':' / '
}
REVERSE_MORSE = {v:k for k,v in MORSE.items()}

# ---------------- LANGUAGE LIST ----------------
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

# ---------------- MODE ----------------
mode = st.sidebar.radio(
    "Select Translator Type",
    ["🌍 Language Translator", "📡 Morse Code"]
)

# ---------------- LANGUAGE TRANSLATOR ----------------
if mode == "🌍 Language Translator":
    input_type = st.radio("Input Type", ["Text Input", "Image Input"])

    src = st.selectbox("From", languages.keys())
    tgt = st.selectbox("To", languages.keys())

    if input_type == "Text Input":
        text = st.text_input("Enter text")

        if text:
            result = translate_text(text, languages[src], languages[tgt])
            st.success(result)

    else:
        img = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
        if img:
            image = Image.open(img)
            st.image(image, use_column_width=True)

            extracted = pytesseract.image_to_string(image)
            st.info(extracted)

            if extracted.strip():
                result = translate_text(extracted, languages[src], languages[tgt])
                st.success(result)

# ---------------- MORSE ----------------
else:
    morse_mode = st.radio("Mode", ["English → Morse", "Morse → English"])
    text = st.text_input("Enter text")

    if text:
        if morse_mode == "English → Morse":
            output = " ".join(MORSE.get(c.lower(), "") for c in text)
        else:
            output = "".join(REVERSE_MORSE.get(c, "") for c in text.split())
        st.success(output)
