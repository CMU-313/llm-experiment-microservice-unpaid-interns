import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:0.6b"


def strip_think_tags(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def translate_content(content: str) -> tuple:
    if not content or not content.strip():
        return True, content

    try:
        detect_response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": (
                    "What language is the following text written in? "
                    "Reply with ONLY the language name, nothing else. "
                    "Do not explain.\n\n"
                    + content
                ),
                "stream": False,
            },
            timeout=300,
        )
        detect_response.raise_for_status()

        raw_language = detect_response.json().get("response", "")
        language = strip_think_tags(raw_language).lower()

        if language == "english" or language.strip().rstrip(".") == "english":
            return True, content

        translate_response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": (
                    "Translate the following text to English. "
                    "Reply with ONLY the translation, nothing else. "
                    "Do not explain.\n\n"
                    + content
                ),
                "stream": False,
            },
            timeout=300,
        )
        translate_response.raise_for_status()

        raw_translation = translate_response.json().get("response", "")
        translation = strip_think_tags(raw_translation)

        if not translation:
            return True, content

        return False, translation

    except Exception as e:
        print(f"Translation error: {e}")
        return True, content
