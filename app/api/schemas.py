from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class DeletePDFRequest(BaseModel):
    filename: str
