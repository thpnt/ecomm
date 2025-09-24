from typing import Tuple
from utils.resources import conn, UserQuery
from utils.config import settings


# Establish cursor in database
cursor = conn.cursor()



def build_fts_queries(search_request: UserQuery) -> Tuple[str, str]:
    """
    This function builds two FTS search queries:
        - One for title and author name
        - One for description keywords
    """
    # Query part for title and author name
    title_author_query_parts = []
    if search_request.author_name:
        title_author_query_parts.append(f'author_name:"{search_request.author_name}"')
    if search_request.title:
        title_author_query_parts.append(f'title:"{search_request.title}"')
    title_author_query = " OR ".join(title_author_query_parts) if title_author_query_parts else "*"

    # Query part for keywords in description
    keyword_query_parts = []
    if search_request.keywords:
        keyword_parts = []
        for keyword in search_request.keywords:
            keyword_parts.append(f'description:"{keyword}"')
        keyword_query_parts.append(" OR ".join(keyword_parts))
    keyword_query = " OR ".join(keyword_query_parts) if keyword_query_parts else "*"

    return title_author_query, keyword_query

def keyword_search(search_request: UserQuery, cursor) -> Tuple:
    # Build the FTS queries
    title_author_query, keyword_query = build_fts_queries(search_request)

    # Function to execute a query and return a set of results
    def execute_query(fts_query):
        query = "SELECT *, rank FROM books_fts WHERE books_fts MATCH ? ORDER BY rank ASC LIMIT 5"
        cursor.execute(query, (fts_query,))
        return cursor.fetchall()

    # Execute both queries
    title_author_results, keyword_results = None, None
    if search_request.author_name:
        title_author_results = execute_query(title_author_query)
    if search_request.keywords:
        keyword_results = execute_query(keyword_query)

    return title_author_results, keyword_results



def parse_keyword_results(results: tuple, conn=conn)->tuple:
    """
    This function takes the sqlite keyword search results and retrieve the corresponding books information in the database.
    """
    cache = []
    rows = ([], [])
    # Author Name exact match
    if results[0]: # if we found exact matches
        for match in results[0]:
            if match[0] in cache:
                continue
            else:
                cursor = conn.cursor() # Connect to db
                cursor.execute("SELECT author_name, title, description, price, avg_rating FROM books WHERE uuid == ?", (match[0],)) # match[0] is the uuid
                row = cursor.fetchall()
                rows[0].append(row)
                cache.append(match[0])
        
    # Keyword matches
    if results[1]:
        for match in results[1]:
            if match[0] in cache:
                continue
            else:
                cursor = conn.cursor() # Connect to db
                cursor.execute("SELECT author_name, title, description, price, avg_rating FROM books WHERE uuid == ?", (match[0],)) # match[0] is the uuid
                row = cursor.fetchall()
                rows[1].append(row)
                cache.append(match[0])
            
    return rows