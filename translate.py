from robyn import Robyn
from googletrans import Translator
import json

app = Robyn(__file__)
translator = Translator()

def translate_ar_en(text: str) -> str:
    """
    Detects if the input is Arabic or English and translates to the other.
    """
    detected_lang = translator.detect(text).lang
    target_lang = 'en' if detected_lang == 'ar' else 'ar'
    return translator.translate(text, dest=target_lang).text

@app.post("/translate")
async def translate(request):
    try:
        data = json.loads(request.body)
        text = data.get("text", "").strip()

        if not text:
            return {"status_code": 400, "body": "Missing or empty 'text' field"}

        translated = translate_ar_en(text)

        return {
            "data": {
                "original": text,
                "translated": translated
            }
        }
    except Exception as e:
        return {"status_code": 500, "body": f"Error: {str(e)}"}

@app.get("/")
async def home():
    return "🌍 Robyn Translator is running. POST to /translate with JSON: { text: 'your text' }"

app.start(port=8000)
