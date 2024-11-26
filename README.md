# Technical Challenge for Open Innovation AI
A document-based GPT system designed to answer questions based on internal documents. Built using FastAPI, Ollama, and LangChain, it provides short, precise, and well-sourced answers with links to document locations.

**GitHub Repository**: [OpenInnovationAi](https://github.com/atmaneayoubdev/OpenInnovationAi)

---

## Features
- Upload, delete, and manage internal documents.
- Generate embeddings using Ollama.
- Answer user queries with well-sourced responses.
- Links to document locations for easy verification.

---

## Architecture
### Tech Stack
- **Backend**: FastAPI
- **Vector Store**: Chroma DB
- **Model**: Llama2 via Ollama
- **Embedding Engine**: LangChain with Ollama embeddings
- **Database**: Local persistence with Chroma

### Workflow
1. Documents are uploaded and split into chunks.
2. Embeddings are generated and stored in Chroma DB.
3. User queries are matched against embeddings.
4. Responses are generated using Llama2, with document links.

---

## Setup Instructions

### Prerequisites
- Docker installed
- NVIDIA or AMD GPU (optional for accelerated performance)

### Clone the Repository
   ```bash
   git clone https://github.com/atmaneayoubdev/OpenInnovationAi.git
   cd OpenInnovationAi
   ```

### Start the Ollama Container
If You Have Ollama Server Running Locally
If you already have the Ollama server running locally, you can skip the steps to start the container. Just ensure that the following models are available on your system:

Llama2 Model for generation
nomic-embed-text Model for embeddings

Before running the Ollama container, make sure you have the Ollama image pulled from Docker Hub:
```bash
docker pull ollama/ollama
```

For CPU:
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

For NVIDIA GPU:
```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Pull Required Models After starting the Ollama container, ensure you have the necessary models for generation and embeddings:
Pull Llama2 Model:
```bash
docker exec -it ollama ollama pull llama2
```
Pull Embedding Model:
```bash
docker exec -it ollama ollama pull nomic-embed-text
```

Verify the models are downloaded by listing the available models:
```bash
docker exec -it ollama ollama list
```


### Start the fastapi Container
Build and run the FastAPI container:

```bash
docker build -f Dockerfile.fastapi -t open_innovation_ai .

docker run -d -p 8000:8000 --name open_innovation_ai open_innovation_ai
```

### Access the API Documentation
Swagger UI: http://localhost:8000/docs

---

## Running the Next.js App with Docker
### Build the Docker Image
```bash
docker build -t nextjs-app -f Dockerfile.nextjs ./frontend
```

### Run the Docker Container
```bash
docker run -d --name nextjs-app -p 3000:3000 nextjs-app
```
### Access the App
http://localhost:3000


---

## Postman Collection

We’ve provided a Postman collection to help you test the API for document handling and querying. The collection contains pre-configured requests for each functionality in your FastAPI application. Below is a breakdown of each endpoint included in the collection.

---

### Steps to Use the Postman Collection

1. **Download the Postman collection** from the link provided: [OpenInnovationAi.postman_collection.json](docs/postman-collection/OpenInnovationAi.postman_collection.json).
2. **Import the collection** into Postman:
    - Open Postman and click the "Import" button at the top-left.
    - Select "File" and upload the `.json` file you downloaded.
3. Once the collection is imported, you'll see all the predefined API requests set up for easy testing.
4. You can now start interacting with the API to upload documents, query the system, and test other functionality.

Alternatively, you can use the following link to directly access the Postman collection: [OpenInnovationAi Postman Collection](https://bold-space-802563.postman.co/workspace/eData~a2f91167-f1ef-4ffa-b8fd-0fea21987860/collection/17084316-2c9fffce-fb5f-49d5-b196-416406bae06f?action=share&source=collection_link&creator=17084316)

---

### Example Usage

#### 1. **Health Check**
   - **Request Type**: `GET`
   - **Endpoint**: `http://127.0.0.1:8000/health-check`
   - **Purpose**: This request checks the health of the API. It helps verify if the server is running properly.
   - **How to use**: Simply send a GET request to the `/health-check` endpoint. If the server is running, you should get a response confirming the status.

#### 2. **Get All Documents**
   - **Request Type**: `GET`
   - **Endpoint**: `http://127.0.0.1:8000/api/v1/documents`
   - **Purpose**: This request fetches all the documents stored in the system. 
   - **How to use**: Send a GET request to this endpoint to retrieve a list of all uploaded documents. This will return document metadata such as file names, document IDs, etc.

#### 3. **Document Upload**
   - **Request Type**: `POST`
   - **Endpoint**: `http://127.0.0.1:8000/api/v1/document-upload`
   - **Purpose**: This request allows you to upload a document to the system.
   - **How to use**: 
     - Set the request body to `multipart/form-data`.
     - Attach the file you want to upload (you can choose a local PDF or text file).
     - Send the request to this endpoint to upload the document.
   - **Expected Response**: You’ll receive a confirmation that the document has been successfully uploaded.

#### 4. **Delete Document**
   - **Request Type**: `POST`
   - **Endpoint**: `http://127.0.0.1:8000/api/v1/document-upload` (same as upload but performs deletion in your backend logic)
   - **Purpose**: This request deletes a previously uploaded document from the system.
   - **How to use**:
     - Similar to the document upload request, set the body type to `multipart/form-data`.
     - Attach the file you want to delete (the same document previously uploaded).
     - Send the request, and the document will be deleted.
   - **Expected Response**: You will get a confirmation message that the document has been successfully deleted.

#### 5. **Ask Ollama (Query the System)**
   - **Request Type**: `POST`
   - **Endpoint**: `http://127.0.0.1:8000/api/v1/ask-ollama`
   - **Purpose**: This request sends a question to the system, which will query the stored documents and generate an answer using Ollama and Llama2 embeddings.
   - **How to use**:
     - Set the request body to raw JSON.
     - Include the question you want to ask in the JSON body, for example:
       ```json
       {
         "question": "What is Talabat?"
       }
       ```
     - Send the request, and the response will contain an answer based on the documents in the system.
   - **Expected Response**: You will receive a generated response from the system along with relevant document references (if available).

#### 6. **Clear Data**
   - **Request Type**: `POST`
   - **Endpoint**: `http://127.0.0.1:8000/api/v1/clear-data`
   - **Purpose**: This request clears all the data in the system.
   - **How to use**:
     - Set the request body to raw JSON.
     - Send the request to clear all data in the system.
   - **Expected Response**: You will receive a confirmation message that the data has been successfully cleared.

---
