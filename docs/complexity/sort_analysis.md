# Sorting Algorithms — Complexity Analysis
> Student Performance Analysis System | August 2026

## 1. Bubble Sort

### 1.1 Algorithm Description
Bubble Sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. It includes an early-exit optimization that stops the algorithm if a full pass is completed without any swaps.

### 1.2 Elementary Operation Count

Count operations for the worst case (no early exit):
- Outer loop runs n-1 times
- Inner loop runs n-1, n-2, ..., 1 times
- Each inner iteration: 1 comparison + up to 3 swap ops + 1 flag update

### 1.3 T(n) Formulation

Worst case (no swaps optimization):
$$T(n) = \sum_{i=0}^{n-2} \sum_{j=0}^{n-2-i} (c_1 + c_2 + c_3)$$

$$T(n) = c \cdot \sum_{i=0}^{n-2}(n-1-i) = c \cdot \frac{n(n-1)}{2}$$

$$T(n) = O(n^2)$$

Best case with early exit (already sorted):
$$T(n) = c \cdot n = O(n)$$

### 1.4 Case Analysis
- **Best**: $O(n)$ — one pass, no swaps, early exit triggered
- **Average**: $O(n^2)$
- **Worst**: $O(n^2)$ — reverse sorted input

### 1.5 Big-O and Big-Omega
$$O(n^2) \quad \Omega(n)$$

---

## 2. Selection Sort

### 2.1 Algorithm Description
Selection Sort is an in-place comparison sorting algorithm. It divides the input list into two parts: a sorted sublist of items which is built up from left to right, and a sublist of the remaining unsorted items. It proceeds by finding the smallest element in the unsorted sublist, exchanging (swapping) it with the leftmost unsorted element, and moving the sublist boundaries one element to the right.

### 2.2 Elementary Operation Count

- Outer loop: n-1 iterations
- Inner loop: n-1-i iterations per outer step
- Each inner iteration: 1 attribute access + 1 comparison

### 2.3 T(n) Formulation

$$T(n) = \sum_{i=0}^{n-2} \sum_{j=i+1}^{n-1} c = c \cdot \frac{n(n-1)}{2}$$

$$T(n) = O(n^2)$$

No early exit exists → best, average and worst are all $O(n^2)$.

### 2.4 Case Analysis
- **Best**: $O(n^2)$
- **Average**: $O(n^2)$
- **Worst**: $O(n^2)$

### 2.5 Big-O and Big-Omega
$$O(n^2) \quad \Omega(n^2)$$

---

## 3. Insertion Sort

### 3.1 Algorithm Description
Insertion Sort is a simple sorting algorithm that builds the final sorted array one item at a time. It iterates, consuming one input element each repetition, and growing a sorted output list. At each iteration, it removes one element from the input data, finds the location it belongs within the sorted list, and inserts it there.

### 3.2 Elementary Operation Count

- Outer loop: n-1 iterations
- Inner while loop: 0 to i iterations depending on input order
- Each inner iteration: 1 comparison + 1 shift

### 3.3 T(n) Formulation

Best case (sorted input — inner loop never executes):
$$T(n) = c_1 \cdot (n-1) = O(n)$$

Worst case (reverse sorted — inner loop runs i times each outer step):
$$T(n) = \sum_{i=1}^{n-1} i \cdot c = c \cdot \frac{n(n-1)}{2} = O(n^2)$$

### 3.4 Case Analysis
- **Best**: $O(n)$
- **Average**: $O(n^2)$
- **Worst**: $O(n^2)$

### 3.5 Big-O and Big-Omega
$$O(n^2) \quad \Omega(n)$$

---

## 4. Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable | Early Exit |
|-----------|------|---------|-------|-------|--------|------------|
| Bubble Sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| Selection Sort | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | No |
| Insertion Sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | No |
