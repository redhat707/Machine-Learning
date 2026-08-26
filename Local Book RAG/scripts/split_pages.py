```python
import cv2
from pathlib import Path

source_dir = Path("01_original")
output_dir = Path("02_pages")
output_dir.mkdir(exist_ok=True)

files = sorted(source_dir.glob("SWScan*.JPG"))

for source in files:
    img = cv2.imread(str(source))

    if img is None:
        print(f"HIBA: nem sikerült megnyitni: {source.name}")
        continue

    height, width = img.shape[:2]
    middle = width // 2

    left = img[:, :middle]
    right = img[:, middle:]

    stem = source.stem

    cv2.imwrite(
        str(output_dir / f"{stem}_L.JPG"),
        left
    )

    cv2.imwrite(
        str(output_dir / f"{stem}_R.JPG"),
        right
    )

    print(f"Kész: {source.name}")

print(f"\nFeldolgozva: {len(files)} eredeti scan.")
```
