```python
import json
import urllib.request
from pathlib import Path

input_file = Path("06_chunks/chunks.json")
output_file = Path("06_chunks/chunks_with_embeddings.json")

model = "nomic-embed-text:latest"

chunks = json.loads(
    input_file.read_text(encoding="utf-8")
)

total = len(chunks)

for i, chunk in enumerate(chunks, start=1):
    payload = {
        "model": model,
        "input": chunk["text"]
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/embed",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    chunk["embedding"] = result["embeddings"][0]

    print(f"[{i}/{total}] {chunk['id']}")

output_file.write_text(
    json.dumps(
        chunks,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print("\nKész.")
print(f"Embeddingek: {total}")
print(f"Fájl: {output_file}")
```
