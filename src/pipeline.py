"""
Pipeline Module
Coordinates textbook ingestion across all books in resources/, agentic keyword extraction,
target file exports, and interactive HTML teaching web app generation.
"""

import os
import sys
import glob
import time
from typing import Dict, Any, Optional, List
from src.agent import STEMExtractionAgent
from src.exporters import STEMExporter
from src.generate_web_app import generate_html_app


def run_pipeline(
    resources_dir: str = "/Users/vishwa/Dev/language-bridge-course/resources",
    target_dir: str = "/Users/vishwa/Dev/language-bridge-course/target"
) -> Dict[str, Any]:
    """
    Runs the complete extraction, export, and web generation pipeline for all textbooks in resources/.
    """
    print("=" * 75)
    print("🚀 Starting STEM Keyword Extraction Pipeline for Kannada Bridge Course")
    print(f"📂 Resources Directory: {resources_dir}")
    print(f"📂 Target Directory: {target_dir}")
    print("=" * 75)

    start_time = time.time()

    if os.path.isfile(resources_dir):
        pdf_paths = [resources_dir]
    else:
        pdf_paths = sorted(glob.glob(os.path.join(resources_dir, "*.pdf")))

    if not pdf_paths:
        raise FileNotFoundError(f"No PDF textbooks found in: {resources_dir}")

    print(f"Found {len(pdf_paths)} textbook(s):")
    for p in pdf_paths:
        print(f"  📖 {os.path.basename(p)} ({os.path.getsize(p):,} bytes)")

    # 1. Initialize Agent
    print("\n[Step 1/4] Initializing Multi-Book STEM Extraction Agent...")
    agent = STEMExtractionAgent(pdf_paths)

    # 2. Run extraction
    print("[Step 2/4] Extracting and classifying chapter-wise STEM keywords...")
    results = agent.run_full_extraction()
    agent.close()

    print(f"  ✓ Successfully processed {results['total_chapters']} chapters across {len(pdf_paths)} books.")
    print(f"  ✓ Extracted {results['total_keywords_extracted']} total high-yield STEM keywords.")

    for ch in results["chapters"]:
        print(f"    - Chapter {ch['chapter_num']:2d}: {ch['chapter_title_kn']} ({ch['chapter_title_en']}) -> {ch['total_keywords_count']} terms [{ch.get('source_book', '')}]")

    # 3. Export to target
    print("\n[Step 3/4] Writing outputs to target folder in multiple formats...")
    exporter = STEMExporter(target_dir)
    exported_files = exporter.export_all(results)

    for fmt, path in exported_files.items():
        print(f"  ✓ Saved {fmt.upper()}: {path} ({os.path.getsize(path):,} bytes)")

    # 4. Generate Interactive HTML Teaching App
    print("\n[Step 4/4] Generating Updated Interactive HTML Teaching Web Application...")
    json_path = exported_files["json"]
    web_paths = [
        "/Users/vishwa/Dev/language-bridge-course/index.html",
        os.path.join(target_dir, "index.html"),
        "/Users/vishwa/Dev/language-bridge-course/src/web/index.html"
    ]
    generate_html_app(json_path=json_path, output_html_paths=web_paths)

    elapsed = time.time() - start_time
    print("\n" + "=" * 75)
    print(f"✨ Extraction, Export & HTML Website Build Complete in {elapsed:.2f} seconds!")
    print("=" * 75)

    return {
        "results": results,
        "exported_files": exported_files,
        "web_paths": web_paths
    }


if __name__ == "__main__":
    res = sys.argv[1] if len(sys.argv) > 1 else "/Users/vishwa/Dev/language-bridge-course/resources"
    target = sys.argv[2] if len(sys.argv) > 2 else "/Users/vishwa/Dev/language-bridge-course/target"
    run_pipeline(res, target)
