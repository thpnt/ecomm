from utils.resources import index, embedd_model, conn
from utils.config import settings

def semantic_search(query: str, index=index, embedd_model=embedd_model, top_k: int = 5,
                    include_metadata: bool = True,
                    include_values: bool = False):
    """
    Performs semantic search with cosine similarity given a query, pinecone index and embedding model.
    """
    # Encode query
    query_vector = embedd_model.encode(query)
    query_vector = query_vector.tolist()
    
    return index.query(
                namespace=settings.PINECONE_INDEX_NAME,
                vector = query_vector,
                top_k=top_k,
                include_metadata=include_metadata,
                include_values=include_values
            )
    
    
    
def parse_semantic_results(results: dict, conn=conn)->list:
    """
    This function takes the pinecone semantic search results and retrieve the corresponding books information in the database.
    """
    cache = []
    rows = []
    
    for match in results["matches"]:
        if match.metadata["original_id"] in cache:
            continue
        else:
            cursor = conn.cursor() # Connect to db
            cursor.execute("SELECT author_name, title, description, price, avg_rating FROM books WHERE uuid == ?", (match.metadata["original_id"],))
            row = cursor.fetchall()
            rows.append(row[0])
            cache.append(match.metadata["original_id"])
    
    del cache
    return rows