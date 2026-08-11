# Statistics Operations — Complexity Analysis
> Student Performance Analysis System | August 2026

## 1. Maximum / Minimum value
Single pass over n records → $O(n)$

$$T(n) = c \cdot n$$
Since the algorithm must inspect every element at least once to determine the maximum or minimum value (as any uninspected element could potentially be the extremum), the lower bound is $\Omega(n)$. Thus, it is tightly bound to $\Theta(n)$.

## 2. Average (mean)
Single pass: sum all scores, divide by n → $O(n)$

$$T(n) = c \cdot n + c'$$
Requires visiting all elements to sum them up, so it is also $\Omega(n)$.

## 3. Count by category
Single pass building a frequency dict → $O(n)$

$$T(n) = c \cdot n$$
Requires categorizing every element, leading to a strict linear time operation. $\Omega(n)$.

## 4. Summary table

| Operation | T(n) | Big-O | Big-Omega |
|-----------|------|-------|-----------|
| Maximum | $T(n) = c \cdot n$ | $O(n)$ | $\Omega(n)$ |
| Minimum | $T(n) = c \cdot n$ | $O(n)$ | $\Omega(n)$ |
| Average | $T(n) = c \cdot n + c'$ | $O(n)$ | $\Omega(n)$ |
| Count by category | $T(n) = c \cdot n$ | $O(n)$ | $\Omega(n)$ |
