import argparse
import sys
from pathlib import Path
from PIL import Image


def process_image(file_path):
    try:
        with Image.open(file_path) as img:
            webp_path = file_path.with_suffix(".webp")

            original_width, original_height = img.size
            new_height = original_height
            new_width = original_width

            # Limit all images to 12MP
            if original_width > original_height:
                new_width = min(original_width, 2048)
                if original_width > new_width:
                    new_height = int((new_width / img.width) * img.height)
            else:
                new_height = min(original_height, 2048)
                if original_height > new_height:
                    new_width = int((new_height / img.height) * img.width)

            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            resized_img.save(webp_path, format="WEBP", quality=85)
            print(f"Resized {file_path} to {new_width}x{new_height}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args()
    image_generated = False

    for file in args.filenames:
        file_path = Path(file)
        if file_path.suffix.lower() in [".jpeg", ".jpg"]:
            process_image(file_path)
            image_generated = True

    return 1 if image_generated else 0


if __name__ == "__main__":
    sys.exit(main())
