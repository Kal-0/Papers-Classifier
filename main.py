import pytesseract, spacy, nltk, re, json, os
from PIL import Image
from pdf2image import convert_from_path
from nltk.corpus import stopwords
from collections import Counter
import google.generativeai as genai

# CONFIG ----------------------------------------------------------------------
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# -----------------------------------------------------------------------------


def pdf_to_image(pdf_path):
    pages = convert_from_path(pdf_path, dpi=200)
    img_path = "temp_page.jpg"
    pages[0].save(img_path, "JPEG")
    return img_path


def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        file_path = pdf_to_image(file_path)
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)


def segment_paragraphs(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def analyze_words(text):
    nltk.download("stopwords", quiet=True)
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    filtered = [w for w in words if w not in stopwords.words("english")]
    return len(filtered), Counter(filtered).most_common(10)


def detect_scientific(text):
    keys = ["abstract", "introduction", "keywords", "references"]
    return any(k in text.lower() for k in keys)


def summarize_with_gemini(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Summarize the following scientific text in 300 words. "
        "Preserve structure and clarity:\n\n" + text[:12000]
    )
    response = model.generate_content(prompt)
    return response.text


def main():
    file_path = input("Enter PDF or image path: ").strip()
    text = extract_text(file_path)
    paragraphs = segment_paragraphs(text)
    word_count, top_words = analyze_words(text)
    is_scientific = detect_scientific(text)
    compliant = len(paragraphs) > 4 and word_count > 2000

    summary = summarize_with_gemini(text) if is_scientific else "Not a valid document."

    result = {
        "is_scientific_article": is_scientific,
        "paragraphs": len(paragraphs),
        "word_count": word_count,
        "valid": compliant,
        "top_words": top_words,
        "summary": summary,
    }

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(json.dumps(result, indent=2))


if _name_ == "_main_":
    main()
