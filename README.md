# 🎓 Kannada to English STEM Bridge Course Engine

An interactive, AI-powered bridge course platform that extracts and maps native Kannada STEM terminologies from school textbooks into English concepts for students transitioning to English-medium STEM education.

---

## 📁 Project Directory Structure

```text
language-bridge-course/
├── resources/                     # 📚 Input Kannada Textbooks (Parts 1 & 2)
│   ├── 8th-Kannada-Maths-Part-1.pdf
│   └── 8th Kannada Maths Part 2 2026-27.pdf
├── src/                           # 💻 Code, extraction agent, and web generator
│   ├── __init__.py
│   ├── pdf_processor.py           # Multi-book text extraction & Nudi ASCII -> Unicode converter
│   ├── stem_dictionary.py        # Bilingual STEM domain knowledge base (14 chapters)
│   ├── agent.py                   # Chapter-wise STEM keyword extraction agent
│   ├── exporters.py               # JSON, CSV, Markdown, and Flashcards exporters
│   ├── generate_web_app.py        # Standalone interactive HTML website generator
│   ├── pipeline.py                # Pipeline coordinator
│   ├── main.py                    # CLI entrypoint
│   ├── app.py                     # Streamlit interactive learning web app
│   └── tests/                     # Unit and integration test suite
│       └── test_extraction.py
└── target/                        # 🎯 Output files & generated artifacts
    ├── index.html                      # Interactive HTML teaching web platform
    ├── stem_keywords_chapterwise.json  # Complete structured JSON dataset (14 chapters)
    ├── stem_keywords_chapterwise.csv   # Spreadsheet-ready tabular data
    ├── stem_keywords_chapterwise.md    # Formatted Markdown vocabulary guide
    └── stem_flashcards.json            # Flashcard deck for study games
```

---

## 🚀 Getting Started

### 1. Ingest All Textbooks & Extract Keywords
To run the extraction agent and regenerate all chapter-wise datasets + HTML website:

```bash
python3 src/main.py
```

### 2. Open the Interactive Teaching HTML Website
```bash
open target/index.html
```

Or serve via local HTTP server:
```bash
python3 -m http.server 8000 --directory target
```

### 3. Run the Streamlit Learning App
```bash
streamlit run src/app.py
```

### 4. Run Automated Tests
```bash
python3 -m pytest src/tests/test_extraction.py -v
```

---

## 📊 Complete Grade 8 Curriculum (14 Chapters • 150 Keywords)

| Book | Chapter | Kannada Title | English Title | Key STEM Terms Extracted |
| :--- | :--- | :--- | :--- | :--- |
| **Part 1** | **Ch 1** | ವರ್ಗ ಮತ್ತು ಘನ | Squares and Cubes | Square, Cube, Square Root, Cube Root, Prime Factorization, Pythagorean Triplets |
| **Part 1** | **Ch 2** | ಘಾತಾಂಕಗಳ ಆಟ | Playing with Exponents | Base, Exponent, Laws of Exponents, Negative Exponents, Scientific Notation |
| **Part 1** | **Ch 3** | ಸಂಖ್ಯೆಗಳ ಕಥೆ | The Story of Numbers | Numeral Systems, Place Value, Face Value, Zero, Abacus, Decimal System |
| **Part 1** | **Ch 4** | ಚತುರ್ಭುಜಗಳು | Quadrilaterals | Quadrilateral, Rectangle, Square, Parallelogram, Rhombus, Trapezium, Kite |
| **Part 1** | **Ch 5** | ಸಂಖ್ಯೆಗಳ ಆಟ | Playing with Numbers | Factors, Multiples, Divisibility Rules, Consecutive Numbers, Triangular Numbers |
| **Part 1** | **Ch 6** | ನಾವು ವಿಭಜಿಸುತ್ತೇವೆ... | Factors & Algebra | Algebra, Expressions, Variables, Constants, Distributive Law, Common Factors |
| **Part 1** | **Ch 7** | ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-1 | Proportional Reasoning - 1 | Ratios, Proportion, Direct Proportion, Inverse Proportion, Unitary Method |
| **Part 2** | **Ch 8** | ವೇಷಧಾರಿ ಭಿನ್ನರಾಶಿಗಳು | Fractions in Disguise | Percentage, Cost Price, Selling Price, Profit, Loss, Discount, Simple Interest |
| **Part 2** | **Ch 9** | ಬೋಧಾಯನ ಪೈಥಾಗೊರಸ್ ಪ್ರಮೇಯ | Pythagoras Theorem | Theorem, Baudhayana-Pythagoras Theorem, Right Triangle, Hypotenuse, Altitude |
| **Part 2** | **Ch 10** | ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-2 | Proportional Reasoning - 2 | Compound Proportion, Speed, Distance, Time, Average Speed, Compound Interest |
| **Part 2** | **Ch 11** | ಜ್ಯಾಮಿತೀಯ ವಿಷಯಗಳು... | Geometry & Fractals | Fractals, Self-Similarity, Symmetry, Circles, Radius, Diameter, Circumference |
| **Part 2** | **Ch 12** | ಚುಕ್ಕೆಗಳು ಮತ್ತು ರೇಖೆಗಳು | Coordinates & Statistics | Coordinate Plane (x, y), Origin, Line Graph, Mean, Median, Data Handling |
| **Part 2** | **Ch 13** | ಬೀಜಗಣಿತ ಆಟ | Algebra Play | Linear Equations in One Variable, Transposition, Balancing, Equation Roots |
| **Part 2** | **Ch 14** | ವಿಸ್ತೀರ್ಣ | Mensuration & Area | Area, Perimeter, Area of Trapezium, Rhombus, Circle Area, Pi (π), Units |

---

## 🎮 Interactive App Features
- 📖 **Chapter Explorer**: Bilingual glossary with Kannada text, phonetic pronunciation, English definitions, and usage examples.
- 🎴 **Interactive Flashcards**: Flip cards with memory hooks and tips to test recall.
- 🎮 **STEM Quiz Challenge**: Gamified multiple-choice quizzes with instant feedback and score tracking.
- 🧩 **Term Matcher Game**: Visual matching between native Kannada words and English terms.
- 🔍 **Bilingual Search**: Instant cross-language search across all mathematical concepts.
