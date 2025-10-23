# System Blueprint
## Scientific Document Detection and Analysis System

---

### 1. Architecture Overview
The system is composed of three main modules:

```
┌─────────────────────────────┐
│       Input Layer           │
│ (PDF/Image Upload Service)  │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│  Processing Core            │
│ ├─ OCR Module               │
│ ├─ Segmentation Module      │
│ ├─ Text Extraction & Stats  │
│ └─ LLM Summarization Engine │
└────────────┬────────────────┘
             │
┌────────────▼────────────────┐
│       Output Layer           │
│ (Validation + Summary View) │
└─────────────────────────────┘
```

---

### 2. Module Breakdown

#### **1. Input Layer**
- Accepts `.pdf`, `.jpg`, `.png` files.  
- Converts PDFs into page images if necessary.  
- Validates file size and type.

#### **2. OCR & Segmentation**
- **OCR Engine** extracts raw text using Tesseract or PaddleOCR.  
- **Segmentation Module** identifies paragraph boundaries using:
  - Text block spacing (OpenCV + heuristic rules).  
  - Optional NLP-based segmentation with spaCy.

#### **3. Text Analysis**
- Counts paragraphs.  
- Tokenizes and normalizes text.  
- Computes:
  - Word count  
  - Frequency distribution  
  - Top 10 most common words  

#### **4. Classification**
- Rule-based or ML-assisted classifier to decide if the text matches a scientific article (based on presence of:
  - Abstract
  - Keywords
  - References
  - Author names / affiliations).

#### **5. Summarization**
- Uses an LLM (GPT or similar) **only for the summary generation**.  
- Prompts model to generate a concise summary within 300–400 words.

#### **6. Compliance Check**
- Evaluate:
  - `paragraph_count >= 4`
  - `word_count >= 2000`
- Output result as:
  ```json
  {
    "is_scientific_article": true,
    "paragraphs": 7,
    "words": 2645,
    "valid": true,
    "summary": "..."
  }
  ```

#### **7. Output Layer**
- Displays summary and validation messages to user:
  - “✅ Valid scientific article”
  - “❌ Not a valid document”

---

### 3. Data Flow
```
[Upload PDF/Image]
       ↓
[OCR Extraction]
       ↓
[Segmentation → Paragraphs]
       ↓
[Text Stats (word count, freq)]
       ↓
[Scientific Classification]
       ↓
[LLM Summarization]
       ↓
[Compliance Report + Summary Output]
```

---

### 4. Implementation Notes
- Preprocessing: normalize text encoding (UTF-8) and remove line breaks.  
- Use **regex or NLP heuristics** to detect scientific keywords.  
- Summarization prompt example:

```
"You are an assistant summarizing scientific articles. 
Summarize the following text in less than 400 words, 
preserving structure and clarity."
```

---

### 5. Possible Extensions
- Add a confidence score for article detection.  
- Allow batch analysis for multiple PDFs.  
- Integrate a visual layout inspector for segmented paragraphs.
