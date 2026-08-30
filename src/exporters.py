"""
Exporters Module
Writes extracted STEM keywords into multiple target formats:
JSON, CSV, Markdown study guide, flashcards deck, and quiz dataset.
"""

import os
import json
import csv
from typing import Dict, Any, List


class STEMExporter:
    """
    Exports structured STEM extraction results into target directory formats.
    """

    def __init__(self, target_dir: str = "/Users/vishwa/Dev/language-bridge-course/target"):
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

    def export_json(self, data: Dict[str, Any], filename: str = "stem_keywords_chapterwise.json") -> str:
        """
        Exports data to a formatted JSON file.
        """
        out_path = os.path.join(self.target_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return out_path

    def export_csv(self, data: Dict[str, Any], filename: str = "stem_keywords_chapterwise.csv") -> str:
        """
        Exports flat keyword rows to a CSV file.
        """
        out_path = os.path.join(self.target_dir, filename)
        fieldnames = [
            "Chapter_Number",
            "Chapter_Title_KN",
            "Chapter_Title_EN",
            "Page_Range",
            "Kannada_Term",
            "English_Term",
            "Transliteration",
            "Category",
            "Importance_Level",
            "Frequency_in_Chapter",
            "Kannada_Definition",
            "English_Definition",
            "Example_KN",
            "Example_EN",
            "Mnemonic_or_Tip"
        ]

        with open(out_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ch in data.get("chapters", []):
                ch_num = ch["chapter_num"]
                ch_kn = ch["chapter_title_kn"]
                ch_en = ch["chapter_title_en"]
                pages = f"pp. {ch['start_page']}-{ch['end_page']}"

                for kw in ch.get("keywords", []):
                    writer.writerow({
                        "Chapter_Number": ch_num,
                        "Chapter_Title_KN": ch_kn,
                        "Chapter_Title_EN": ch_en,
                        "Page_Range": pages,
                        "Kannada_Term": kw["kannada_term"],
                        "English_Term": kw["english_term"],
                        "Transliteration": kw["transliteration"],
                        "Category": kw["category"],
                        "Importance_Level": kw.get("importance_level", "Core"),
                        "Frequency_in_Chapter": kw.get("frequency_in_chapter", 0),
                        "Kannada_Definition": kw["definition_kn"],
                        "English_Definition": kw["definition_en"],
                        "Example_KN": kw["example_kn"],
                        "Example_EN": kw["example_en"],
                        "Mnemonic_or_Tip": kw.get("mnemonic_or_tip", "")
                    })

        return out_path

    def export_markdown(self, data: Dict[str, Any], filename: str = "stem_keywords_chapterwise.md") -> str:
        """
        Generates a rich, student-friendly Markdown study guide with tables and examples.
        """
        out_path = os.path.join(self.target_dir, filename)
        lines = []

        lines.append("# 🌟 Kannada to English STEM Bridge Course Vocabulary Guide")
        lines.append(f"**Textbook**: {data.get('textbook_name', 'Grade 8 Mathematics')}")
        lines.append(f"**Total Chapters**: {data.get('total_chapters', 7)}")
        lines.append(f"**Total Key Terms Extracted**: {data.get('total_keywords_extracted', 0)}")
        lines.append("\n---\n")

        # Table of Contents
        lines.append("## 📑 Quick Navigation (Chapters)")
        for ch in data.get("chapters", []):
            anchor = f"chapter-{ch['chapter_num']}-{ch['chapter_title_en'].lower().replace(' ', '-').replace(',', '')}"
            lines.append(f"- [Chapter {ch['chapter_num']}: {ch['chapter_title_kn']} ({ch['chapter_title_en']})](#{anchor}) — *{ch['total_keywords_count']} key terms*")
        lines.append("\n---\n")

        # Chapter sections
        for ch in data.get("chapters", []):
            ch_num = ch["chapter_num"]
            ch_kn = ch["chapter_title_kn"]
            ch_en = ch["chapter_title_en"]
            anchor = f"chapter-{ch_num}-{ch_en.lower().replace(' ', '-').replace(',', '')}"

            lines.append(f"<a id='{anchor}'></a>")
            lines.append(f"## 📘 Chapter {ch_num}: {ch_kn} / *{ch_en}*")
            lines.append(f"📍 **Textbook Pages**: {ch['start_page']} – {ch['end_page']} | **Focus Area**: {ch['description']}")
            lines.append("")

            # Summary Table
            lines.append("| Kannada Term (ಕನ್ನಡ) | Transliteration | English STEM Term | Category | Importance |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for kw in ch.get("keywords", []):
                lines.append(f"| **{kw['kannada_term']}** | *{kw['transliteration']}* | **{kw['english_term']}** | `{kw['category']}` | {kw['importance_level']} |")
            lines.append("")

            # Deep dive for each term
            lines.append(f"### 🔍 Detailed Concept Cards for Chapter {ch_num}")
            for idx, kw in enumerate(ch.get("keywords", []), 1):
                lines.append(f"#### {idx}. {kw['kannada_term']} ➔ **{kw['english_term']}** (*{kw['transliteration']}*)")
                lines.append(f"- 🏷️ **Category**: `{kw['category']}` | **Chapter Frequency**: {kw['frequency_in_chapter']} occurrences")
                lines.append(f"- 📖 **ಕನ್ನಡ ವಿವರಣೆ (Kannada)**: {kw['definition_kn']}")
                lines.append(f"- 📖 **English Definition**: {kw['definition_en']}")
                lines.append(f"- 💡 **ಉದಾಹರಣೆ (Example)**: `{kw['example_kn']}` ➔ `{kw['example_en']}`")
                if kw.get("mnemonic_or_tip"):
                    lines.append(f"- 🧠 **Bridge Memory Tip**: *{kw['mnemonic_or_tip']}*")
                if kw.get("textbook_excerpts") and kw["textbook_excerpts"][0] != kw["example_kn"]:
                    lines.append(f"- 📜 **Textbook Excerpt**: *\"{kw['textbook_excerpts'][0]}\"*")
                lines.append("")

            lines.append("\n---\n")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return out_path

    def export_flashcards(self, data: Dict[str, Any], filename: str = "stem_flashcards.json") -> str:
        """
        Exports terms formatted as interactive flashcard items for study apps.
        """
        out_path = os.path.join(self.target_dir, filename)
        cards = []
        card_id = 1

        for ch in data.get("chapters", []):
            for kw in ch.get("keywords", []):
                cards.append({
                    "id": card_id,
                    "chapter_num": ch["chapter_num"],
                    "chapter_title": ch["chapter_title_en"],
                    "front_kannada": kw["kannada_term"],
                    "transliteration": kw["transliteration"],
                    "back_english": kw["english_term"],
                    "category": kw["category"],
                    "definition_kn": kw["definition_kn"],
                    "definition_en": kw["definition_en"],
                    "example_en": kw["example_en"],
                    "hint": kw.get("mnemonic_or_tip", "")
                })
                card_id += 1

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)

        return out_path

    def export_all(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Exports all formats and returns a dictionary of output paths.
        """
        json_path = self.export_json(data)
        csv_path = self.export_csv(data)
        md_path = self.export_markdown(data)
        flashcards_path = self.export_flashcards(data)

        return {
            "json": json_path,
            "csv": csv_path,
            "markdown": md_path,
            "flashcards": flashcards_path
        }
