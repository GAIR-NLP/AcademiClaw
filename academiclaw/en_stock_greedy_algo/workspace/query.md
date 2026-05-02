# Task: Stock Trading Maximum Profit (Regret-Based Greedy)

## 1. Problem Description
Buy and sell stocks over $n$ days, with a transaction fee $C$ charged for each sale. At most one share can be traded per day. Find the maximum profit.

### Input Format
- First line: $n$ and $C$ ($1 \le n \le 10^5$, $0 \le C \le 10^6$)
- Second line: $n$ integers $a_i$ ($1 \le a_i \le 10^6$)

### Output Format
- A single integer on one line representing the maximum profit.

## 2. Core Approach Guide
- **Context reference**: `./context/Logic_hint.txt` contains the basic idea behind the regret-based greedy approach.
- **Key questions**:
    1. If you buy today and sell at a higher price in the future, the profit is `sell_price - buy_price - C`.
    2. If we buy on day `i`, sell on day `j`, and later discover that day `k` has a higher price (`k > j`), how should we "undo" (regret)?
        - Ideally: buy on day `i`, sell on day `k`.
        - This is equivalent to executing the `(i, j)` transaction, then undoing it and executing the `(i, k)` transaction.
        - **Think**: On day `j`, how can we both settle the `(i, j)` profit and reserve a "virtual buy point" for a future day `k`? What is the cost of this virtual buy point?

- **Algorithm hints**:
    - Use a **min-heap (priority_queue)** to maintain all **potential buy costs**.
    - Iterate through each day's `price`:
        - If `price - C` is greater than the minimum cost at the top of the heap, there is a profit opportunity.
        - At this point, execute the trade and think about how to update the heap to support future "regret" operations.

## 3. Output Requirements
- Provide a complete **C++ code** implementation, saved as **`solution.cpp`**.
- **Note**: All profit and price calculations should use `long long`.
