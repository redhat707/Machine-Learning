```python
import base64
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

source_dir = Path("03_preprocessed")
output_dir = Path("04_ocr_raw")
output_dir.mkdir(exist_ok=True)

model = "maternion/LightOnOCR-2:latest"

prompt = """Olvasd ki pontosan a képen látható magyar szöveget.
Ne foglald össze, ne javítsd át, ne modernizáld.
Őrizd meg a bekezdéseket és a címsorokat.
Csak az OCR-rel kiolvasott szöveget add vissza."""

files = sorted(source_dir.glob("SWScan*_?.PNG"))

total = len(files)

print(f"Talált oldalak: {total}")

for index, image_path in enumerate(files, start=1):
    output_path = output_dir / f"{image_path.stem}.txt"

    if output_path.exists():
        print(f"[{index}/{total}] KIHAGYVA: {image_path.name}")
        continue

    try:
        image_b64 = base64.b64encode(
            image_path.read_bytes()
        ).decode("utf-8")

        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False
        }

        request = Request(
            "http://localhost:11434/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        print(f"[{index}/{total}] OCR: {image_path.name}")

        with urlopen(request, timeout=300) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        text = result["response"]

        output_path.write_text(
            text,
            encoding="utf-8"
        )

    except (URLError, HTTPError, TimeoutError) as e:
        print(f"HIBA: {image_path.name}: {e}")

print("\nOCR feldolgozás kész.")
```
