```python
import json
from pathlib import Path

source_dir = Path("05_ocr_clean")
output_dir = Path("06_chunks")
output_dir.mkdir(exist_ok=True)

CHUNK_SIZE = 1800
OVERLAP = 300

files = sorted(source_dir.glob("*.txt"))

all_chunks = []

for source in files:
    text = source.read_text(
        encoding="utf-8",
        errors="replace"
    ).strip()

    # Skip very short or nearly empty pages
    if len(text) < 80:
        continue

    start = 0
    chunk_id = 0

    while start < len(text):
        end = min(
            start + CHUNK_SIZE,
            len(text)
        )

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunk = {
                "id": f"{source.stem}_{chunk_id:03d}",
                "source": source.name,
                "text": chunk_text
            }

            all_chunks.append(chunk)

        if end == len(text):
            break

        start = end - OVERLAP
        chunk_id += 1

output_file = output_dir / "chunks.json"

output_file.write_text(
    json.dumps(
        all_chunks,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print("Kész.")
print(f"Feldolgozott oldalak: {len(files)}")
print(f"Létrehozott chunkok: {len(all_chunks)}")
print(f"Fájl: {output_file}")
```
