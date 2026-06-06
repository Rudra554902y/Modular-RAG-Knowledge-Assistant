from pathlib import Path
from typing import Any, Dict, List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, JSONLoader, CSVLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader

def load_all_documents(directory: str) -> List[Any]:
    """
    Load all documents from a specified directory and return a list of dictionaries containing the content and metadata.
    
    Supported file types include PDF, TXT, DOCX, JSON, CSV, and Excel files. The function automatically detects the file type based on the file extension and uses the appropriate loader to extract the content.
    
    Args:
        directory (str): The path to the directory containing the documents.
    """
    data_path = Path(directory).resolve()
    print(f"[DEBUG] Data path resolved to: {data_path}")
    documents = []
    
    ## PDF Files
    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f"[DEBUG] Found {len(pdf_files)} PDF files : {[str(f) for f in pdf_files]}")
    for pdf_file in pdf_files:
        print(f"[DEBUG] Loading PDF: {pdf_file}")
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DEBUG] Loaded {len(loaded)} PDF docs from {pdf_file}")
            documents.extend(loaded)
        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")
    
    return documents
    