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

### Running the System
1. **Clone the Repository**
   ```bash
   git clone https://github.com/atmaneayoubdev/OpenInnovationAi.git
   cd OpenInnovationAi


### Start the Ollama Container

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
docker exec -it ollama ollama pull embed
```

Verify the models are downloaded by listing the available models:
```bash
docker exec -it ollama ollama list
```


### Start the Ollama Container
Build and run the FastAPI container:

```bash
docker build -t open_innovation_ai .
docker run -d -p 8000:8000 --name open_innovation_ai open_innovation_ai
```

### Access the API Documentation
Swagger UI: http://localhost:8000/docs

