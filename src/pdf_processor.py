"""
PDF Processor Module
Handles multi-book PDF text extraction, legacy font (Nudi/Baraha) to Unicode Kannada conversion,
text cleaning, and chapter segmentation for both Part 1 and Part 2.
"""

import os
import re
from typing import List, Dict, Any, Optional
import pymupdf
from kannada_converter import KannadaConverter


# Registry of known textbook outlines
TEXTBOOK_REGISTRY = {
    "8th-Kannada-Maths-Part-1.pdf": {
        "book_title": "Grade 8 Mathematics Part 1 (Kannada Medium)",
        "part": 1,
        "chapters": [
            {
                "chapter_num": 1,
                "title_kn": "ವರ್ಗ ಮತ್ತು ಘನ",
                "title_en": "Squares and Cubes",
                "start_page": 19,
                "end_page": 38,
                "description": "Square numbers, cube numbers, square roots, cube roots, Pythagorean triplets, and patterns."
            },
            {
                "chapter_num": 2,
                "title_kn": "ಘಾತಾಂಕಗಳ ಆಟ",
                "title_en": "Playing with Exponents and Powers",
                "start_page": 39,
                "end_page": 69,
                "description": "Exponents, powers, laws of exponents, negative exponents, standard scientific notation."
            },
            {
                "chapter_num": 3,
                "title_kn": "ಸಂಖ್ಯೆಗಳ ಕಥೆ",
                "title_en": "The Story of Numbers",
                "start_page": 70,
                "end_page": 103,
                "description": "History of numeral systems, place value, base systems (base 10, base 60), zero, abacus."
            },
            {
                "chapter_num": 4,
                "title_kn": "ಚತುರ್ಭುಜಗಳು",
                "title_en": "Quadrilaterals",
                "start_page": 104,
                "end_page": 134,
                "description": "Polygons, quadrilaterals, rectangles, squares, parallelograms, rhombuses, kites, trapeziums, angle properties."
            },
            {
                "chapter_num": 5,
                "title_kn": "ಸಂಖ್ಯೆಗಳ ಆಟ",
                "title_en": "Playing with Numbers",
                "start_page": 135,
                "end_page": 160,
                "description": "Multiples, factors, divisibility tests (2,3,4,5,6,8,9,10,11), cryptarithms, number puzzles."
            },
            {
                "chapter_num": 6,
                "title_kn": "ನಾವು ವಿಭಜಿಸುತ್ತೇವೆ ಆದರೆ ಅವು ಗುಣಿಸಲ್ಪಡುತ್ತವೆ",
                "title_en": "Factors, Multiples and Algebraic Expressions",
                "start_page": 161,
                "end_page": 184,
                "description": "Algebraic expressions, distributive law, polynomial multiplication, common factors, factoring."
            },
            {
                "chapter_num": 7,
                "title_kn": "ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-1",
                "title_en": "Proportional Reasoning - 1",
                "start_page": 185,
                "end_page": 208,
                "description": "Ratios, simplest form, direct and inverse proportion, sharing in ratios, scale factors, unit conversions."
            }
        ]
    },
    "8th Kannada Maths Part 2 2026-27.pdf": {
        "book_title": "Grade 8 Mathematics Part 2 (Kannada Medium)",
        "part": 2,
        "chapters": [
            {
                "chapter_num": 8,
                "title_kn": "ವೇಷಧಾರಿ ಭಿನ್ನರಾಶಿಗಳು",
                "title_en": "Fractions in Disguise (Percentages & Commercial Math)",
                "start_page": 3,
                "end_page": 41,
                "description": "Fractions to percentages, percentage increase/decrease, profit and loss, discount, and simple interest."
            },
            {
                "chapter_num": 9,
                "title_kn": "ಬೋಧಾಯನ ಪೈಥಾಗೊರಸ್ ಪ್ರಮೇಯ",
                "title_en": "Baudhayana-Pythagoras Theorem",
                "start_page": 42,
                "end_page": 66,
                "description": "Right-angled triangles, squares on the hypotenuse and legs, geometric proofs, and Pythagorean triples."
            },
            {
                "chapter_num": 10,
                "title_kn": "ಸಮಾನುಪಾತತೆಯ ತಾರ್ಕಿಕತೆ-2",
                "title_en": "Proportional Reasoning - 2",
                "start_page": 67,
                "end_page": 84,
                "description": "Compound proportions, inverse variation, speed-distance-time relationships, work-time problems, and compound interest."
            },
            {
                "chapter_num": 11,
                "title_kn": "ಕೆಲವು ಜ್ಯಾಮಿತೀಯ ವಿಷಯಗಳನ್ನು ಅನ್ವೇಷಿಸುವುದು",
                "title_en": "Exploring Geometric Concepts & Fractals",
                "start_page": 85,
                "end_page": 121,
                "description": "Fractals, self-similarity, reflection and rotational symmetry, circle properties (radius, diameter, chords), and constructions."
            },
            {
                "chapter_num": 12,
                "title_kn": "ಚುಕ್ಕೆಗಳು ಮತ್ತು ರೇಖೆಗಳ ಮೂಲಕ ಕಥೆಗಳು",
                "title_en": "Stories through Dots and Lines (Coordinates & Statistics)",
                "start_page": 122,
                "end_page": 157,
                "description": "Cartesian coordinate plane, plotting points (x, y), line graphs, reading graphs, central tendency (mean, median, mode)."
            },
            {
                "chapter_num": 13,
                "title_kn": "ಬೀಜಗಣಿತ ಆಟ",
                "title_en": "Algebra Play (Linear Equations)",
                "start_page": 158,
                "end_page": 172,
                "description": "Linear equations in one variable, transposing terms, balancing equations, and solving word problems algebraically."
            },
            {
                "chapter_num": 14,
                "title_kn": "ವಿಸ್ತೀರ್ಣ",
                "title_en": "Mensuration & Area",
                "start_page": 173,
                "end_page": 208,
                "description": "Area and perimeter of triangles, quadrilaterals, trapeziums, rhombuses, general polygons, circles, and surface area."
            }
        ]
    }
}


class PDFProcessor:
    """
    Extracts and normalizes text from Kannada textbook PDFs.
    """

    def __init__(self, pdf_path: str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")
        self.pdf_path = pdf_path
        self.doc = pymupdf.open(pdf_path)
        self.converter = KannadaConverter()
        self.num_pages = len(self.doc)
        self.filename = os.path.basename(pdf_path)

    def extract_page_raw(self, page_num: int) -> str:
        if page_num < 1 or page_num > self.num_pages:
            raise ValueError(f"Page {page_num} out of bounds (1..{self.num_pages})")
        page = self.doc[page_num - 1]
        return page.get_text()

    def clean_kannada_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"@KTBS\s*NOT TO BE REPUBLISHED", "", text, flags=re.IGNORECASE)
        text = re.sub(r"ಓಔಖಿ\s*ಖಿಔ\s*ಃಇ\s*ಖಇPUಃಐISಊಇಆ", "", text)
        text = re.sub(r"NOT TO BE REPUBLISHED", "", text, flags=re.IGNORECASE)
        text = re.sub(r"[ 	]+", " ", text)
        text = text.replace("¯ï", "ಲ್")
        text = text.replace("viï", "ವ್")
        text = text.replace("mÁUÀ¯ï", "ಟಾಗಲ್")

        lines = [line.strip() for line in text.split("\n")]
        cleaned_lines = [line for line in lines if line]
        return "\n".join(cleaned_lines)

    def extract_page_unicode(self, page_num: int) -> str:
        raw_text = self.extract_page_raw(page_num)
        try:
            unicode_text = self.converter.convert_ascii_to_unicode(raw_text)
        except Exception:
            unicode_text = raw_text
        return self.clean_kannada_text(unicode_text)

    def get_table_of_contents(self) -> List[Dict[str, Any]]:
        # Check if filename is in registry
        for reg_key, reg_info in TEXTBOOK_REGISTRY.items():
            if reg_key.lower().replace(' ', '').replace('-', '') in self.filename.lower().replace(' ', '').replace('-', ''):
                return reg_info["chapters"]
        # Fallback to Part 1 if not matched
        return TEXTBOOK_REGISTRY["8th-Kannada-Maths-Part-1.pdf"]["chapters"]

    def extract_chapter_text(self, chapter: Dict[str, Any]) -> Dict[str, Any]:
        start = chapter["start_page"]
        end = chapter["end_page"]
        pages_content = []
        full_text_chunks = []

        for p in range(start, min(end + 1, self.num_pages + 1)):
            page_text = self.extract_page_unicode(p)
            pages_content.append({
                "page_num": p,
                "text": page_text
            })
            full_text_chunks.append(page_text)

        full_text = "\n\n".join(full_text_chunks)
        return {
            "chapter_num": chapter["chapter_num"],
            "title_kn": chapter["title_kn"],
            "title_en": chapter["title_en"],
            "start_page": start,
            "end_page": end,
            "description": chapter.get("description", ""),
            "full_text": full_text,
            "pages": pages_content
        }

    def extract_all_chapters(self) -> List[Dict[str, Any]]:
        chapters = self.get_table_of_contents()
        results = []
        for ch in chapters:
            ch_data = self.extract_chapter_text(ch)
            results.append(ch_data)
        return results

    def close(self):
        self.doc.close()
