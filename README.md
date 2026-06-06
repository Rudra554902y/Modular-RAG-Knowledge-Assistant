# RAG — Retrieval-Augmented Generation (local)

A small local Retrieval-Augmented Generation (RAG) prototype that ingests PDF and text files, creates embeddings, stores them in a FAISS vector store, and exposes search/QA utilities for querying the indexed documents.

## Features

- Ingest documents from `data/PDF_files` and `data/text_files`.
- Create embeddings and persist a FAISS vector index in `faiss_store`.
- Simple search and retrieval utilities in `src/search.py` for building RAG workflows.

## Repo Structure

- [main.py](main.py) — project entrypoint / orchestrator
- [requirements.txt](requirements.txt) — Python dependencies
- [pyproject.toml](pyproject.toml) — project metadata
- [data/](data/) — document sources
	- `PDF_files/` — put PDFs to ingest here
	- `text_files/` — plain text files
- [faiss_store/](faiss_store/) — persisted FAISS index and metadata
- [src/](src/) — core modules
	- [src/data_loader.py](src/data_loader.py) — document loading/parsing
	- [src/embedding.py](src/embedding.py) — embedding creation
	- [src/vector_store.py](src/vector_store.py) — FAISS store helpers
	- [src/search.py](src/search.py) — search / retrieval utilities

## Quickstart (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Prepare data:

- Put PDF files into `data/PDF_files/` and/or text files into `data/text_files/`.

4. Build the embeddings and vector store:

```powershell
python main.py
```

This project's `main.py` coordinates loading documents, computing embeddings, and writing the FAISS index into `faiss_store/`.

## Usage

- After building the vector store you can use the functions in [src/search.py](src/search.py) to query the index and compose RAG prompts.
- Example (python REPL):

```python
from src.search import load_vector_store, query
vs = load_vector_store('faiss_store')
results = query(vs, 'Explain the main idea of the document')
print(results)
```

Adjust function names and parameters to match the implementations in `src/`.

## Development notes

- The FAISS index and any associated metadata are stored under `faiss_store/`. Remove or back up that folder to rebuild from scratch.
- If you add new documents, re-run `python main.py` to update the index.

## Pushing to GitHub

Create a repo on GitHub and follow these commands (replace the remote URL):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Contributing

Feel free to open issues or submit pull requests. Suggestions:

- Add CLI flags to `main.py` for incremental indexing and verbose logging.
- Add tests for `src/` modules.

## License

Specify a license for the project (e.g., MIT). Add a `LICENSE` file at the repository root.

---

If you want, I can also:

- Add a minimal example script demonstrating a full query roundtrip.
- Create a GitHub Actions workflow to run tests or format code on push.

