"""
Comprehensive test of listener.py to validate the logic and show prime factors
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from sympy import isprime
from typing import List, Tuple
from utils import find_solutions, get_prime_factors_with_multiplicity

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

def test_comprehensive_validation():
    """Comprehensive validation of the listener logic"""
    print("\nCOMPREHENSIVE VALIDATION")
    print("="*50)
    
    # Test various combinations
    test_cases = [
        (2, 1, 0),   # 2 digits, 1 prime factor, diff=0
        (2, 2, 1),   # 2 digits, 2 prime factors, diff=1
        (3, 2, 5),   # 3 digits, 2 prime factors, diff=5
        (3, 3, 10),  # 3 digits, 3 prime factors, diff=10
    ]
    
    all_passed = True
    for a, b, c in test_cases:
        print(f"\nTesting (a={a}, b={b}, c={c}):")
        solutions = find_solutions(a, b, c)
        print(f"  Found {len(solutions)} solutions: {solutions}")
        
        # Validate each solution
        for solution in solutions:
            factors = get_prime_factors_with_multiplicity(solution)
            if len(factors) != b or max(factors) - min(factors) != c:
                print(f"  ✗ {solution} -> {factors} (invalid)")
                all_passed = False
            else:
                print(f"  ✓ {solution} -> {factors}")
    
    return all_passed

def main():
    """Main test function"""
    print("LISTENER MATHS CROSSWORD - LISTENER VALIDATION TEST")
    print("="*60)
    
    try:
        # Test prime factorization
        prime_test_passed = test_prime_factorization()
        
        # Analyze clue 10
        clue_10_passed = analyze_solutions_for_clue_10()
        
        # Test edge cases
        test_edge_cases()
        
        # Comprehensive validation
        comprehensive_passed = test_comprehensive_validation()
        
        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Prime factorization test: {'✓ PASSED' if prime_test_passed else '✗ FAILED'}")
        print(f"Clue 10 analysis: {'✓ PASSED' if clue_10_passed else '✗ FAILED'}")
        print(f"Comprehensive validation: {'✓ PASSED' if comprehensive_passed else '✗ FAILED'}")
        
        if all([prime_test_passed, clue_10_passed, comprehensive_passed]):
            print("\n🎉 ALL TESTS PASSED! Listener logic is working correctly.")
        else:
            print("\n⚠️ Some tests failed. Please check the implementation.")
            
    except Exception as e:
        print(f"Error during listener validation test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 