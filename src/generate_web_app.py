"""
HTML Teaching Website Generator.
Generates an interactive, standalone single-page HTML5/JS application
for learning Kannada-English STEM keywords with 3D Flashcards, Quiz Arena,
Term Matcher, and Bilingual Search across Part 1 and Part 2 textbooks.
"""

import os
import re
import json

def generate_html_app(
    json_path: str = "/Users/vishwa/Dev/language-bridge-course/target/stem_keywords_chapterwise.json",
    template_path: str = "/Users/vishwa/Dev/language-bridge-course/src/web/index.html",
    output_html_paths: list = None
):
    if output_html_paths is None:
        output_html_paths = [
            "/Users/vishwa/Dev/language-bridge-course/index.html",
            "/Users/vishwa/Dev/language-bridge-course/src/web/index.html",
            "/Users/vishwa/Dev/language-bridge-course/target/index.html"
        ]

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON dataset not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    json_str = json.dumps(data, ensure_ascii=False)
    total_chs = data.get("total_chapters", 14)
    total_kws = data.get("total_keywords_extracted", 0)

    # Inject latest JSON
    new_html = re.sub(
        r'const STEM_DATA = .*?;\s*\n\s*// State Management',
        f'const STEM_DATA = {json_str};\n\n    // State Management',
        html,
        flags=re.DOTALL
    )

    for out_path in output_html_paths:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Generated updated HTML website at: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    generate_html_app()
