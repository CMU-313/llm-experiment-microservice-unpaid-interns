from unittest.mock import patch, MagicMock
from src.translator import translate_content

# Existing hardcoded test
def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_english():
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True

# Mock tests from Colab
def test_llm_normal_response():
    is_english, translated_content = translate_content("Dies ist eine Nachricht auf Deutsch")
    assert is_english == False
    assert translated_content == "This is a German message"

def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdfjkl;qweruiop")
    assert is_english == True

def test_null_content():
    is_english, translated_content = translate_content("")
    assert is_english == True

def test_none_like_content():
    is_english, translated_content = translate_content("None")
    assert is_english == True