import os
from fastapi import Request
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from app.services.get_embeddings import get_embedding_function
from app.core.logging import logger
from app.core.settings import settings


def get_chroma_client():
    return Chroma(
        persist_directory=settings.CHROMA_PATH,
        embedding_function=get_embedding_function()
    )


PROMPT_TEMPLATE = """
Answer the question {question} based only on the following context:

{context}

---

Please ensure your answer is short, precise, and well-sourced. Do not include any offensive or inappropriate content.
"""


def main(query_text: str):
    query_rag(query_text)


def is_question_relevant(results, threshold=1):
    logger.info(f"Checking relevance with threshold: {threshold}")
    # Check if any of the similarity scores are above the threshold
    for _, score in results:
        logger.info(f"Similarity score: {score}")
        if score < threshold:
            return True
    return False


def query_rag(query_text: str, llm, request: Request):
    try:
        logger.info("Preparing the database connection.")
        db = get_chroma_client()

        # Log the number of chunks in the database
        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])
        logger.info(f"Number of existing documents in DB: {len(existing_ids)}")

        if len(existing_ids) == 0:
            logger.info("No documents are present in the database.")
            return {"result": "No documents are present in the database.", "source_documents": []}

        logger.info("Performing similarity search in the database.")
        results = db.similarity_search_with_score(query_text, k=3)
        logger.info(f"Found {len(results)} results.")

        # Filter results with valid `page_content`
        valid_results = [
            (doc, score) for doc, score in results
            if doc.page_content and isinstance(doc.page_content, str)
        ]
        logger.info(f"Number of valid results: {len(valid_results)}")

        if not valid_results:
            logger.info("No valid documents found with content.")
            return {"result": "No relevant documents found.", "source_documents": []}

        # Log the scores of valid results
        for doc, score in valid_results:
            logger.info(
                f"Document: {doc.metadata.get('source', 'Unknown Source')}, Score: {score}"
            )

        # Check if the question is relevant to valid results
        if not is_question_relevant(valid_results, threshold=1):
            logger.info(
                "Question is not relevant to the content of the documents.")
            return {"result": "The question is not related to the content of the documents.", "source_documents": []}

        # Prepare context text from valid documents
        context_text = "\n\n---\n\n".join(
            [doc.page_content for doc, _ in valid_results]
        )
        logger.info("Context text prepared for the prompt.")

        # Format the prompt
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        formatted_prompt = prompt.format(
            context=context_text, question=query_text)
        logger.info("Prompt formatted.")

        # Get response from LLM
        response_text = llm.invoke(formatted_prompt)
        logger.info("Response received from the LLM.")

        # Prepare source information
        sources = []
        for doc, _ in valid_results:
            doc_metadata = doc.metadata
            source_id = doc_metadata.get("id", "Unknown ID")
            source_path = doc_metadata.get("source", "Unknown Source")
            filename = os.path.basename(source_path)

            source_info = {
                "source": source_path,
                "page": str(int(doc_metadata.get("page", "Unknown Page")) + 1),
                "paragraph": str(int(source_id.split(':')[2]) + 1)
                if len(source_id.split(':')) > 2 else "Unknown Paragraph",
                "link": f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/documents/{filename}",
            }
            sources.append(source_info)

        logger.info(f"Sources extracted: {sources}")
        return {"result": response_text, "source_documents": sources}

    except Exception as e:
        logger.error(f"Error during query processing: {e}")
        raise


# Example usage
if __name__ == "__main__":
    query_text = "Your query text here"
    main(query_text)
