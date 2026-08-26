```python
import json
import math
import urllib.request
from pathlib import Path

db_file = Path("06_chunks/chunks_with_embeddings.json")
model = "nomic-embed-text:latest"

query = input("Kérdés: ").strip()

payload = {
    "model": model,
    "input": query
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

query_embedding = result["embeddings"][0]

chunks = json.loads(
    db_file.read_text(encoding="utf-8")
)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


results = []

for chunk in chunks:
    score = cosine_similarity(
        query_embedding,
        chunk["embedding"]
    )

    results.append((score, chunk))

results.sort(
    key=lambda x: x[0],
    reverse=True
)

print("\nTOP TALÁLATOK:\n")

for score, chunk in results[:5]:
    print("=" * 80)
    print(f"Pontszám: {score:.4f}")
    print(f"Forrás: {chunk['source']}")
    print()
    print(chunk["text"])
    print()
```
