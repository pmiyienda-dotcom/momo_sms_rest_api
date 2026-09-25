"""
DSA Module: Linear Search vs Dictionary Lookup on MoMo Transactions
Demonstrates O(N) vs O(1) search efficiency on real transaction data.
"""
import json
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "api", "mock_db.json")


def load_transactions():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def linear_search(tx_list, target_id):
    """O(N) — scans every record sequentially until match is found."""
    for tx in tx_list:
        if tx["id"] == target_id:
            return tx
    return None


def dictionary_lookup(tx_dict, target_id):
    """O(1) — direct key access via hash map (Python dict)."""
    return tx_dict.get(target_id)


if __name__ == "__main__":
    transactions = load_transactions()
    tx_dict = {t["id"]: t for t in transactions}

    # Worst-case target: last record
    target_id = transactions[-1]["id"]

    start = time.perf_counter()
    result_linear = linear_search(transactions, target_id)
    linear_time = time.perf_counter() - start

    start = time.perf_counter()
    result_dict = dictionary_lookup(tx_dict, target_id)
    dict_time = time.perf_counter() - start

    print(f"Records in dataset         : {len(transactions)}")
    print(f"Target ID                  : {target_id}")
    print(f"Linear Search O(N)         : {linear_time:.8f} seconds")
    print(f"Dictionary Lookup O(1)     : {dict_time:.8f} seconds")
    if dict_time > 0:
        print(f"Speedup                    : {linear_time / dict_time:.1f}x faster")
    print(f"\nFound record: {json.dumps(result_dict, indent=2)}")
