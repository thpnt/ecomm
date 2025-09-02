import json
import pandas as pd
import os


# Function to load a subset of data from a JSONL file of the Amazon Reviews dataset
def load_n_rows_from_jsonl(file_path: str, n: int) -> list:
    """
    Load the first n rows from a JSONL file.
    """

    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i >= n:
                break
            rows.append(json.loads(line))
    
    return rows




