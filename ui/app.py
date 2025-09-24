import gradio as gr
import requests

from utils.config import settings  # if you want env vars

API_URL = "http://localhost:8000/api/chat"  # FastAPI endpoint

def chat_with_backend(message, history):
    payload = {"message": message}  # matches your UserMessage model
    response = requests.post(API_URL, json=payload)
    data = response.json()  # get the dict from FastAPI JSON
    print(f"data json : {data}")
    answer = data.get("response", "⚠️ No response")

    return answer

# Basic chatbot interface
demo = gr.ChatInterface(
    fn=chat_with_backend,
    title="📚 RAG Chatbot",
    description="Ask me about books and get recommendations.",
    theme="default",  # or "soft", "glass"
    examples=["Recommend me books on AI", "What should I read about philosophy?"],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
