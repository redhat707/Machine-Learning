```python
import json
import math
import urllib.request
from pathlib import Path

DB_FILE = Path("06_chunks/chunks_with_embeddings.json")

EMBED_MODEL = "nomic-embed-text:latest"
CHAT_MODEL = "gpt-oss:20b"

TOP_K = 4


def ollama_embed(text):
    payload = {
        "model": EMBED_MODEL,
        "input": text
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

    return result["embeddings"][0]


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def search_chunks(query, chunks):
    query_embedding = ollama_embed(query)

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

    return results[:TOP_K]


def ask_gpt(query, results):
    context_parts = []

    for number, (score, chunk) in enumerate(results, start=1):
        context_parts.append(
            f"""
FORRÁS {number}
Fájl: {chunk['source']}
Hasonlóság: {score:.4f}

{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
Te egy régi magyar gyógynövénykönyv tudásbázisát használod.

SZABÁLYOK:

- Magyarul válaszolj.
- Elsősorban kizárólag az alább megadott könyvrészletekből válaszolj.
- Ne találj ki olyan állítást, amely nincs a forrásokban.
- Ha nincs elegendő információ a forrásokban, ezt világosan mondd meg.
- A választ jól áttekinthető Markdown formában add meg.
- Kezdd 2-3 mondatos rövid összefoglalóval.
- Ezután használj rövid alcímeket és felsorolásokat.
- Ne használj táblázatot, hacsak a kérdés kifejezetten nem kéri.
- Ne ismételd ugyanazt több pontban.
- Minden fontos állítás után add meg a forrást ilyen formában:
  [SWScan00092_L]
- A végén legyen egy "Források" rész.
- Ne használj felesleges díszítést vagy túl sok címsort.
- A könyv régi lehet, ezért az egészségügyi állításokat történeti
  forrásként kezeld, ne modern orvosi tanácsként.

KÉRDÉS:

{query}

KÖNYVRÉSZLETEK:

{context}
"""

    payload = {
        "model": CHAT_MODEL,
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    print("\nA gpt-oss gondolkodik...\n")

    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["response"]


chunks = json.loads(
    DB_FILE.read_text(encoding="utf-8")
)

print("Local Book RAG")
print("Kilépés: exit\n")

while True:
    query = input("Kérdés: ").strip()

    if query.lower() in {
        "exit",
        "quit",
        "kilepes",
        "kilépés"
    }:
        break

    if not query:
        continue

    results = search_chunks(
        query,
        chunks
    )

    answer = ask_gpt(
        query,
        results
    )

    print("=" * 80)
    print(answer)
    print("=" * 80)
    print()
```
