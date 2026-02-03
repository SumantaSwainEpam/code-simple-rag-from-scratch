# Simple RAG from Scratch

A minimal **Retrieval-Augmented Generation (RAG)** implementation built from scratch. It loads a list of cat facts, embeds each fact as a chunk with Ollama, retrieves relevant chunks by cosine similarity, and answers questions using a local LLM with the retrieved context.

### How it works

1. **Index:** Load `data/cat-facts.txt`, embed each line with the embedding model, and store (embedding, chunk) pairs in an in-memory vector store.
2. **Retrieve:** For your question, embed the query, compute cosine similarity with all chunks, and return the top 3.
3. **Generate:** Build a system prompt with only those chunks; the language model answers using that context (no extra knowledge).

## Table of contents

- [Models](#models) · [Dataset](#dataset) · [Features](#features) · [Requirements](#requirements)
- [Project structure](#project-structure) · [Setup](#setup) · [Usage](#usage) · [Example output](#example-output)
- [Configuration](#configuration) · [Notes](#notes) · [Author](#author)

## Models

- **Embedding model:** `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf`
- **Language model:** `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF`

## Dataset

The project uses a simple list of **facts about cats** stored in `data/cat-facts.txt`. Each line (each fact) is treated as **one chunk** during the indexing phase.

## Features

- Load cat facts from a text file (`data/cat-facts.txt`)
- Embed each fact as a chunk and store in an in-memory vector store
- Retrieve top-k relevant chunks for a user query using cosine similarity
- Generate answers via Ollama (streaming) using only the retrieved context

## Requirements

- **Python** >= 3.13
- **Ollama** installed and running locally (see [Download Ollama and models](#download-ollama-and-models))
- **ollama** Python package (see [Install the ollama Python package](#install-the-ollama-python-package))

## Project Structure

```
code-simple-rag-from-scartch/
├── main.py                 # Entry point: load data, build vector DB, query, and chat
├── pyproject.toml          # Project metadata and dependencies (ollama)
├── README.md
├── data/
│   ├── cat-facts.txt       # Cat facts dataset (one fact per line = one chunk)
│   └── rag_sample_data.txt # Optional sample data
└── src/
    ├── loading_datasets.py  # Loads text file into a list of lines (dataset)
    ├── impl_vector_db.py    # Vector DB (list of embeddings + chunks), embedding model, add_chunks_to_vector_db()
    └── impl_retrieval_func.py  # cosine_similarity(), retrieve_chunks(query, top_n=3)
```

### Module Overview

| File | Purpose |
|------|---------|
| `main.py` | Loads dataset, populates vector DB, prompts for a question, retrieves top chunks, builds system prompt with context, and streams the LLM response. |
| `src/loading_datasets.py` | Opens `data/cat-facts.txt` (UTF-8), reads lines into `dataset`. |
| `src/impl_vector_db.py` | Defines `EMBEDDING_MODEL`, `LANGUAGE_MODEL`, `VECTOR_DB`, and `add_chunks_to_vector_db(chunk)` using Ollama embeddings. |
| `src/impl_retrieval_func.py` | Computes cosine similarity, embeds the query, scores all chunks, returns top `top_n` as `(chunk, similarity)` pairs. |

## Setup

### Download Ollama and models

1. **Install Ollama** from the project website: [ollama.com](https://ollama.com).

2. After installation, open a terminal and run the following commands to download the required models:

   ```bash
   ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
   ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
   ```

3. If you see output like the following, the models were downloaded successfully:

   ```
   pulling manifest
   ...
   verifying sha256 digest
   writing manifest
   success
   ```

### Install the ollama Python package

To use Ollama from Python, install the **ollama** package:

```bash
pip install ollama
```

If you use [uv](https://github.com/astral-sh/uv) for this project, run from the project root:

```bash
uv sync
```

This installs the project dependencies (including `ollama`) from `pyproject.toml`.

## Usage

Run from the **project root** (so `data/` and `src` imports resolve correctly):

```bash
uv run main.py
```

Or with Python directly:

```bash
python main.py
```

1. The script loads `data/cat-facts.txt` and embeds each fact (each line) into the vector DB.
2. You are prompted: **Ask me a question:**
3. It retrieves the top 3 most similar chunks and prints them with similarity scores.
4. The chatbot answers using only that context; the response is streamed in the terminal.

## Example output

After running `uv run main.py` or `python main.py`, you’ll see the indexing messages, then the prompt. Example with the question *"How much do cats sleep?"*:

```
Loaded 150 entries
Added chunk 1 of 150 to vector database
Added chunk 2 of 150 to vector database
...
Added chunk 150 of 150 to vector database

Ask me a question: How much do cats sleep?

Retrieved knowledge:
 - (similarity: 0.89) On average, cats spend 2/3 of every day sleeping. That means a nine-year-old cat has been awake for only three years of its life.
 - (similarity: 0.72) A cat's brain is biologically more similar to a human brain than it is to a dog's. Both humans and cats have identical regions in their brains that are responsible for emotions.
 - (similarity: 0.68) Cats make about 100 different sounds. Dogs make only about 10.

Chatbot response:
On average, cats spend about two-thirds of every day sleeping. So a nine-year-old cat has been awake for only around three years of its life.
```

The similarity scores and chatbot reply depend on the embedding and language models; your run may differ slightly.

## Configuration

- **Data file**: Edit `src/loading_datasets.py` to change the path (e.g. to `data/rag_sample_data.txt`) or loading logic. The default is `data/cat-facts.txt` (one fact per line = one chunk).
- **Models**: The project uses `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf` (embedding) and `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF` (language). Edit `EMBEDDING_MODEL` and `LANGUAGE_MODEL` in `src/impl_vector_db.py` to use other Ollama models.
- **Retrieval**: Change `top_n` in `retrieve_chunks(query, top_n=3)` in `main.py` (default is 3) or when calling the function.

## Notes

- **Ollama must be running** before you start the script (e.g. start the Ollama app or run `ollama serve`).
- **Run from the project root** so that `data/cat-facts.txt` and `from src.*` imports work.
- The data file is read with **UTF-8** encoding; use UTF-8 for custom data files.

## Author

**Sumanta Swain**

---

Built with ❤️ using RAG & Python.
