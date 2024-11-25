from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Local document folder for storage
    DOCUMENTS_FOLDER: str = Field('app/documents', env='DOCUMENTS_FOLDER')

    # Path to the vector store
    VECTORSTORE_PATH: str = Field('app/vectorstore', env='VECTORSTORE_PATH')

    # Enable or disable debug mode
    DEBUG: bool = Field(True, env='DEBUG')

    # Host for OLLAMA
    OLLAMA_HOST: str = Field('host.docker.internal', env='OLLAMA_HOST')

    # Port for OLLAMA
    OLLAMA_PORT: int = Field(11434, env='OLLAMA_PORT')

    # Path to the Chroma vector store
    CHROMA_PATH: str = Field('app/vectorstore/chroma', env='CHROMA_PATH')

    # Path to the data
    DATA_PATH: str = Field('app/documents', env='DATA_PATH')

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Instantiate the settings object to use in the application
settings = Settings()

# This should print the values from the .env file if correctly loaded
print(settings.DOCUMENTS_FOLDER)
print(settings.VECTORSTORE_PATH)
print(settings.DEBUG)
print(settings.OLLAMA_HOST)
print(settings.OLLAMA_PORT)
print(settings.CHROMA_PATH)
print(settings.DATA_PATH)
