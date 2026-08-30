"""
Main CLI Entrypoint for the Interactive Kannada STEM Bridge Course Engine.
Supports extracting from single textbooks or all textbooks in resources/.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Kannada STEM Keyword Extraction Agent & Interactive Bridge Course Engine"
    )
    parser.add_argument(
        "--resources",
        type=str,
        default="/Users/vishwa/Dev/language-bridge-course/resources",
        help="Path to directory containing Kannada textbook PDFs or a single PDF file"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="/Users/vishwa/Dev/language-bridge-course/target",
        help="Directory to write output files"
    )

    args = parser.parse_args()
    run_pipeline(resources_dir=args.resources, target_dir=args.target)


if __name__ == "__main__":
    main()
