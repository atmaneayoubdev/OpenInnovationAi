import shutil
from fastapi import APIRouter, HTTPException, Request
from fastapi import APIRouter, File, UploadFile, HTTPException
import os

from langchain_ollama import OllamaLLM
from app.api.schemas import DeletePDFRequest, QuestionRequest
from app.core.settings import settings
from app.core.logging import logger
from app.services.populate_database import clear_database, delete_pdf_records, main
from app.services.query_handler import query_rag as query_document_ollama

router = APIRouter()
llama_model = OllamaLLM(model="llama2")


@router.post("/document-upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Check for allowed file extensions
        allowed_extensions = ["pdf"]
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            logger.error(f"File type not allowed: {file.filename}")
            return {"message": "We support only PDF files. Thanks for using our API."}

        # Trim spaces from the filename
        trimmed_filename = file.filename.replace(" ", "_")

        # Read the content of the uploaded file
        content = await file.read()

        # Define the path to save the file
        save_path = os.path.join(settings.DOCUMENTS_FOLDER, trimmed_filename)

        # Ensure the documents folder exists
        if not os.path.exists(settings.DOCUMENTS_FOLDER):
            os.makedirs(settings.DOCUMENTS_FOLDER)

        # Save the file to the defined path
        with open(save_path, "wb") as f:
            f.write(content)

        # Call the populate_database script to save the embeddings
        main()

        # Log and return response
        logger.info(
            f"Document uploaded and saved successfully: {trimmed_filename}")
        return {"message": "Document uploaded and saved successfully!", "document_info": {"filename": trimmed_filename}}

    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred while uploading the document.")


@router.post("/delete-pdf")
async def delete_pdf(request: DeletePDFRequest):
    try:
        # Call the delete_pdf_records function to delete records associated with the specified PDF file
        status_message = delete_pdf_records(request.filename)

        # Log and return response
        logger.info(status_message)
        return {"message": status_message}

    except Exception as e:
        logger.error(
            f"Error deleting records for {request.filename}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred while deleting records for {request.filename}: {str(e)}")


@router.post("/clear-data")
async def clear_data():
    try:
        # Get the documents folder path from settings
        documents_folder = settings.DOCUMENTS_FOLDER

        # Check if the folder exists
        if os.path.exists(documents_folder):
            # Iterate over all PDF files in the documents folder
            for filename in os.listdir(documents_folder):
                if filename.endswith(".pdf"):
                    # Call the delete_pdf_records function to delete records associated with the PDF file
                    delete_pdf_records(filename)

            # # Delete all files in the documents folder
            # for filename in os.listdir(documents_folder):
            #     file_path = os.path.join(documents_folder, filename)
            #     if os.path.isfile(file_path) or os.path.islink(file_path):
            #         os.unlink(file_path)
            #     elif os.path.isdir(file_path):
            #         shutil.rmtree(file_path)

            # # Clear the Chroma vector store
            # clear_database()

            # Log and return response
            logger.info(
                "All documents and embeddings have been deleted successfully.")
            return {"message": "All documents and embeddings have been deleted successfully."}
        else:
            raise HTTPException(
                status_code=404, detail="Documents folder not found.")

    except Exception as e:
        logger.error(f"Error clearing data: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred while clearing the data.")


@router.get("/documents")
async def list_documents():
    try:
        # List all files in the documents folder
        documents = os.listdir(settings.DOCUMENTS_FOLDER)
        all_files = [{"filename": file, "extension": os.path.splitext(
            file)[1].lower()} for file in documents]

        # Log and return response
        logger.info(f"Available documents: {all_files}")
        return {"documents": all_files}

    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred while listing the documents.")


@router.post("/ask-ollama")
async def ask_ollama(request: Request, question_request: QuestionRequest):
    try:
        # Get the query from the request
        query = question_request.question

        # Query the vector database using Ollama model
        result = query_document_ollama(query, llama_model, request)

        # Log the result to inspect its structure
        logger.info(f"Query result: {result}")

        if result is None:
            raise ValueError("No response from the model")

        # Initialize response data
        response_data = {
            "answer": "",
            "sources": []
        }

        # Check if the result is a string
        if isinstance(result, str):
            response_data["answer"] = result
        # Ensure the result is a dictionary
        elif isinstance(result, dict):
            # Process the result to return a formatted response
            answer = result.get('result')
            sources = result.get('source_documents', [])

            if answer is None:
                raise ValueError("No answer found in the result")

            response_data["answer"] = answer
            response_data["sources"] = sources
        else:
            raise ValueError(f"Unexpected result format: {result}")

        return response_data

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
