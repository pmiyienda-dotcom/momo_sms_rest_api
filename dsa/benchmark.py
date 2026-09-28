import time
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "api", "mock_db.json")
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "benchmark_results.txt")


def linear_search(tx_list, target_id):
    for tx in tx_list:
        if tx["id"] == target_id:
            return tx
    return None


def dictionary_lookup(tx_dict, target_id):
    return tx_dict.get(target_id)


def run_benchmark():
    with open(DB_PATH, "r") as f:
        transactions_list = json.load(f)

    # Use first 20 records minimum as required, but benchmark full dataset
    sample = transactions_list[:20]
    print(f"Total records loaded      : {len(transactions_list)}")
    print(f"Sample used for display   : {len(sample)} records")

    # Build dict keyed by integer id
    transactions_dict = {t["id"]: t for t in transactions_list}

    # Target: last record in full list 
    target_id = transactions_list[-1]["id"]
    iterations = 10000

    # Linear Search Timing
    start = time.perf_counter()
    for _ in range(iterations):
        linear_search(transactions_list, target_id)
    linear_duration = time.perf_counter() - start

    # Dictionary Lookup Timing
    start = time.perf_counter()
    for _ in range(iterations):
        dictionary_lookup(transactions_dict, target_id)
    dict_duration = time.perf_counter() - start

    speedup = linear_duration / dict_duration if dict_duration > 0 else float("inf")

    lines = [
        "=== MoMo DSA Efficiency Benchmark ===",
        f"Dataset Size               : {len(transactions_list)} records",
        f"Iterations per method      : {iterations}",
        f"Target ID (worst-case)     : {target_id}",
        "",
        f"Linear Search  O(N) Time   : {linear_duration:.6f} seconds",
        f"Dictionary     O(1) Time   : {dict_duration:.6f} seconds",
        f"Speedup Factor             : {speedup:.2f}x faster with dictionary",
        "",
        "--- Sample of first 20 records used in comparison ---",
    ]
    for t in sample:
        lines.append(f"  ID={t['id']}  amount={t.get('amount','N/A')}  type={t.get('type','N/A')}  sender={t.get('sender','N/A')}")

    output = "\n".join(lines)
    print(output)

    with open(RESULTS_PATH, "w") as f:
        f.write(output + "\n")
    print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    run_benchmark()