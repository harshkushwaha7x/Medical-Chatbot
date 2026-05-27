"""Helper functions for Medical Chatbot.

This module contains utility functions for loading and processing PDF documents,
text splitting, and embedding generation using HuggingFace models.
"""
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


def load_pdf_file(data: str) -> List[Document]:
    """Extract and load PDF documents from a directory.
    
    Args:
        data (str): Path to directory containing PDF files
        
    Returns:
        List[Document]: List of loaded documents from PDF files
        
    Raises:
        FileNotFoundError: If directory does not exist
        Exception: If PDF loading fails
    """
    try:
        logger.info(f"Loading PDF files from {data}")
        loader = DirectoryLoader(
            data,
            glob="*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents
    except Exception as e:
        logger.error(f"Error loading PDF files: {e}")
        raise



def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs



#Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks



#Download the Embeddings from HuggingFace 
def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  #this model return 384 dimensions
    return embeddings