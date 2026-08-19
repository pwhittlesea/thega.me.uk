#!/usr/bin/env python3
"""Pre-commit hook: check for mandatory fields in markdown front matter."""

import argparse
import frontmatter
import re
import sys


REQUIRED_FIELDS = ["date", "title"]
DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?\s*(?:Z|[+-]\d{2}:?\d{2}|[+-]\d{4})$"
)
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def get_frontmatter(filepath: str) -> dict:
    post = frontmatter.load(filepath)
    if not post or not post.metadata:
        print(f"File has no frontmatter: {filepath}")
        return None

    return post.metadata


def validate_date(filepath: str, metadata: dict) -> bool:
    """Validate a single markdown file."""
    date_value = metadata.get("date")
    if not date_value:
        return True  # No date field

    date_str = str(date_value).strip()

    pattern = DATE_PATTERN
    if filepath.startswith("content/posts"):
        pattern = DATETIME_PATTERN

    if not pattern.match(date_str):
        print(f"Invalid date format: '{date_str}'")
        return False

    return True


def validate_mandatory_fields(metadata: dict) -> bool:
    """Check that a markdown file has all required fields in its front matter."""
    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] is None or metadata[field] == "":
            print(f"Missing required field: '{field}'")
            return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Process Markdown files to ensure they have the correct frontmatter"
    )
    parser.add_argument("files", nargs="+", help="Markdown files to process")

    args = parser.parse_args()

    for filepath_str in args.files:
        metadata = get_frontmatter(filepath_str)
        if (
            not metadata
            or not validate_mandatory_fields(metadata)
            or not validate_date(filepath_str, metadata)
        ):
            print(f"Failure for file {filepath_str}")
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
