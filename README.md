# Cryptography Assignment: Primality & Elliptic Curves

This repository contains solutions for the **Cryptography (2025)** programming assignments. It explores two core concepts:
1.  **Primality Testing:** Optimizing Willans' Formula to compute the $n^{th}$ prime.
2.  **Elliptic Curve Cryptography (ECC):** Extracting curve parameters from live SSL certificates.

---

## Part 1: Willans' Formula (PA-1)

### Problem Statement
The goal is to transform a "prime detector" (like Wilson's Theorem) into a "prime computer" (a function that takes $n$ and returns the $n^{th}$ prime number $p_n$). The assignment contrasts the theoretical (but inefficient) Willans' Formula with a practically optimized hybrid approach.

### Approaches Implemented

#### 1. Original Willans' Formula (Theoretical)
* **Logic:** Uses Wilson's Theorem ($(j-1)! \equiv -1 \pmod j$) to check primality and sums over a range up to $2^n$ (Bertrand's Postulate).
* **Time Complexity:** Exponential. The factorial computation in Wilson's Theorem combined with the $2^n$ search space makes this $O(2^{2n})$ or worse practically.
* **Status:** Computationally intractable for $n > 10$.

#### 2. Improved Hybrid Approach (Optimized)
* **Range Reduction (Rosser's Theorem):** Instead of scanning up to $2^n$, we use the tighter upper bound $p_n < n(\ln n + \ln \ln n)$ for $n \ge 6$. This reduces the search space from Exponential to Linear-Logarithmic.
* **Primality Test (Deterministic Miller-Rabin):** Replaces the factorial-heavy Wilson's Theorem with the Deterministic Miller-Rabin test (valid for $n < 2^{64}$). This check is Polylogarithmic $O(\log^4 n)$.
* **Status:** Can compute the $n^{th}$ prime for large $n$ in milliseconds.

### Code Overview (`nth_prime.py`)
The script compares both algorithms via a race/benchmark.

* **`original_willans_formula(n)`**: Implements the naive summation.
* **`hybrid_rosser_dmr(n)`**: Implements the optimized bounds and primality test.
* **`run_benchmark()`**: Runs both methods for various $n$ and calculates the speedup factor.

### Usage
Run the script to see the performance gap:

```bash
python nth_prime.py
```

# PA-2: Elliptic Curve DSA Parameter Extractor

## Project Overview
This project implements a tool to analyze the **Elliptic Curve Digital Signature Algorithm (EC-DSA)** used by modern secure websites (e.g., YouTube, Google). 

As per the assignment requirements, this script connects to a website, retrieves its SSL/TLS certificate, and extracts the mathematical parameters of the underlying elliptic curve, specifically:
* The **Curve Name** (e.g., secp256r1).
* The **Finite Field Characteristic** ($p$).
* The **Curve Coefficients** ($a$ and $b$).
* The **Curve Equation** ($y^2 = x^3 + ax + b \pmod p$).

## Mathematical Background
Elliptic Curve Cryptography (ECC) relies on the algebraic structure of elliptic curves over finite fields. A curve is typically defined by the Weierstrass equation:

$$y^2 \equiv x^3 + ax + b \pmod p$$

Where:
* $p$ is a large prime number (the field characteristic).
* $a$ and $b$ are coefficients defining the curve's shape.
* The security of the system relies on the hardness of the **Elliptic Curve Discrete Logarithm Problem (ECDLP)**.

## Prerequisites
The solution is implemented in **Python 3**. You must install the following dependencies to handle SSL certificates and curve registries:

```bash
pip install cryptography tinyec
