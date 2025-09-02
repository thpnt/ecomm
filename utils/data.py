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
def populate_dataframe_from_json(data, df: pd.DataFrame) -> None:
    """
    Populates a DataFrame with values extracted from an Amazon Book Reviews JSON entry.

    Args:
        data (Dict[str, Any]): A dictionary containing book data from Amazon Book Reviews.
        df (pd.DataFrame): The DataFrame to be populated with the book data.
    """
    # Instance
    entry = {}
   
    # Populate each field
    entry["uuid"] = None
    entry["title"] = data.get("title")
    entry["description"] = " ".join(data.get("features", []))
    entry["author_name"] = data.get("author", {}).get("name") if (data.get("author", {})) else None
    entry["author_about"] = " ".join(data.get("author", {}).get("about")) if (data.get("author", {})) else None
    entry["avg_rating"] = data.get("average_rating")
    entry["rating_number"] = data.get("rating_number")
    entry["price"] = data.get("price")
    entry["categories"] = " ".join(data.get("categories", []))
    
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

