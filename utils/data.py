import json
import pandas as pd

def load_idx_from_jsonl(file_path: str, idx: list) -> list:
    """
    Load rows corresponding to the indices passed from a JSONL file.
    """

    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i in idx:
                rows.append(json.loads(line))
            else:
                continue
    
    return rows


# Function to populate a dataframe with books info from JSON
def safe_join(value, sep=" "):
    """Convert value into a string safely.
    - If list/tuple → join elements as strings
    - If str → return as is
    - If dict → join values
    - Else → return None
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        return sep.join(str(v) for v in value if v is not None)
    if isinstance(value, dict):
        return sep.join(str(v) for v in value.values() if v is not None)
    if isinstance(value, str):
        return value
    return str(value)  # fallback (e.g. int/float)

def populate_dataframe_from_json(data, df: pd.DataFrame) -> None:
    """
    Populates a DataFrame with values extracted from an Amazon Book Reviews JSON entry.

    Args:
        data (Dict[str, Any]): A dictionary containing book data from Amazon Book Reviews.
        df (pd.DataFrame): The DataFrame to be populated with the book data.
    """
    
    # Populate each column
    entry = {}
    
    
    entry["uuid"] = None  # to be filled later if needed

    entry["title"] = data.get("title")
    entry["description"] = safe_join(data.get("features"))
    
    author = data.get("author") or {}
    entry["author_name"] = author.get("name") if isinstance(author, dict) else None
    entry["author_about"] = safe_join(author.get("about") if isinstance(author, dict) else None)

    entry["avg_rating"] = data.get("average_rating")
    entry["rating_number"] = data.get("rating_number")
    entry["price"] = data.get("price")
    entry["categories"] = safe_join(data.get("categories"))
    
    # Ensure all DataFrame columns are present in entry, fill missing with None
    for col in df.columns:
        if col not in entry:
            entry[col] = None
    # Add the entry as a new row
    df.loc[len(df)] = [entry[col] for col in df.columns]


def replace_none_with_empty_string(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace None/NaN values with empty string, but only in string/object columns.
    """
    # Select only string/object columns
    string_cols = df.select_dtypes(include=["object", "string"]).columns
    
    # Replace None/NaN with "" in those columns
    df[string_cols] = df[string_cols].fillna("")
    
    return df


def chunk_text(text, tokenizer, chunck_size: int = 256, step_size: int = 230):
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    
    chunks = []
    
    for i in range(0, len(token_ids), step_size):
        chunk = token_ids[i:i+chunck_size] if (i+chunck_size<=len(token_ids)) else token_ids[i:]
        chunks.append(tokenizer.decode(chunk))
        
    return chunks