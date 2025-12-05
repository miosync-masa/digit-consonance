"""
Digit Consonance Analysis
=========================

Mathematical tool for analyzing consonance patterns in digit ratios
based on continued fraction expansions.

Based on: "On the Consonance of Prime Factorization: A Continued 
Fraction Analysis of Digit Ratio Resonance with Riemann Zeta Zeros"
by Masamichi Iizumi and Tamaki Iizumi (2025)

No external dependencies required - uses only Python standard library.
"""

def continued_fraction(x, depth=10):
    """
    Compute continued fraction expansion of a real number.
    
    Parameters
    ----------
    x : float
        Real number to expand
    depth : int, optional
        Maximum depth of expansion (default: 10)
    
    Returns
    -------
    list of int
        Continued fraction coefficients [a₀, a₁, a₂, ...]
    
    Examples
    --------
    >>> continued_fraction(0.3896, depth=8)
    [0, 2, 1, 1, 3, 3, 1]
    
    Notes
    -----
    For a real number x, the continued fraction is:
        x = a₀ + 1/(a₁ + 1/(a₂ + 1/(a₃ + ...)))
    """
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


def analyze_digit_consonance(N_digits, kappa_threshold=4):
    """
    Analyze consonance patterns for all possible digit ratios.
    
    For an N-digit number, analyzes the consonance degree of all
    possible factor digit counts using continued fraction theory.
    
    Parameters
    ----------
    N_digits : int
        Total number of digits
    kappa_threshold : int, optional
        Consonance threshold (default: 4)
        - κ ≤ threshold → consonant
        - κ > threshold → dissonant
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'consonant': list of consonant patterns
        - 'dissonant': list of dissonant patterns
        - 'N_digits': input digit count
        - 'threshold': threshold used
        
        Each pattern is a dict with:
        - 'p_digits': factor digit count
        - 'ratio': digit ratio (p_digits / N_digits)
        - 'cf': continued fraction coefficients
        - 'kappa': consonance degree (max CF coefficient)
    
    Examples
    --------
    >>> result = analyze_digit_consonance(77)
    >>> len(result['consonant'])
    15
    >>> len(result['dissonant'])
    23
    
    Notes
    -----
    The consonance degree κ is defined as:
        κ(r) := max{a₁, a₂, a₃, ...}
    
    where [0; a₁, a₂, ...] is the continued fraction of ratio r.
    
    The threshold κ = 4 corresponds to the classical boundary
    between consonant and dissonant intervals in music theory.
    """
    consonant = []
    dissonant = []
    
    # Iterate through all possible factor digit counts
    for p_digits in range(1, N_digits // 2 + 1):
        ratio = p_digits / N_digits
        
        # Compute continued fraction expansion
        cf = continued_fraction(ratio, depth=10)
        
        # Consonance degree: maximum coefficient (excluding a₀)
        kappa = max(cf[1:]) if len(cf) > 1 else 0
        
        # Create pattern dictionary
        pattern = {
            'p_digits': p_digits,
            'ratio': ratio,
            'cf': cf,
            'kappa': kappa
        }
        
        # Classify as consonant or dissonant
        if kappa <= kappa_threshold:
            consonant.append(pattern)
        else:
            dissonant.append(pattern)
    
    return {
        'consonant': consonant,
        'dissonant': dissonant,
        'N_digits': N_digits,
        'threshold': kappa_threshold
    }


def print_analysis(result, max_display=None):
    """
    Print formatted analysis results.
    
    Parameters
    ----------
    result : dict
        Output from analyze_digit_consonance()
    max_display : int, optional
        Maximum number of patterns to display per category
        If None, displays all patterns
    
    Examples
    --------
    >>> result = analyze_digit_consonance(77)
    >>> print_analysis(result)
    >>> print_analysis(result, max_display=5)  # Show only first 5
    """
    N = result['N_digits']
    threshold = result['threshold']
    
    print(f"\n{'='*70}")
    print(f"Digit Consonance Analysis: N = {N} digits")
    print(f"Consonance threshold: κ ≤ {threshold}")
    print(f"{'='*70}\n")
    
    # Consonant patterns
    consonant = result['consonant']
    display_cons = consonant[:max_display] if max_display else consonant
    
    print(f"♪ Consonant patterns (κ ≤ {threshold}): {len(consonant)} total")
    print("-" * 70)
    for p in display_cons:
        cf_str = str(p['cf'][:6]) if len(p['cf']) > 6 else str(p['cf'])
        print(f"  {p['p_digits']:3d} / {N:3d} digits = {p['ratio']:6.4f}  "
              f"CF: {cf_str:30s}  κ = {p['kappa']}")
    
    if max_display and len(consonant) > max_display:
        print(f"  ... and {len(consonant) - max_display} more")
    
    # Dissonant patterns
    dissonant = result['dissonant']
    display_dis = dissonant[:max_display] if max_display else dissonant
    
    print(f"\n♫ Dissonant patterns (κ > {threshold}): {len(dissonant)} total")
    print("-" * 70)
    for p in display_dis:
        cf_str = str(p['cf'][:6]) if len(p['cf']) > 6 else str(p['cf'])
        print(f"  {p['p_digits']:3d} / {N:3d} digits = {p['ratio']:6.4f}  "
              f"CF: {cf_str:30s}  κ = {p['kappa']}")
    
    if max_display and len(dissonant) > max_display:
        print(f"  ... and {len(dissonant) - max_display} more")
    
    print(f"\n{'='*70}\n")


def summary_table(digit_ranges):
    """
    Generate summary table for multiple digit ranges.
    
    Parameters
    ----------
    digit_ranges : list of int
        List of N values to analyze
    
    Examples
    --------
    >>> summary_table([50, 77, 100, 154, 256])
    """
    print(f"\n{'='*60}")
    print(f"Summary: Consonance Distribution Across Digit Ranges")
    print(f"{'='*60}")
    print(f"{'N (digits)':>12} | {'Consonant':>12} | {'Dissonant':>12} | {'Ratio':>8}")
    print(f"{'-'*12}-+-{'-'*12}-+-{'-'*12}-+-{'-'*8}")
    
    for N in digit_ranges:
        result = analyze_digit_consonance(N)
        n_cons = len(result['consonant'])
        n_dis = len(result['dissonant'])
        ratio = n_cons / (n_cons + n_dis) if (n_cons + n_dis) > 0 else 0
        
        print(f"{N:12d} | {n_cons:12d} | {n_dis:12d} | {ratio:7.2%}")
    
    print(f"{'='*60}\n")


# ===============================================
# Example Usage
# ===============================================

if __name__ == "__main__":
    # Basic analysis for 77 digits
    print("Example 1: Analyzing 77-digit patterns")
    result = analyze_digit_consonance(77)
    print_analysis(result, max_display=10)
    
    # Detailed look at a specific ratio
    print("\nExample 2: Detailed analysis of 20/77 ratio")
    ratio_20_77 = 20 / 77
    cf_20_77 = continued_fraction(ratio_20_77)
    kappa_20_77 = max(cf_20_77[1:]) if len(cf_20_77) > 1 else 0
    
    print(f"Ratio: 20/77 = {ratio_20_77:.6f}")
    print(f"Continued fraction: {cf_20_77}")
    print(f"Consonance degree: κ = {kappa_20_77}")
    print(f"Classification: {'Consonant' if kappa_20_77 <= 4 else 'Dissonant'}")
    
    # Summary across multiple digit ranges
    print("\nExample 3: Summary across common digit ranges")
    summary_table([30, 50, 77, 100, 154, 256, 617])
    
    # Custom threshold analysis
    print("\nExample 4: Effect of changing threshold")
    for threshold in [3, 4, 5]:
        result = analyze_digit_consonance(77, kappa_threshold=threshold)
        n_cons = len(result['consonant'])
        n_dis = len(result['dissonant'])
        print(f"κ ≤ {threshold}: {n_cons} consonant, {n_dis} dissonant")
