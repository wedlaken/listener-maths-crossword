"""
Comprehensive test of listener.py to validate the logic and show prime factors
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
from sympy import isprime
from typing import List, Tuple
from listener import find_solutions, get_prime_factors_with_multiplicity

def test_prime_factorization():
    """Test the prime factorization function with known examples"""
    print("TESTING PRIME FACTORIZATION")
    print("="*50)
    
    test_cases = [
        (12, [2, 2, 3]),
        (15, [3, 5]),
        (16, [2, 2, 2, 2]),
        (17, [17]),
        (18, [2, 3, 3]),
        (20, [2, 2, 5]),
        (25, [5, 5]),
        (27, [3, 3, 3]),
        (30, [2, 3, 5]),
        (100, [2, 2, 5, 5]),
    ]
    
    for number, expected in test_cases:
        result = get_prime_factors_with_multiplicity(number)
        correct = result == expected
        print(f"{number:3d} -> {result} {'✓' if correct else '✗ (expected: ' + str(expected) + ')'}")
    
    return all(get_prime_factors_with_multiplicity(num) == expected for num, expected in test_cases)

def analyze_solutions_for_clue_10():
    """Analyze the solutions for clue 10 (a=4, b=3, c=104)"""
    print("\nANALYZING SOLUTIONS FOR CLUE 10 (a=4, b=3, c=104)")
    print("="*60)
    
    a, b, c = 4, 3, 104
    solutions = find_solutions(a, b, c)
    
    print(f"Found {len(solutions)} solutions: {solutions}")
    print()
    
    print("Detailed analysis of each solution:")
    print("-" * 60)
    print(f"{'Solution':<8} {'Prime Factors':<20} {'Min':<4} {'Max':<4} {'Diff':<4} {'Valid':<6}")
    print("-" * 60)
    
    valid_count = 0
    for solution in solutions:
        factors = get_prime_factors_with_multiplicity(solution)
        min_factor = min(factors)
        max_factor = max(factors)
        diff = max_factor - min_factor
        is_valid = (len(factors) == b and diff == c)
        
        print(f"{solution:<8} {str(factors):<20} {min_factor:<4} {max_factor:<4} {diff:<4} {'✓' if is_valid else '✗'}")
        
        if is_valid:
            valid_count += 1
    
    print("-" * 60)
    print(f"Valid solutions: {valid_count}/{len(solutions)}")
    
    return valid_count == len(solutions)

def test_edge_cases():
    """Test edge cases for the listener logic"""
    print("\nTESTING EDGE CASES")
    print("="*50)
    
    # Test case 1: Single prime factor (b=1)
    print("Test 1: Single prime factor (b=1, c=0)")
    solutions = find_solutions(2, 1, 0)  # 2-digit numbers with 1 prime factor, diff=0
    print(f"Solutions: {solutions}")
    for sol in solutions:
        factors = get_prime_factors_with_multiplicity(sol)
        print(f"  {sol} -> {factors}")
    
    # Test case 2: Small difference
    print("\nTest 2: Small difference (b=2, c=1)")
    solutions = find_solutions(2, 2, 1)  # 2-digit numbers with 2 prime factors, diff=1
    print(f"Solutions: {solutions}")
    for sol in solutions:
        factors = get_prime_factors_with_multiplicity(sol)
        print(f"  {sol} -> {factors}")
    
    # Test case 3: Large difference
    print("\nTest 3: Large difference (b=2, c=100)")
    solutions = find_solutions(3, 2, 100)  # 3-digit numbers with 2 prime factors, diff=100
    print(f"Solutions: {solutions}")
    for sol in solutions:
        factors = get_prime_factors_with_multiplicity(sol)
        print(f"  {sol} -> {factors}")

def verify_listener_logic():
    """Verify the listener logic step by step"""
    print("\nVERIFYING LISTENER LOGIC")
    print("="*50)
    
    # Let's manually check a few solutions for clue 10
    a, b, c = 4, 3, 104
    solutions = find_solutions(a, b, c)
    
    print(f"Checking first few solutions for (a={a}, b={b}, c={c}):")
    
    for i, solution in enumerate(solutions[:5]):  # Check first 5
        print(f"\nSolution {i+1}: {solution}")
        
        # Check it's 4 digits
        digits = len(str(solution))
        print(f"  Digits: {digits} {'✓' if digits == a else '✗'}")
        
        # Get prime factors
        factors = get_prime_factors_with_multiplicity(solution)
        print(f"  Prime factors: {factors}")
        
        # Check number of factors
        factor_count = len(factors)
        print(f"  Factor count: {factor_count} {'✓' if factor_count == b else '✗'}")
        
        # Check difference
        min_factor = min(factors)
        max_factor = max(factors)
        diff = max_factor - min_factor
        print(f"  Min factor: {min_factor}")
        print(f"  Max factor: {max_factor}")
        print(f"  Difference: {diff} {'✓' if diff == c else '✗'}")
        
        # Verify the number actually equals the product of its factors
        product = 1
        for factor in factors:
            product *= factor
        print(f"  Product check: {product} {'✓' if product == solution else '✗'}")

def main():
    """Main test function"""
    print("LISTENER.PY VALIDATION TEST")
    print("="*60)
    
    # Test 1: Prime factorization
    print("Test 1: Prime factorization function")
    factorization_ok = test_prime_factorization()
    print(f"Prime factorization: {'PASS' if factorization_ok else 'FAIL'}")
    
    # Test 2: Analyze clue 10 solutions
    print("\nTest 2: Clue 10 solution analysis")
    clue_10_ok = analyze_solutions_for_clue_10()
    print(f"Clue 10 analysis: {'PASS' if clue_10_ok else 'FAIL'}")
    
    # Test 3: Edge cases
    test_edge_cases()
    
    # Test 4: Manual verification
    verify_listener_logic()
    
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    
    if factorization_ok and clue_10_ok:
        print("✓ All tests passed - listener.py appears to be working correctly")
    else:
        print("✗ Some tests failed - there may be issues with listener.py")

if __name__ == "__main__":
    main() 