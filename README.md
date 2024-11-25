# Technical Challenge for Open Innovation AI
A document-based GPT system designed to answer questions based on internal documents. Built using FastAPI, Ollama, and LangChain, it provides short, precise, and well-sourced answers with links to document locations.

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
   git clone https://github.com/<your-username>/Technical-Challenge-for-Open-Innovation-AI.git
   cd Technical-Challenge-for-Open-Innovation-AI
