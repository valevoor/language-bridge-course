"""
STEM Keyword Extraction Agent
Intelligently scans textbook chapters from single or multiple textbooks,
detects STEM terminologies, extracts contextual definitions, calculates frequencies,
and organizes chapter-wise datasets across Part 1 and Part 2.
"""

import os
import glob
import re
from typing import List, Dict, Any, Optional
from src.pdf_processor import PDFProcessor, TEXTBOOK_REGISTRY
from src.stem_dictionary import STEM_GLOSSARY, get_terms_for_chapter, get_all_terms


class STEMExtractionAgent:
    """
    Intelligent Agent for extracting and organizing Kannada-English STEM keywords
    from single or multiple textbook PDFs.
    """

    def __init__(self, pdf_paths: Any):
        if isinstance(pdf_paths, str):
            if os.path.isdir(pdf_paths):
                self.pdf_paths = sorted(glob.glob(os.path.join(pdf_paths, "*.pdf")))
            else:
                self.pdf_paths = [pdf_paths]
        else:
            self.pdf_paths = list(pdf_paths)

        self.processors = [PDFProcessor(p) for p in self.pdf_paths]
        self.glossary = STEM_GLOSSARY

    def extract_context_sentences(self, text: str, term: str, max_sentences: int = 2) -> List[str]:
        if not text or not term:
            return []

        raw_sentences = re.split(r'[.।\n?!]+', text)
        matched_sentences = []
        term_clean = term.split('/')[0].strip()

        for s in raw_sentences:
            s_clean = s.strip()
            if len(s_clean) < 15 or len(s_clean) > 250:
                continue
            if term_clean in s_clean:
                clean_stmt = re.sub(r'\s+', ' ', s_clean)
                if clean_stmt not in matched_sentences:
                    matched_sentences.append(clean_stmt)
                if len(matched_sentences) >= max_sentences:
                    break

        return matched_sentences

    def count_term_occurrences(self, text: str, term_entry: Dict[str, Any]) -> int:
        terms_to_search = [term_entry["kannada_term"]]
        if "/" in term_entry["kannada_term"]:
            terms_to_search.extend([t.strip() for t in term_entry["kannada_term"].split("/")])
        terms_to_search.extend(term_entry.get("aliases_kn", []))

        total_count = 0
        for t in set(terms_to_search):
            if t:
                total_count += text.count(t)

        return total_count

    def process_chapter_with_processor(self, processor: PDFProcessor, chapter_info: Dict[str, Any]) -> Dict[str, Any]:
        ch_num = chapter_info["chapter_num"]
        ch_text_data = processor.extract_chapter_text(chapter_info)
        full_text = ch_text_data["full_text"]

        primary_terms = get_terms_for_chapter(ch_num)
        all_terms = get_all_terms()
        candidate_terms = list(primary_terms)
        for term in all_terms:
            if term not in candidate_terms:
                count = self.count_term_occurrences(full_text, term)
                if count >= 4:
                    candidate_terms.append(term)

        extracted_keywords = []
        for term in candidate_terms:
            freq = self.count_term_occurrences(full_text, term)
            excerpts = self.extract_context_sentences(full_text, term["kannada_term"], max_sentences=2)
            
            if freq >= 10 or term["primary_chapter"] == ch_num:
                importance = "Core / Essential"
            elif freq >= 4:
                importance = "Important"
            else:
                importance = "Supplementary"

            keyword_data = {
                "kannada_term": term["kannada_term"],
                "english_term": term["english_term"],
                "transliteration": term["transliteration"],
                "category": term["category"],
                "frequency_in_chapter": freq,
                "importance_level": importance,
                "definition_kn": term["definition_kn"],
                "definition_en": term["definition_en"],
                "example_kn": term["example_kn"],
                "example_en": term["example_en"],
                "mnemonic_or_tip": term.get("mnemonic_or_tip", ""),
                "textbook_excerpts": excerpts if excerpts else [term["example_kn"]]
            }
            extracted_keywords.append(keyword_data)

        extracted_keywords.sort(
            key=lambda k: (0 if k["importance_level"] == "Core / Essential" else (1 if k["importance_level"] == "Important" else 2), -k["frequency_in_chapter"])
        )

        return {
            "chapter_num": ch_num,
            "chapter_title_kn": chapter_info["title_kn"],
            "chapter_title_en": chapter_info["title_en"],
            "start_page": chapter_info["start_page"],
            "end_page": chapter_info["end_page"],
            "description": chapter_info.get("description", ""),
            "source_book": processor.filename,
            "total_keywords_count": len(extracted_keywords),
            "keywords": extracted_keywords
        }

    def run_full_extraction(self) -> Dict[str, Any]:
        all_chapter_results = []
        total_terms_extracted = 0

        for proc in self.processors:
            toc = proc.get_table_of_contents()
            for ch in toc:
                processed = self.process_chapter_with_processor(proc, ch)
                all_chapter_results.append(processed)
                total_terms_extracted += processed["total_keywords_count"]

        # Sort all chapters by chapter number
        all_chapter_results.sort(key=lambda c: c["chapter_num"])

        summary = {
            "textbook_name": "Grade 8 Mathematics (Complete Parts 1 & 2 - Kannada Medium)",
            "source_files": [os.path.basename(p) for p in self.pdf_paths],
            "total_chapters": len(all_chapter_results),
            "total_keywords_extracted": total_terms_extracted,
            "chapters": all_chapter_results
        }
        return summary

    def close(self):
        for proc in self.processors:
            proc.close()
