# Local Book RAG

Helyben futó OCR + RAG rendszer beszkennelt könyvek feldolgozására és természetes nyelvű lekérdezésére.

A projekt egy régi, magyar nyelvű, JPG formátumban beszkennelt könyvből készít kereshető tudásbázist. A teljes feldolgozás lokálisan történik: a képek OCR-ezése, a szemantikus keresés és a válaszgenerálás is helyi modellekkel fut.

## Fő cél

A rendszer lehetővé teszi, hogy egy beszkennelt könyv tartalmáról természetes nyelven kérdezzünk, például:

```text
Mire használják a kamillát?
```

A rendszer:

1. megkeresi a kérdéshez leginkább kapcsolódó könyvrészleteket,
2. ezeket átadja a helyben futó nyelvi modellnek,
3. a modell kizárólag a megtalált források alapján válaszol,
4. a válasz végén megadja a felhasznált forrásfájlokat.

## Feldolgozási folyamat

```text
Beszkennelt JPG oldalak
        ↓
Oldalak szétvágása
        ↓
Képek előfeldolgozása
        ↓
LightOnOCR-2
        ↓
Nyers OCR szöveg
        ↓
Szövegtisztítás
        ↓
Chunkolás
        ↓
nomic-embed-text
        ↓
Szemantikus keresés
        ↓
gpt-oss:20b
        ↓
Forrásolt válasz
```

## Használt technológiák

* Python 3.12
* Ollama
* OpenCV
* LightOnOCR-2
* nomic-embed-text
* gpt-oss:20b
* cosine similarity
* JSON alapú lokális adattárolás

## Használt Ollama modellek

OCR:

```bash
ollama pull maternion/LightOnOCR-2
```

Embedding:

```bash
ollama pull nomic-embed-text
```

Válaszgenerálás:

```bash
ollama pull gpt-oss:20b
```

## Projektstruktúra

```text
Local Book RAG/
│
├── README.md
│
└── scripts/
    ├── split_pages.py
    ├── preprocess.py
    ├── ocr_all.py
    ├── clean_ocr.py
    ├── make_chunks.py
    ├── embed_chunks.py
    ├── search_test.py
    └── ask_book.py
```

A helyi feldolgozási könyvtárak:

```text
01_original/
02_pages/
03_preprocessed/
04_ocr_raw/
05_ocr_clean/
06_chunks/
```

Ezeket nem szükséges GitHubra feltölteni.

## 1. Oldalak szétvágása

A beszkennelt könyvoldalak gyakran két oldalt tartalmaznak egyetlen JPG-ben.

```bash
python scripts/split_pages.py
```

A kimenet:

```text
SWScan00055_L.JPG
SWScan00055_R.JPG
```

## 2. Kép-előfeldolgozás

A képek OCR előtti javítása:

* szürkeárnyalatos átalakítás,
* zajszűrés,
* kontrasztjavítás,
* enyhe élesítés.

```bash
python scripts/preprocess.py
```

## 3. OCR

Az OCR-t a helyben futó LightOnOCR-2 modell végzi az Ollama API-n keresztül.

```bash
python scripts/ocr_all.py
```

A rendszer minden oldalhoz külön TXT fájlt készít:

```text
SWScan00092_L.PNG
        ↓
SWScan00092_L.txt
```

## 4. OCR szöveg tisztítása

A nyers OCR szövegek alapvető tisztítása:

* sortörések normalizálása,
* sorvégi elválasztások összefűzése,
* fölösleges whitespace eltávolítása,
* túl sok üres sor csökkentése.

```bash
python scripts/clean_ocr.py
```

Az eredeti OCR fájlok változatlanul megmaradnak.

## 5. Chunkolás

A megtisztított könyvszöveg kisebb, átfedő szövegrészekre kerül felosztásra.

Alapértelmezett értékek:

```text
Chunk size: 1800 karakter
Overlap: 300 karakter
```

Futtatás:

```bash
python scripts/make_chunks.py
```

Kimenet:

```text
06_chunks/chunks.json
```

## 6. Embeddingek létrehozása

A chunkokból a `nomic-embed-text` modell készít embedding vektorokat.

```bash
python scripts/embed_chunks.py
```

Kimenet:

```text
06_chunks/chunks_with_embeddings.json
```

## 7. Szemantikus keresés tesztelése

A keresési réteg külön is tesztelhető LLM nélkül.

```bash
python scripts/search_test.py
```

Példa:

```text
Kérdés: Mire használják a kamillát?
```

A rendszer cosine similarity alapján kiírja az 5 legrelevánsabb könyvrészletet.

## 8. Kérdezés a könyvből

A teljes RAG rendszer:

```bash
python scripts/ask_book.py
```

Példa:

```text
Kérdés: Mire használják a kamillát?
```

A folyamat:

```text
Kérdés
   ↓
nomic-embed-text
   ↓
Top releváns chunkok
   ↓
gpt-oss:20b
   ↓
Magyar nyelvű válasz
   ↓
Forráshivatkozások
```

Példa válasz:

```text
A könyv szerint a kamillát többek között
gyomor- és bélpanaszok, görcsök és különféle
gyulladások esetén alkalmazták. [SWScan00092_L]

Források:
- SWScan00092_L
- SWScan00090_R
```

## Lokális működés

A projekt nem használ külső AI API-t.

Az OCR, az embeddingek létrehozása és a válaszgenerálás is a helyi gépen fut az Ollama segítségével.



## Megjegyzés

Régi könyvek esetén az OCR tartalmazhat kisebb hibákat, ezért a rendszer megtartja az eredeti forrásfájl nevét minden szövegrész mellett.

Egészségügyi vagy történeti könyvek esetén a generált válaszokat az eredeti könyv tartalmaként kell kezelni, nem automatikusan aktuális szakmai ajánlásként.
