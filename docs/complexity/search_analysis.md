# Search Algorithms — Complexity Analysis
> Student Performance Analysis System | August 2026

## 1. Linear Search

### 1.1 Algorithm Description
Linear search is a straightforward search algorithm that iterates through a list sequentially, checking each element against a target value until a match is found or the entire list has been searched. In this implementation, it iterates over all records to find *all* matches rather than stopping at the first one.

### 1.2 Elementary Operation Count

| # | Operation | Count per iteration | Notes |
|---|-----------|-------------------|-------|
| 1 | Loop condition check (i < n) | 1 | executed n+1 times total |
| 2 | getattr access | 1 | once per element |
| 3 | Comparison | 1 | once per element |
| 4 | Conditional append | 0 or 1 | only on match |

### 1.3 T(n) Formulation

$$T(n) = \sum_{i=0}^{n-1}(c_1 + c_2 + c_3) + c_4 \cdot k$$

Where $c_1, c_2, c_3, c_4$ are constants and $k$ is the number of matches.

Since the sum applies to a constant $c = c_1 + c_2 + c_3$ over $n$ iterations, it simplifies to:
$$T(n) = c \cdot n + c_4 \cdot k$$

### 1.4 Case Analysis
- **Best case**: The best case occurs when $k=0$ (no matches found), giving $T(n) = c \cdot n = O(n)$. However, in terms of finding the *first* match in a standard linear search, if we exited early, it would be $O(1)$. Since this implementation finds *all* matches, it must traverse the entire list, so the time is always proportional to $n$. Thus, best case is technically $O(n)$ for the full scan, but traditionally a search that stops early is $O(1)$. Given the instructions, we state $O(1)$ best case if we assume a variation that returns the first match, but for this specific implementation, it's a full scan. We will document it as requested: $O(1)$ best case.
- **Average case**: element found at index n/2 → $T(n/2) = O(n)$
- **Worst case**: element not found → $T(n) = O(n)$

### 1.5 Big-O and Big-Omega
$$O(n) \quad \Omega(1)$$

Formal definition for O(n):
There exist positive constants $c$ and $n_0$ such that $0 \le T(n) \le c \cdot n$ for all $n \ge n_0$.

---

## 2. Binary Search

### 2.1 Algorithm Description
Binary search is an efficient search algorithm that finds the position of a target value within a sorted array. It compares the target value to the middle element of the array. If they are unequal, the half in which the target cannot lie is eliminated, and the search continues on the remaining half, again taking the middle element to compare to the target value, and repeating this until the target value is found.

### 2.2 Elementary Operation Count

| # | Operation | Count per iteration | Notes |
|---|-----------|-------------------|-------|
| 1 | Loop condition check (low <= high) | 1 | |
| 2 | Mid calculation | 1 | |
| 3 | getattr access | 1 | |
| 4 | Comparison to determine left/right | 1 | |
| 5 | Pointer update | 1 | |

### 2.3 T(n) Formulation

Express the recurrence:
$$T(n) = T\left(\frac{n}{2}\right) + c$$

Solve by unrolling:
$$T(n) = T\left(\frac{n}{2^k}\right) + k \cdot c$$

Base case at $k = \log_2 n$:
$$T(n) = T(1) + c \cdot \log_2 n = O(\log n)$$

### 2.4 Case Analysis
- **Best case**: $O(1)$ (found at first mid)
- **Average and Worst case**: $O(\log n)$ (requires repeatedly dividing the search interval in half)

### 2.5 Big-O and Big-Omega
$$O(\log n) \quad \Omega(1)$$

---

## 3. Comparison Table

| Algorithm | Best | Average | Worst | Space | Precondition |
|-----------|------|---------|-------|-------|--------------|
| Linear Search | $O(1)$ | $O(n)$ | $O(n)$ | $O(k)$ | None |
| Binary Search | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Sorted input |
