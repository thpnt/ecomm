from scripts.keyword_search import keyword_search, parse_keyword_results
from scripts.semantic_search import semantic_search, parse_semantic_results
from scripts.llm import MistralClient
from prompts.system_prompts import intent_system_prompt, main_system_prompt
from prompts.augmented_prompt import build_augmented_prompt
from utils.resources import conn

mistral_client = MistralClient()

def retrieve_and_answer(user_query: str, client: MistralClient = mistral_client):
    """
    Given a user message and discussion history, perform retrieval and augmented generation. 
    """
    
    # Intent and Keyword detection
    intent_messages = [
        {
            "role": "system",
            "content": intent_system_prompt,
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
    # LLM API Call
    detection_results = client.llm_intent_and_keyword_detection(intent_messages)
    query_struct = detection_results.choices[0].message.parsed
    
    
    # Semantic search
    semantic_results = semantic_search(query_struct.semantic_description)
    semantic_results = parse_semantic_results(semantic_results)
    
    # Keyword search
    cursor = conn.cursor()
    keyword_results = keyword_search(query_struct, cursor)
    keyword_results = parse_keyword_results(keyword_results)
    
    # Build augmented prompt
    instructions_prompt = build_augmented_prompt(user_query, semantic_results, keyword_results)
    aug_messages = [
        {
            "role": "system",
            "content": main_system_prompt,
        },
        {
            "role": "user",
            "content": instructions_prompt
        }
    ]
    
    
    # LLM API CALL
    aug_results = client.llm_augmented_generation(aug_messages)
    
    return aug_results
    
    
    
    

    
    
    