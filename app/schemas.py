from typing import Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant']
    content: str

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description='New user message')
    history: list[ChatMessage] = Field(default_factory=list)

class ChatResponse(BaseModel):
    answer: str
    tool_calls: list[str] = Field(default_factory=list)