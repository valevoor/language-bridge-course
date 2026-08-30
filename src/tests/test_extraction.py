"""
Unit and Integration Tests for STEM Keyword Extraction Engine.
"""

import os
import json
import csv
import pytest
from src.pdf_processor import PDFProcessor
from src.stem_dictionary import STEM_GLOSSARY, get_terms_for_chapter, get_all_terms
from src.agent import STEMExtractionAgent
from src.exporters import STEMExporter
from src.generate_web_app import generate_html_app

PDF_PATH = "/Users/vishwa/Dev/language-bridge-course/resources/8th-Kannada-Maths-Part-1.pdf"
TARGET_DIR = "/Users/vishwa/Dev/language-bridge-course/target"


# ---------------------------------------------------------
# 1. Resource & File Existence Tests
# ---------------------------------------------------------
def test_pdf_exists():
    """Verifies that the target input PDF textbook exists in resources/."""
    assert os.path.exists(PDF_PATH), f"PDF file not found at {PDF_PATH}"


# ---------------------------------------------------------
# 2. PDF Processor & Encoding Conversion Tests
# ---------------------------------------------------------
def test_pdf_processor_page_count_and_toc():
    """Validates total pages (208) and extraction of all 7 chapter boundaries."""
    proc = PDFProcessor(PDF_PATH)
    assert proc.num_pages == 208
    toc = proc.get_table_of_contents()
    assert len(toc) == 7
    for i, ch in enumerate(toc, 1):
        assert ch["chapter_num"] == i
        assert ch["start_page"] < ch["end_page"]
    proc.close()


def test_pdf_unicode_conversion_and_cleaning():
    """Tests that Nudi ASCII encoded text converts to valid Kannada Unicode strings."""
    proc = PDFProcessor(PDF_PATH)
    p18_unicode = proc.extract_page_unicode(18)
    assert "ಪರಿವಿಡಿ" in p18_unicode or "ವರ್ಗ" in p18_unicode
    assert "NOT TO BE REPUBLISHED" not in p18_unicode
    proc.close()


def test_pdf_processor_page_out_of_bounds():
    """Tests out-of-bounds page handling."""
    proc = PDFProcessor(PDF_PATH)
    with pytest.raises(ValueError):
        proc.extract_page_raw(0)
    with pytest.raises(ValueError):
        proc.extract_page_raw(999)
    proc.close()


# ---------------------------------------------------------
# 3. Domain Knowledge & STEM Dictionary Tests
# ---------------------------------------------------------
def test_stem_dictionary_schema_and_completeness():
    """Checks that all STEM dictionary entries have mandatory bilingual fields."""
    terms = get_all_terms()
    assert len(terms) >= 30
    for t in terms:
        assert isinstance(t["kannada_term"], str) and len(t["kannada_term"]) > 0
        assert isinstance(t["english_term"], str) and len(t["english_term"]) > 0
        assert isinstance(t["transliteration"], str) and len(t["transliteration"]) > 0
        assert isinstance(t["primary_chapter"], int) and 1 <= t["primary_chapter"] <= 14
        assert isinstance(t["definition_kn"], str) and len(t["definition_kn"]) > 0
        assert isinstance(t["definition_en"], str) and len(t["definition_en"]) > 0
        assert "example_kn" in t
        assert "example_en" in t


def test_stem_dictionary_chapter_distribution():
    """Ensures each of the 7 chapters has primary STEM terms defined."""
    for ch_num in range(1, 15):
        ch_terms = get_terms_for_chapter(ch_num)
        assert len(ch_terms) > 0, f"Chapter {ch_num} has no assigned terms"


# ---------------------------------------------------------
# 4. Agent Extraction & Context Parsing Tests
# ---------------------------------------------------------
def test_agent_extraction_integration():
    """Runs full extraction agent and verifies chapter breakdown, keywords, and term frequencies."""
    agent = STEMExtractionAgent(PDF_PATH)
    results = agent.run_full_extraction()
    agent.close()

    assert results["total_chapters"] == 7
    assert results["total_keywords_extracted"] > 0
    assert len(results["chapters"]) == 7

    # Check Chapter 1 (Squares and Cubes)
    ch1 = results["chapters"][0]
    assert ch1["chapter_num"] == 1
    assert "ವರ್ಗ" in ch1["chapter_title_kn"]
    kn_terms_ch1 = [k["kannada_term"] for k in ch1["keywords"]]
    assert "ವರ್ಗ" in kn_terms_ch1
    assert "ಘನ" in kn_terms_ch1

    # Check Chapter 4 (Quadrilaterals)
    ch4 = results["chapters"][3]
    assert ch4["chapter_num"] == 4
    kn_terms_ch4 = [k["kannada_term"] for k in ch4["keywords"]]
    assert "ಚತುರ್ಭುಜ" in kn_terms_ch4
    assert "ಆಯತ" in kn_terms_ch4


def test_agent_context_sentence_extractor():
    """Tests the agent's ability to extract relevant context sentences around keywords."""
    agent = STEMExtractionAgent(PDF_PATH)
    sample_text = "ವರ್ಗ ಸಂಖ್ಯೆಗಳು ಗಣಿತದಲ್ಲಿ ಬಹಳ ಮುಖ್ಯ. ನಾವು 5 ರ ವರ್ಗವನ್ನು 25 ಎಂದು ಕರೆಯುತ್ತೇವೆ."
    sentences = agent.extract_context_sentences(sample_text, "ವರ್ಗ", max_sentences=2)
    assert len(sentences) > 0
    assert any("ವರ್ಗ" in s for s in sentences)
    agent.close()


# ---------------------------------------------------------
# 5. Multi-Format Exporters Tests (JSON, CSV, MD, Flashcards, HTML)
# ---------------------------------------------------------
def test_file_exporters_and_content_integrity(tmp_path):
    """Tests that exporter creates valid, non-empty JSON, CSV, Markdown, and Flashcards files."""
    exporter = STEMExporter(str(tmp_path))
    sample_data = {
        "textbook_name": "Test Textbook",
        "total_chapters": 1,
        "total_keywords_extracted": 2,
        "chapters": [
            {
                "chapter_num": 1,
                "chapter_title_kn": "ವರ್ಗ ಮತ್ತು ಘನ",
                "chapter_title_en": "Squares and Cubes",
                "start_page": 19,
                "end_page": 38,
                "description": "Square and cube numbers",
                "total_keywords_count": 2,
                "keywords": [
                    {
                        "kannada_term": "ವರ್ಗ",
                        "english_term": "Square",
                        "transliteration": "Varga",
                        "category": "Arithmetic & Powers",
                        "frequency_in_chapter": 15,
                        "importance_level": "Core / Essential",
                        "definition_kn": "ವರ್ಗ ವ್ಯಾಖ್ಯಾನ",
                        "definition_en": "Square definition",
                        "example_kn": "5² = 25",
                        "example_en": "5² = 25",
                        "mnemonic_or_tip": "Tip",
                        "textbook_excerpts": ["ಉದಾಹರಣೆ"]
                    },
                    {
                        "kannada_term": "ಘನ",
                        "english_term": "Cube",
                        "transliteration": "Ghana",
                        "category": "Arithmetic & Powers",
                        "frequency_in_chapter": 8,
                        "importance_level": "Core / Essential",
                        "definition_kn": "ಘನ ವ್ಯಾಖ್ಯಾನ",
                        "definition_en": "Cube definition",
                        "example_kn": "4³ = 64",
                        "example_en": "4³ = 64",
                        "mnemonic_or_tip": "Tip",
                        "textbook_excerpts": ["ಉದಾಹರಣೆ"]
                    }
                ]
            }
        ]
    }

    out = exporter.export_all(sample_data)
    
    assert os.path.exists(out["json"])
    assert os.path.exists(out["csv"])
    assert os.path.exists(out["markdown"])
    assert os.path.exists(out["flashcards"])

    with open(out["json"], "r", encoding="utf-8") as f:
        loaded_json = json.load(f)
        assert loaded_json["total_keywords_extracted"] == 2
        assert len(loaded_json["chapters"]) == 1

    with open(out["csv"], "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        assert len(reader) == 2
        assert reader[0]["Kannada_Term"] == "ವರ್ಗ"
        assert reader[0]["English_Term"] == "Square"

    with open(out["markdown"], "r", encoding="utf-8") as f:
        md_content = f.read()
        assert "# 🌟 Kannada to English STEM Bridge Course Vocabulary Guide" in md_content
        assert "Chapter 1: ವರ್ಗ ಮತ್ತು ಘನ" in md_content

    with open(out["flashcards"], "r", encoding="utf-8") as f:
        flashcards = json.load(f)
        assert len(flashcards) == 2
        assert flashcards[0]["front_kannada"] == "ವರ್ಗ"
        assert flashcards[0]["back_english"] == "Square"
