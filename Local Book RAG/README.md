# Local Book RAG

Helyben futó OCR + RAG rendszer beszkennelt könyvek feldolgozására és kereshető AI-tudásbázis építésére.

## Repository structure

```text
local-book-rag/
├── README.md
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-image-processing.md
│   ├── 03-ocr-pipeline.md
│   ├── 04-text-cleaning.md
│   ├── 05-chunking.md
│   ├── 06-embeddings.md
│   ├── 07-semantic-search.md
│   └── 08-rag-with-gpt-oss.md
├── scripts/
│   ├── split_pages.py
│   ├── preprocess.py
│   ├── ocr_all.py
│   ├── clean_ocr.py
│   ├── make_chunks.py
│   ├── embed_chunks.py
│   ├── search_test.py
│   └── ask_book.py
├── examples/
│   └── example-output.md
└── .gitignore
```

## Documentation

1. [Project overview](docs/01-project-overview.md)
2. [Image processing](docs/02-image-processing.md)
3. [OCR pipeline](docs/03-ocr-pipeline.md)
4. [Text cleaning](docs/04-text-cleaning.md)
5. [Chunking](docs/05-chunking.md)
6. [Embeddings](docs/06-embeddings.md)
7. [Semantic search](docs/07-semantic-search.md)
8. [RAG with gpt-oss](docs/08-rag-with-gpt-oss.md)

## Pipeline

```text
Scanned JPG book
      ↓
Page splitting
      ↓
Image preprocessing
      ↓
LightOnOCR-2
      ↓
Raw OCR text
      ↓
Text cleaning
      ↓
Chunking
      ↓
nomic-embed-text
      ↓
Semantic search
      ↓
gpt-oss:20b
      ↓
Answer with source references
```

## Main components

* Python 3.12
* OpenCV
* Ollama
* LightOnOCR-2
* nomic-embed-text
* gpt-oss:20b
* Cosine similarity
* Local JSON-based vector storage

## Result

A scanned Hungarian book can be queried with natural-language questions.

Example:

```text
Question:
Mire használják a kamillát?

Retrieved source:
SWScan00092_L.txt

Generated answer:
A könyv szerint a kamillát gyomor- és bélpanaszok,
görcsök és különféle gyulladások esetén alkalmazták.

Source:
[SWScan00092_L]
```

The complete pipeline runs locally without an external AI API.
