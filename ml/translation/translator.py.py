import json
import os

DATA_PATH = os.path.join("ml", "sample_phrases.json")

def load_phrases():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

PHRASES = load_phrases()

def normalize_text(text):
    return text.strip().replace("?", "").replace("।", "")

def detect_language(text):
    """
    Very simple keyword-based language detection.
    This simulates early-stage NLP language identification
    for low-resource languages.
    """
    garhwali_markers = ["पाणी", "कैसो", "कठां", "म्यर"]
    kumaoni_markers = ["पानी", "कसो", "कत", "म्यर"]

    for word in garhwali_markers:
        if word in text:
            return "garhwali"

    for word in kumaoni_markers:
        if word in text:
            return "kumaoni"

    return "unknown"

def translate(text, language=None):
    """
    Translates Garhwali/Kumaoni text to Hindi and English.
    Returns translation along with a confidence score.
    """
    text = normalize_text(text)

    if not language or language == "auto":
        language = detect_language(text)

    if language not in PHRASES:
        return {
            "hindi": "भाषा पहचानी नहीं जा सकी",
            "english": "Language could not be detected",
            "confidence": 0.0,
            "language_detected": language
        }

    phrases = PHRASES[language]

    for key in phrases:
        if key in text:
            return {
                "hindi": phrases[key]["hi"],
                "english": phrases[key]["en"],
                "confidence": 0.85,
                "language_detected": language
            }

    return {
        "hindi": "अनुवाद उपलब्ध नहीं है",
        "english": "Translation not available",
        "confidence": 0.3,
        "language_detected": language
    }

# ------------------ TESTING ------------------
if __name__ == "__main__":
    tests = [
        "पाणी",
        "कैसो छो",
        "लोकल मंदिर कठां छ",
        "डॉक्टर कत मिलछ"
    ]

    for t in tests:
        print("Input:", t)
        print("Output:", translate(t, "auto"))
        print("-" * 40)
