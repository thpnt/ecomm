from mistralai import Mistral
from typing import List, Dict
from utils.config import settings
from utils.resources import UserQuery

class MistralClient:
    """
    Wrapper for Mistral API for different types of api CALLS
    """
    def __init__(self, client=Mistral(api_key=settings.MISTRAL_API_KEY)):
        self.client = client
        
    def llm_intent_and_keyword_detection(self, messages,
                                         model: str = "mistral-tiny-latest",
                                         max_tokens: int = 256):
    
        chat_response = self.client.chat.parse(
            model=model,
            messages=messages,
            response_format=UserQuery,
            max_tokens = max_tokens
        )

        return chat_response
    
    
    def llm_augmented_generation(self,
                                 messages, model: str = "mistral-small-latest"):
        
        chat_response = self.client.chat.complete(
            model=model,
            messages=messages
        )
        
        return chat_response
    
    
    
        