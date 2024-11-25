FROM python:3.11-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Uninstall all currently installed packages if any
RUN pip freeze | xargs -r pip uninstall -y

# Install required packages
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY ./app /code/app
COPY .env /code/.env  

# Set environment variables
ENV CHROMA_PATH=/code/app/vectorstore/chroma
ENV DATA_PATH=/code/app/documents
ENV OLLAMA_HOST=host.docker.internal
ENV OLLAMA_PORT=11434
# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]