import math
from sympy import isprime
from typing import List, Tuple

def get_prime_factors_with_multiplicity(n: int) -> List[int]:
    """Returns a list of prime factors including multiplicity, e.g., 12 -> [2, 2, 3]"""
    factors = []
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0 and isprime(i):
            factors.append(i)
            n //= i
        if n == 1:
            break
    if n > 1:
        factors.append(n)
    return factors

def find_solutions(a: int, b: int, c: int) -> Tuple[int, ...]:
    """Finds all numbers with:
    - a digits
    - b prime factors (with multiplicity)
    - difference c between largest and smallest prime factor
    """
    start = 10**(a - 1)
    end = 10**a

    solutions = []

    for n in range(start, end):
        factors = get_prime_factors_with_multiplicity(n)
        if len(factors) == b and max(factors) - min(factors) == c:
            solutions.append(n)

    return tuple(solutions)

def main() -> None:
    a = int(input("Enter number of digits (a): "))
    b = int(input("Enter number of prime factors (b): "))
    c = int(input("Enter difference between largest and smallest prime factor (c): "))

    results = find_solutions(a, b, c)
    print(f"Solutions for ({a}, {b}, {c}): {results}")

if __name__ == "__main__":
    main()
