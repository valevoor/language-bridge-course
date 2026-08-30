# 🎓 Kannada to English STEM Bridge Course Engine — Rules & Guidelines (GEMINI.md)

## 📌 Project Overview
An automated, bilingual AI bridge course engine and interactive teaching platform that ingests native Kannada STEM textbooks (Karnataka State Syllabus, Grade 8 Mathematics Parts 1 & 2), extracts foundational mathematical & scientific keywords, and produces structured datasets, flashcards, quizzes, and standalone interactive teaching web applications.

---

## 📁 Repository Structure & Folder Roles

- **`resources/`**: Input textbook repository containing Kannada language PDF textbooks.
  - `8th-Kannada-Maths-Part-1.pdf`: Grade 8 Mathematics Part 1 (Chapters 1–7).
  - `8th Kannada Maths Part 2 2026-27.pdf`: Grade 8 Mathematics Part 2 (Chapters 8–14).
- **`src/`**: All source code, extraction agents, domain dictionaries, and application scripts:
  - `pdf_processor.py`: PyMuPDF PDF parser, Nudi/ASCII legacy font to Unicode Kannada converter, text normalizer, and chapter segmenter.
  - `stem_dictionary.py`: Curated bilingual STEM domain knowledge base covering all 14 chapters, definitions, pronunciations, and memory tips.
  - `agent.py`: `STEMExtractionAgent` that scans text, matches terms, extracts contextual sentences from the book, and calculates term frequencies.
  - `exporters.py`: `STEMExporter` multi-format file export engine (JSON, CSV, Markdown, Flashcards).
  - `generate_web_app.py`: Generator for the standalone, dependency-free interactive HTML teaching platform.
  - `pipeline.py`: End-to-end orchestrator coordinating multi-book ingestion -> extraction -> export -> web app build.
  - `main.py`: CLI entrypoint for running extractions.
  - `app.py`: Interactive Streamlit web application.
  - `tests/test_extraction.py`: Automated Pytest unit & integration test suite.
- **`target/`**: Output directory for generated artifacts and datasets:
  - `index.html`: Interactive teaching web platform.
  - `stem_keywords_chapterwise.json`: Complete 14-chapter bilingual dataset.
  - `stem_keywords_chapterwise.csv`: Flat tabular dataset for spreadsheets.
  - `stem_keywords_chapterwise.md`: Formatted Markdown study guide and cheatsheet.
  - `stem_flashcards.json`: Flashcard deck for study games.
- **`index.html`**: Root-level copy of the interactive teaching web application for direct browser access.

---

## 🛠️ Common Commands

### 1. Ingest Textbooks & Run Full Extraction Pipeline
```bash
python3 src/main.py
```
*(Automatically scans all PDFs in resources/, extracts 14 chapters, and updates all outputs in target/ and root index.html)*

### 2. Launch Standalone Interactive HTML Teaching App
```bash
# Direct browser opening:
open index.html

# Or via local HTTP web server:
python3 -m http.server 8000
```

### 3. Launch Streamlit Web App
```bash
streamlit run src/app.py
```

### 4. Run Automated Test Suite
```bash
python3 -m pytest src/tests/test_extraction.py -v
```

---

## 📖 Chapter & Curriculum Mapping (Grade 8 Mathematics)

| Part | Chapter | Kannada Title | English Concept |
| :--- | :--- | :--- | :--- |
| **Part 1** | **Ch 1** | ವರ್ಗ ಮತ್ತು ಘನ | Squares and Cubes |
| **Part 1** | **Ch 2** | ಘಾತಾಂಕಗಳ ಆಟ | Playing with Exponents and Powers |
| **Part 1** | **Ch 3** | ಸಂಖ್ಯೆಗಳ ಕಥೆ | The Story of Numbers (Numeral Systems & Place Value) |
| **Part 1** | **Ch 4** | ಚತುರ್ಭುಜಗಳು | Quadrilaterals (Rectangles, Rhombus, Parallelograms) |
| **Part 1** | **Ch 5** | ಸಂಖ್ಯೆಗಳ ಆಟ | Playing with Numbers (Factors, Multiples, Divisibility) |
| **Part 1** | **Ch 6** | ನಾವು ವಿಭಜಿಸುತ್ತೇವೆ... | Factors, Multiples and Algebraic Expressions |
| **Part 1** | **Ch 7** | ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-1 | Proportional Reasoning - 1 (Ratios & Unitary Method) |
| **Part 2** | **Ch 8** | ವೇಷಧಾರಿ ಭಿನ್ನರಾಶಿಗಳು | Fractions in Disguise (Percentages, Commercial Math) |
| **Part 2** | **Ch 9** | ಬೋಧಾಯನ ಪೈಥಾಗೊರಸ್ ಪ್ರಮೇಯ | Baudhayana-Pythagoras Theorem |
| **Part 2** | **Ch 10** | ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-2 | Proportional Reasoning - 2 (Speed, Time, Compound Interest) |
| **Part 2** | **Ch 11** | ಜ್ಯಾಮಿತೀಯ ವಿಷಯಗಳು... | Geometric Concepts & Fractals (Symmetry, Circles) |
| **Part 2** | **Ch 12** | ಚುಕ್ಕೆಗಳು ಮತ್ತು ರೇಖೆಗಳು | Stories through Dots and Lines (Coordinates & Statistics) |
| **Part 2** | **Ch 13** | ಬೀಜಗಣಿತ ಆಟ | Algebra Play (Linear Equations in One Variable) |
| **Part 2** | **Ch 14** | ವಿಸ್ತೀರ್ಣ | Mensuration & Area (Polygons, Trapeziums, Circles, Pi) |

---

## 💡 Development & Coding Guidelines

1. **Text Encoding**: Textbook PDFs use legacy Nudi/ASCII glyph mappings. Always run text through `kannada_converter.KannadaConverter` and `PDFProcessor.clean_kannada_text()` before string matching or processing.
2. **Synchronized Outputs**: Any changes to extraction algorithms or vocabulary datasets must update `target/stem_keywords_chapterwise.json`, `target/stem_keywords_chapterwise.csv`, `target/stem_keywords_chapterwise.md`, `target/stem_flashcards.json`, `target/index.html`, and `./index.html`.
3. **Interactive Web App**: Keep the HTML app (`src/web/index.html`) standalone, responsive, and kid-friendly with Text-to-Speech audio aids, 3D flashcards, quiz games, and live search.
4. **Test-Driven Maintenance**: Ensure all pytest test cases in `src/tests/test_extraction.py` pass after any changes.
