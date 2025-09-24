# api/routes/chat.py
from fastapi import APIRouter
from api.models.schemas import UserMessage, ChatResponse
from scripts.main import retrieve_and_answer  # Your logic function

router = APIRouter(tags=["chat"])

@router.post(
    "/chat",
    response_model=ChatResponse,
    description="Endpoint to process user messages",
)
async def chat_endpoint(user_message: UserMessage):
    # Call your main function with the user's message
    result = await retrieve_and_answer(user_message.message)
    return ChatResponse(response=result.choices[0].message.content)
