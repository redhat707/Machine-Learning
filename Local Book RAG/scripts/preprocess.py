```python id="dnnqpv"
import cv2
from pathlib import Path

source_dir = Path("02_pages")
output_dir = Path("03_preprocessed")
output_dir.mkdir(exist_ok=True)

files = sorted(source_dir.glob("*.JPG"))

for source in files:
    img = cv2.imread(str(source))

    if img is None:
        print(f"HIBA: {source.name}")
        continue

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Mild noise reduction
    denoised = cv2.fastNlMeansDenoising(
        gray,
        None,
        h=7,
        templateWindowSize=7,
        searchWindowSize=21
    )

    # Local contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    contrast = clahe.apply(denoised)

    # Mild sharpening
    blurred = cv2.GaussianBlur(contrast, (0, 0), 1.0)
    sharpened = cv2.addWeighted(
        contrast,
        1.5,
        blurred,
        -0.5,
        0
    )

    output = output_dir / f"{source.stem}.PNG"

    cv2.imwrite(str(output), sharpened)

    print(f"Kész: {source.name}")

print(f"\nFeldolgozva: {len(files)} oldal.")
```
