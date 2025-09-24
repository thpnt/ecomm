from typing import Tuple, List


def build_augmented_prompt(user_query: str, semantic_results: List, keyword_results: Tuple[List, List]):
    
    """
    This function dynamically build the LLM prompt to generate the augmented answer.
    """
    
    # Unpack keyword results into exact matches and keyword matches
    exact_matches, keyword_matches = keyword_results

    # Initialize the sections for each type of match
    exact_matches_section = ""
    semantic_matches_section = ""
    keyword_matches_section = ""

    # Function to format book information
    def format_book_info(books):
        formatted_books = []
        for book_list in books:
            for book in book_list:
                # Ensure the book tuple has the expected number of elements
                if isinstance(book, tuple) and len(book) == 5:
                    author_name, title, description, price, avg_rating = book
                    # Handle potential None values or empty strings
                    author_name = author_name or "Unknown"
                    title = title or "Unknown"
                    description = description or "No description available"
                    price = price or "Not specified"
                    avg_rating = avg_rating or "Not rated"

                    formatted_book = (
                        f"Title: {title}\n"
                        f"Author: {author_name}\n"
                        f"Average Rating: {avg_rating}\n"
                        f"Price: {price}\n"
                        f"Description: {description}\n"
                    )
                else:
                    formatted_book = f"Invalid book info: {book}"
                formatted_books.append(formatted_book)
        return "\n".join(formatted_books)

    # Format exact matches
    if exact_matches:
        exact_matches_section = "1. Exact Matches:\n" + format_book_info(exact_matches)
    else:
        exact_matches_section = "1. Exact Matches: None"

    # Format semantic matches
    if semantic_results:
        semantic_matches_section = "2. Semantic Search Matches:\n" + format_book_info([semantic_results])
    else:
        semantic_matches_section = "2. Semantic Search Matches: None"

    # Format keyword matches
    if keyword_matches:
        keyword_matches_section = "3. Keyword Search Matches:\n" + format_book_info(keyword_matches)
    else:
        keyword_matches_section = "3. Keyword Search Matches: None"

    # Combine all sections
    retrieved_info = f"{exact_matches_section}\n\n{semantic_matches_section}\n\n{keyword_matches_section}"

    # Full prompt
    prompt = f"Using the retrieved information, provide a helpful and concise response to the user's query: {user_query}. \n Here is the information retrieved based on the user's query:\n\n{retrieved_info}"

    return prompt
