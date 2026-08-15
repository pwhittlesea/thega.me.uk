#!/usr/bin/env python3
"""
Pre-commit hook for processing images in the repository.

Removes all EXIF data except ICC color profiles and adds copyright information.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_git_user_name():
    """Get the configured git user name."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: Could not retrieve git user name", file=sys.stderr)
        return "Unknown"


def load_json_metadata(image_path: Path) -> dict | None:
    """Load metadata from accompanying JSON file if it exists."""
    json_path = image_path.with_suffix(".metadata.json")

    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read {json_path}: {e}", file=sys.stderr)
            return None

    return None


def build_metadata_fields(
    metadata: dict | None, current_year: int, git_name: str, verbose: bool = False
) -> list[str]:
    """Build complete exiftool command arguments with EXIF + IPTC + XMP metadata."""
    if metadata and "skip" in metadata:
        if verbose:
            print("  Skipped: true")
        return []

    if metadata and "author" in metadata and metadata["author"].get("name"):
        author_name = metadata["author"]["name"]
        license_title = metadata.get("licence", {}).get("title", "All Rights Reserved")
        license_url = metadata.get("licence", {}).get("url", "")
        source_url = metadata.get("source", "")
        year = metadata.get("year", current_year)
    else:
        author_name = git_name
        license_title = "CC BY-NC 4.0"
        license_url = "https://creativecommons.org/licenses/by-nc/4.0/"
        source_url = "https://thega.me.uk"
        year = current_year

    copyright_notice = f"© {year} {author_name} ({license_title})"
    if source_url:
        copyright_notice += f" [{source_url}]"

    if verbose:
        print(f"  Author: {author_name}")
        print(f"  License Title: {license_title}")
        print(f"  License URL: {license_url}")
        print(f"  Source URL: {source_url}")
        print(f"  Year: {year}")
        print(f"  Copyright Notice: {copyright_notice}")

    # Complete metadata field list (EXIF + IPTC + XMP)
    # Order matters: base fields first, then derived
    fields = [
        # EXIF fields (persist in all formats with EXIF support)
        f"-copyright={copyright_notice}",
        f"-copyrightnotice={copyright_notice}",
        f"-artist={author_name}",
        f"-credit={author_name}",
        # IPTC fields (persist in JPEG, TIFF; NOT in WebP)
        f"-IPTC:CopyrightNotice={copyright_notice}",
        f"-IPTC:Credit={author_name}",
        f"-IPTC:By-line={author_name}",
        f"-IPTC:Source={source_url}" if source_url else None,
        # XMP fields (persist in JPEG, PNG, WebP, TIFF)
        f"-XMP-dc:Rights={copyright_notice}",
        f"-XMP-dc:Creator={author_name}",
        f"-XMP-dc:Source={source_url}" if source_url else None,
        f"-XMP-cc:attributionName={author_name}",
        f"-XMP-cc:attributionURL={source_url}" if source_url else None,
        f"-XMP-cc:license={license_url}" if license_url else None,
    ]

    # Filter out None values
    return [f for f in fields if f]


def process_image(image_path: Path, metadata_fields: list[str]) -> bool:
    """Process a single image by removing EXIF data and adding complete metadata."""
    try:
        cmd = [
            "exiftool",
            "-q",
            "-all=",
            "--icc_profile:all",  # Preserve ICC profile
        ]

        # Add all metadata fields
        cmd.extend(metadata_fields)

        cmd.extend(["-overwrite_original", str(image_path)])

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            return True
        else:
            print(f"  Failed: {result.stderr}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Process images for pre-commit: strip EXIF, add copyright."
    )
    parser.add_argument("files", nargs="+", help="Image files to process")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    current_year = datetime.now().year
    git_user_name = get_git_user_name()

    processed = 0
    failed = 0

    for file_arg in args.files:
        image_path = Path(file_arg)

        if not image_path.exists():
            print(f"Warning: File not found: {image_path}", file=sys.stderr)
            continue

        if args.verbose:
            print(f"Processing: {image_path}")

        # Load metadata if available
        metadata = load_json_metadata(image_path)
        metadata_fields = build_metadata_fields(
            metadata, current_year, git_user_name, args.verbose
        )

        if process_image(image_path, metadata_fields):
            processed += 1
        else:
            failed += 1
            # Return non-zero exit code to fail commit if any image fails
            sys.exit(1)

    if args.verbose:
        print(f"\nSummary: {processed} processed, {failed} failed")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
