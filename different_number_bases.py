"""
Tamaki's Lemma: Base Invariance Analysis
=========================================

Testing whether Tamaki's Lemma holds across different number bases.

If the lemma is base-invariant, it reveals a universal mathematical
structure independent of human-chosen notation (decimal).

If it varies by base, it might reveal special properties of certain bases.

Hypothesis: The structural relationship a₁ = ⌊d_N / d_p⌋ should hold
regardless of the base used to count digits.
"""

import math

def digit_count(n, base=10):
    """Count digits of n in given base."""
    if n <= 0:
        return 1
    return int(math.log(n, base)) + 1

def continued_fraction(x, depth=10):
    """Compute continued fraction expansion."""
    result = []
    for _ in range(depth):
        if abs(x) < 1e-10:
            break
        a = int(x)
        result.append(a)
        x = x - a
        if abs(x) < 1e-10:
            break
        x = 1 / x
    return result

def verify_tamaki_for_base(base, test_cases):
    """
    Verify Tamaki's Lemma for a specific base.
    
    Returns match rate and details.
    """
    results = []
    
    for N, p in test_cases:
        # Compute digit counts in the given base
        d_N = digit_count(N, base)
        d_p = digit_count(p, base)
        
        if d_p >= d_N or d_p == 0:
            continue
        
        # Digit ratio
        ratio = d_p / d_N
        
        # Continued fraction
        cf = continued_fraction(ratio, depth=8)
        
        # Tamaki's prediction
        a1_expected = d_N // d_p
        a1_actual = cf[1] if len(cf) > 1 else 0
        
        match = (a1_expected == a1_actual)
        
        results.append({
            'N': N,
            'p': p,
            'd_N': d_N,
            'd_p': d_p,
            'ratio': ratio,
            'cf': cf,
            'a1_expected': a1_expected,
            'a1_actual': a1_actual,
            'match': match
        })
    
    return results

def run_base_comparison():
    """Compare Tamaki's Lemma across multiple bases."""
    
    # Test cases: various semiprimes and their factors
    # Using actual numbers to test across bases
    test_cases = [
        (10**20, 10**7),      # 21 digits vs 8 digits (base 10)
        (10**50, 10**20),     # 51 vs 21
        (10**77, 10**30),     # 78 vs 31
        (10**100, 10**33),    # 101 vs 34
        (2**128, 2**50),      # RSA-like
        (2**256, 2**100),     # Large crypto
        (2**1024, 2**400),    # RSA-1024
        (10**154, 10**60),    # 155 vs 61
        (7**50, 7**20),       # Base 7 native
        (16**32, 16**12),     # Hex native
    ]
    
    bases = [2, 3, 7, 10, 12, 16, 60]  # Binary, ternary, sept, decimal, duodecimal, hex, sexagesimal
    
    print("=" * 80)
    print("TAMAKI'S LEMMA: BASE INVARIANCE ANALYSIS")
    print("=" * 80)
    print("\nHypothesis: a₁ = ⌊d_N / d_p⌋ holds regardless of number base")
    print("=" * 80)
    
    base_results = {}
    
    for base in bases:
        base_name = {
            2: "Binary", 3: "Ternary", 7: "Septenary", 
            10: "Decimal", 12: "Duodecimal", 16: "Hexadecimal",
            60: "Sexagesimal"
        }.get(base, f"Base-{base}")
        
        results = verify_tamaki_for_base(base, test_cases)
        
        if not results:
            continue
            
        matches = sum(1 for r in results if r['match'])
        total = len(results)
        rate = matches / total * 100 if total > 0 else 0
        
        base_results[base] = {
            'name': base_name,
            'matches': matches,
            'total': total,
            'rate': rate,
            'details': results
        }
        
        print(f"\n{'='*60}")
        print(f"BASE {base} ({base_name})")
        print(f"{'='*60}")
        print(f"{'d_N':>6} {'d_p':>6} {'ratio':>8} {'⌊d_N/d_p⌋':>10} {'a₁':>6} {'Match':>6}")
        print("-" * 60)
        
        for r in results:
            symbol = "✓" if r['match'] else "✗"
            print(f"{r['d_N']:>6} {r['d_p']:>6} {r['ratio']:>8.4f} "
                  f"{r['a1_expected']:>10} {r['a1_actual']:>6} {symbol:>6}")
        
        print(f"\nMatch rate: {rate:.1f}% ({matches}/{total})")
    
    # Summary comparison
    print("\n" + "=" * 80)
    print("SUMMARY: BASE COMPARISON")
    print("=" * 80)
    print(f"{'Base':>12} {'Name':>15} {'Match Rate':>12} {'Matches':>10}")
    print("-" * 50)
    
    all_perfect = True
    for base, data in base_results.items():
        rate_str = f"{data['rate']:.1f}%"
        print(f"{base:>12} {data['name']:>15} {rate_str:>12} {data['matches']}/{data['total']:>7}")
        if data['rate'] < 100:
            all_perfect = False
    
    print("=" * 80)
    
    if all_perfect:
        print("\n🎯 RESULT: Tamaki's Lemma is BASE-INVARIANT!")
        print("   The relationship a₁ = ⌊d_N / d_p⌋ holds in ALL tested bases.")
        print("   This is a universal property of continued fractions,")
        print("   independent of human notation choice.")
    else:
        print("\n⚠️  RESULT: Base-dependent variations detected.")
        print("   Further investigation needed.")
    
    return base_results

def deep_analysis_specific_ratio():
    """
    Deep dive: same NUMBER, different base representations.
    
    Key insight: The RATIO d_p/d_N changes with base, but does
    the CF structure maintain some invariant?
    """
    print("\n" + "=" * 80)
    print("DEEP ANALYSIS: Same Number Across Bases")
    print("=" * 80)
    
    # A specific semiprime
    N = 2**127 - 1  # Mersenne prime (for illustration)
    p = 2**50       # A factor-sized number
    
    bases = [2, 8, 10, 16]
    
    print(f"\nN ≈ 2^127")
    print(f"p ≈ 2^50")
    print("-" * 60)
    
    for base in bases:
        d_N = digit_count(N, base)
        d_p = digit_count(p, base)
        ratio = d_p / d_N
        cf = continued_fraction(ratio, depth=8)
        kappa = max(cf[1:]) if len(cf) > 1 else 0
        
        base_name = {2: "bin", 8: "oct", 10: "dec", 16: "hex"}[base]
        
        print(f"\nBase {base:>2} ({base_name}):")
        print(f"  d_N = {d_N}, d_p = {d_p}")
        print(f"  ratio = {ratio:.6f}")
        print(f"  CF = {cf}")
        print(f"  κ = {kappa}")
        print(f"  a₁ = {cf[1] if len(cf) > 1 else 'N/A'}, ⌊d_N/d_p⌋ = {d_N // d_p}")

def analyze_kappa_invariance():
    """
    The big question: Is κ (consonance degree) base-invariant?
    
    This would mean the "musical" quality of a ratio is 
    independent of how we write numbers!
    """
    print("\n" + "=" * 80)
    print("κ (CONSONANCE DEGREE) BASE INVARIANCE")
    print("=" * 80)
    print("\nQuestion: Does the 'musicality' of a number ratio")
    print("          depend on the base we use to represent it?")
    print("-" * 60)
    
    test_pairs = [
        (10**77, 10**30),   # "77-digit RSA"
        (10**77, 10**20),   # Different ratio
        (10**100, 10**50),  # Near 1/2
        (10**100, 10**33),  # ~1/3
    ]
    
    bases = [2, 10, 16]
    
    for N, p in test_pairs:
        print(f"\n{'='*50}")
        print(f"N = 10^{int(math.log10(N))}, p = 10^{int(math.log10(p))}")
        print(f"{'='*50}")
        
        kappas = {}
        for base in bases:
            d_N = digit_count(N, base)
            d_p = digit_count(p, base)
            ratio = d_p / d_N
            cf = continued_fraction(ratio, depth=10)
            kappa = max(cf[1:]) if len(cf) > 1 else 0
            kappas[base] = kappa
            
            base_name = {2: "Binary", 10: "Decimal", 16: "Hex"}[base]
            consonance = "Consonant" if kappa <= 4 else "Dissonant"
            
            print(f"  {base_name:>8}: ratio={ratio:.4f}, κ={kappa:>3} → {consonance}")
        
        # Check if κ classification is consistent
        classifications = ["C" if k <= 4 else "D" for k in kappas.values()]
        if len(set(classifications)) == 1:
            print(f"  → Classification CONSISTENT across bases")
        else:
            print(f"  → ⚠️  Classification VARIES by base!")

if __name__ == "__main__":
    # Run all analyses
    run_base_comparison()
    deep_analysis_specific_ratio()
    analyze_kappa_invariance()
