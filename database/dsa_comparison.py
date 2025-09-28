# dsa/dsa_comparison.py
import time
import random
import json
from .parser import parse_xml_to_json # Assuming parser.py is in the same directory

# Load the data (you must run parser.py first)
try:
    with open('transactions.json', 'r') as f:
        TRANSACTIONS_LIST = json.load(f)
except FileNotFoundError:
    print("FATAL: transactions.json not found. Run parser.py first.")
    TRANSACTIONS_LIST = []

# Create the dictionary structure
TRANSACTIONS_DICT = {t['id']: t for t in TRANSACTIONS_LIST}

# Select IDs to search (ensure they exist and are >= 20)
# Adjust COUNT based on your dataset size, ensuring >= 20.
COUNT = min(len(TRANSACTIONS_LIST), 50) 
SEARCH_IDS = random.sample(list(TRANSACTIONS_DICT.keys()), COUNT)

def linear_search(data_list, search_id):
    """Scans a list linearly to find a record by ID."""
    for record in data_list:
        if record['id'] == search_id:
            return record
    return None

def dictionary_lookup(data_dict, search_id):
    """Uses dictionary key access to find a record by ID."""
    return data_dict.get(search_id)

# --- Comparison Logic ---
def run_comparison():
    if not TRANSACTIONS_LIST:
        return

    print(f"--- Running search comparison for {COUNT} records ---")

    # 1. Linear Search Time
    start_time = time.perf_counter()
    for _id in SEARCH_IDS:
        linear_search(TRANSACTIONS_LIST, _id)
    end_time = time.perf_counter()
    linear_time = (end_time - start_time) * 1000 # Time in milliseconds

    # 2. Dictionary Lookup Time
    start_time = time.perf_counter()
    for _id in SEARCH_IDS:
        dictionary_lookup(TRANSACTIONS_DICT, _id)
    end_time = time.perf_counter()
    dict_time = (end_time - start_time) * 1000 # Time in milliseconds

    print(f"\nResults (Time in milliseconds for {COUNT} lookups):")
    print(f"Linear Search Time: {linear_time:.6f} ms")
    print(f"Dictionary Lookup Time: {dict_time:.6f} ms")
    print(f"Dictionary Lookup is {linear_time / dict_time:.2f} times faster.")
    
    # Store results in a file or print for the report
    with open('dsa_results.txt', 'w') as f:
        f.write(f"Count: {COUNT}\n")
        f.write(f"Linear Search Time (ms): {linear_time:.6f}\n")
        f.write(f"Dictionary Lookup Time (ms): {dict_time:.6f}\n")
        f.write(f"Speedup Factor: {linear_time / dict_time:.2f}\n")

if __name__ == '__main__':
    run_comparison()
