import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:0.6b"

def translate_content(content: str) -> tuple:
    if not content or not content.strip():
        return True, content

    try:
        # Step 1: Detect language
        detect_response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": f"What language is this text written in? Reply with only the language name, nothing else.\n\n{content}",
            "stream": False,
            "think": False,
        }, timeout=300)
        detect_response.raise_for_status()
        language = detect_response.json().get("response", "").strip().lower()

        if "english" in language:
            return True, content

        # Step 2: Translate if not English
        translate_response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": f"Translate the following text to English. Reply with only the translation, nothing else.\n\n{content}",
            "stream": False,
            "think": False,
        }, timeout=300)
        translate_response.raise_for_status()
        translation = translate_response.json().get("response", "").strip()

        return False, translation
    except Exception as e:
        print(f"Translation error: {e}")
        return True, content
