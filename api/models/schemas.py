from pydantic import BaseModel

class UserMessage(BaseModel):
    message: str  # Input from the user

class ChatResponse(BaseModel):
    response: str  # Output