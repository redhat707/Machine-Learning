```python
import re
from pathlib import Path

source_dir = Path("04_ocr_raw")
output_dir = Path("05_ocr_clean")
output_dir.mkdir(exist_ok=True)

files = sorted(source_dir.glob("*.txt"))

for source in files:
    text = source.read_text(
        encoding="utf-8",
        errors="replace"
    )

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Join words split by line-end hyphenation
    # Example:
    # "össze-\nfoglalta" -> "összefoglalta"
    text = re.sub(
        r"(\w)-\n(\w)",
        r"\1\2",
        text
    )

    # Remove trailing whitespace
    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    # Replace repeated spaces with one space
    text = re.sub(
        r"[ \t]{2,}",
        " ",
        text
    )

    # Reduce excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    text = text.strip() + "\n"

    output = output_dir / source.name

    output.write_text(
        text,
        encoding="utf-8"
    )

    print(f"Kész: {source.name}")

print(f"\nFeldolgozva: {len(files)} OCR fájl.")
```
