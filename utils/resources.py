import sqlite3
from utils.config import settings

from typing import List, Optional, Tuple
from pydantic import BaseModel

from pinecone import Pinecone

from sentence_transformers import SentenceTransformer

# Database connection
conn = sqlite3.connect(settings.DB_PATH)
def close_database():
    conn.close()
    
    
# UserQuery object
class UserQuery(BaseModel):
    author_name: Optional[str] = None
    title: Optional[str] = None
    keywords: List[str] = []
    semantic_description: Optional[str] = None
    
# Pinecone index connection
pc = Pinecone(api_key=settings.PINECONE_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)
    
# Embedding model
embedd_model = SentenceTransformer(settings.EMBEDDING_MODEL)