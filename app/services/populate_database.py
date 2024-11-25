import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from app.services.get_embeddings import get_embedding_function
from langchain_chroma import Chroma
from app.core.logging import logger
from app.core.settings import settings

# CHROMA_PATH = os.getenv("CHROMA_PATH", "app/vectorstore/chroma")
# DATA_PATH = os.getenv("DATA_PATH", "app/documents")


def create_directories():
    os.makedirs(settings.CHROMA_PATH, exist_ok=True)
    os.makedirs(settings.DATA_PATH, exist_ok=True)
    logger.info(
        f"Ensured directories exist: {settings.CHROMA_PATH}, {settings.DATA_PATH}")


def get_chroma_client():
    return Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=get_embedding_function()
    )


def main(reset=False):
    create_directories()

    if reset:
        logger.info("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


def load_documents():
    logger.info(f"Loading documents from {settings.DATA_PATH}")
    document_loader = PyPDFDirectoryLoader(settings.DATA_PATH)
    documents = document_loader.load()
    logger.info(f"Loaded {len(documents)} documents")
    return documents


def split_documents(documents: list[Document]):
    logger.info("Splitting documents into chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunks)} chunks")
    return chunks


def add_to_chroma(chunks: list[Document]):
    logger.info("Adding chunks to Chroma vector store")
    try:
        # Load the existing database.
        db = get_chroma_client()

        # Calculate Page IDs.
        chunks_with_ids = calculate_chunk_ids(chunks)

        # Add or Update the documents.
        # IDs are always included by default
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        logger.info(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            # Use the correct method to add documents
            db.add_documents(new_chunks)
            logger.info(
                f"Added {len(new_chunks)} new chunks to the Chroma vector store")
        else:
            logger.info("No new chunks to add")

    except Exception as e:
        logger.error(f"Error adding chunks to Chroma vector store: {e}")


def calculate_chunk_ids(chunks):
    logger.info("Calculating chunk IDs")
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index (Paragraph)

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    logger.info(f"Calculated IDs for {len(chunks)} chunks")
    return chunks


def clear_database():
    logger.info("Clearing Chroma vector store and documents")

    # Delete the Chroma database directory
    if os.path.exists(settings.CHROMA_PATH):
        shutil.rmtree(settings.CHROMA_PATH)
        logger.info(
            f"Deleted Chroma database directory: {settings.CHROMA_PATH}")
    else:
        logger.info(
            f"Chroma database directory not found: {settings.CHROMA_PATH}")

    # Delete the documents directory
    if os.path.exists(settings.DATA_PATH):
        shutil.rmtree(settings.DATA_PATH)
        logger.info(f"Deleted documents directory: {settings.DATA_PATH}")
    else:
        logger.info(f"Documents directory not found: {settings.DATA_PATH}")

    # Recreate the directories
    create_directories()


def delete_pdf_records(pdf_filename: str) -> str:
    logger.info(
        f"Deleting records for {pdf_filename} from Chroma vector store")
    try:
        # Load the existing database.
        db = get_chroma_client()

        # Retrieve all metadata.
        existing_items = db.get(include=["metadatas"])
        metadatas = existing_items["metadatas"]

        # Find and delete records associated with the specified PDF file.
        ids_to_delete = []
        for idx, metadata in enumerate(metadatas):
            source_path = metadata.get("source", "")
            if os.path.basename(source_path) == pdf_filename:
                ids_to_delete.append(existing_items["ids"][idx])
                logger.info(
                    f"Found record to delete: {existing_items['ids'][idx]}")

        if ids_to_delete:
            db.delete(ids=ids_to_delete)
            logger.info(
                f"Deleted {len(ids_to_delete)} records for {pdf_filename}")
        else:
            logger.info(f"No records found for {pdf_filename}")

        # Delete the PDF file from the documents folder.
        file_path = os.path.join(settings.DATA_PATH, pdf_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file {file_path}")
            return f"Records and file for {pdf_filename} deleted successfully"
        else:
            logger.info(f"File {file_path} not found")
            if ids_to_delete:
                return f"Records for {pdf_filename} deleted, but file not found"
            else:
                return f"No records or file found for {pdf_filename}"

    except Exception as e:
        logger.error(f"Error deleting records from Chroma vector store: {e}")
        raise
