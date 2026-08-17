# Simple RAG from Scratch

A minimal, terminal-based **Retrieval-Augmented Generation (RAG)** implementation built from scratch. It dynamically loads documents from the `data` directory, embeds each line as a chunk with Ollama, retrieves relevant chunks by cosine similarity, and answers questions using a local LLM with the retrieved context.

### How it works

1. **Scan & Index:** Automatically scans the `data/` directory, loads all text files (`.txt`), embeds each non-empty line with the embedding model, and stores the (embedding, chunk) pairs in an in-memory vector database.
2. **Retrieve:** When a query is submitted, the system embeds it, computes cosine similarity across all database chunks, and returns the top matching results.
3. **Generate:** Builds a system prompt with only the retrieved context chunks, guiding the local language model (LLM) to answer the query solely using the compiled facts.

---

## Table of Contents

- [Models](#models)
- [Datasets](#datasets)
- [Features](#features)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage (Interactive CLI)](#usage-interactive-cli)
- [Configuration](#configuration)
- [Author](#author)

---

## Models

- **Embedding Model:** `hf.co/CompendiumLabs/bge-base-en-v1.5-gguf`
- **Language Model:** `hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF`

---

## Datasets

The project automatically consumes any text files (`.txt`) placed in the `data/` directory. Each line is treated as **one chunk** during the indexing phase. The built-in datasets include:
- `cat-facts.txt`: Facts about cats (150 entries).
- `dog-facts.txt`: Facts about dogs (15 entries).
- `oops-concepts.txt`: Key Object-Oriented Programming (OOP) concepts (20 entries).
- `rag_sample_data.txt`: RAG overview, components, and strategies (45 entries).

---

## Features

- **Multi-File Dataset Ingestion**: Scans the `data/` directory to load and index all text files automatically.
- **Interactive CLI Loop**: Keep the vector database loaded in memory and run multiple queries without rebuilding the index.
- **Direct Database Search**: Query and retrieve the raw matched text chunks and their similarity scores directly without involving the LLM.
- **Database Statistics**: View the total counts of loaded chunks and models in use.
- **Consolidated Progress Logs**: Minimal footprint output when index is populating.

---

## Requirements

- **Python** >= 3.13
- **Ollama** installed and running locally (see [Setup](#setup))
- **ollama** Python package (installed via `pip` or virtual environment synchronization)

---

## Project Structure

```text
code-simple-rag-from-scartch/
├── main.py                  # Entry point: Interactive shell, search, and LLM chat
├── pyproject.toml           # Project metadata and dependencies (ollama)
├── README.md                # Documentation
├── data/                    # Text datasets folder (reads all *.txt files)
│   ├── cat-facts.txt        # Facts about cats (one per line)
│   ├── dog-facts.txt        # Facts about dogs
│   ├── oops-concepts.txt    # OOP definitions
│   └── rag_sample_data.txt  # RAG general architecture overview
└── src/
    ├── loading_datasets.py  # Scans and reads data/*.txt into in-memory list
    ├── impl_vector_db.py    # Memory database, models, and embeddings addition
    └── impl_retrieval_func.py  # Cosine similarity and retrieval score ranker (top_n)
```

---

## Setup

### 1. Download Ollama and Models

1. Install Ollama from [ollama.com](https://ollama.com).
2. Start the Ollama app or service, then download the required models in your terminal:
   ```bash
   ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
   ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
   ```

### 2. Install Dependencies

Using **pip** directly:
```bash
pip install ollama
```

Or using **uv** (recommended) from the project root:
```bash
uv sync
```

---

## Usage (Interactive CLI)

Start the program from the project root directory:

```bash
uv run main.py
```
Or:
```bash
python main.py
```

### Flow and Menu Options

1. The script will load all datasets and display progress:
   ```text
   Initializing vector database...
   Loaded 150 entries from cat-facts.txt
   Loaded 15 entries from dog-facts.txt
   Loaded 20 entries from oops-concepts.txt
   Loaded 45 entries from rag_sample_data.txt
   Progress: 10/230 chunks added.
   ...
   Progress: 230/230 chunks added.

   === RAG System Initialized ===
   ```

2. Choose from the CLI Menu:
   ```text
   ========================================
   Select an option:
   1. Ask the Chatbot (RAG)
   2. Search Vector Database (Direct)
   3. View Database Statistics
   4. Exit
   ========================================
   Enter choice (1-4):
   ```

* **Option 1**: Asks a question, retrieves the top 3 relevant chunks, displays their similarity score, and feeds them to the LLM to stream a context-grounded response.
* **Option 2**: Performs a vector-based semantic search across all facts, returning the top 5 match candidates (no LLM generation).
* **Option 3**: Displays database telemetry (total size, models configured).
* **Option 4**: Safely exits the application.

---

## Configuration

- **Models**: If you wish to use different GGUF weights, edit `EMBEDDING_MODEL` and `LANGUAGE_MODEL` inside `src/impl_vector_db.py`.
- **Top K Settings**: Modify `top_n` parameters within menu options in `main.py` to get more or fewer matched chunks.

---

## Author

**Sumanta Swain**

---

Built with ❤️ using RAG & Python.
