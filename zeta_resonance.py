"""
Zeta Zero Resonance Detection
==============================

Detection of digit patterns using Riemann zeta zero resonance.

This module implements the resonance detection framework from:
"On the Consonance of Prime Factorization: A Continued Fraction Analysis 
of Digit Ratio Resonance with Riemann Zeta Zeros"
by Masamichi Iizumi (2025)

Theory
------
For a semiprime N = p × q, certain Riemann zeta zeros γ "resonate" with N
when cos(γ log N) ≈ 1. This resonance can reveal digit patterns of the factors.

Dependencies
------------
Standard library only for core functionality.
Optional: numpy for faster computation (not required)

License
-------
MIT License

Authors
-------
Masamichi Iizumi

__version__ = "1.0.0"
__author__ = "Masamichi Iizumi
"""

import math
import json
from typing import List, Dict, Tuple, Optional


def load_zeta_zeros(filepath: str, max_zeros: Optional[int] = None,
                   verbose: bool = False) -> Tuple[List[float], List[float], Dict]:
    """
    Load Riemann zeta zeros from JSON file.
    
    Expected JSON format:
    {
        "source": "mpmath_zetazero",
        "version": "2.0",
        "K": 10000,
        "T": 10000.0,
        "zeros": [
            {"n": 1, "gamma": 14.134725..., "w": 0.0615...},
            {"n": 2, "gamma": 21.022039..., "w": 0.0350...},
            ...
        ],
        "meta": {...}
    }
    
    Parameters
    ----------
    filepath : str
        Path to JSON file containing zeta zeros
    max_zeros : int, optional
        Maximum number of zeros to load (default: load all)
    verbose : bool, optional
        Print loading information (default: False)
    
    Returns
    -------
    gammas : list of float
        List of zeta zero imaginary parts (γ values)
    weights : list of float
        List of weights
    metadata : dict
        Metadata from the JSON file
    
    Examples
    --------
    >>> gammas, weights, meta = load_zeta_zeros('data/zeta_zeros_10000.json')
    >>> len(gammas)
    10000
    >>> gammas[0]
    14.134725...
    >>> meta['source']
    'mpmath_zetazero'
    
    Notes
    -----
    This is a standard-library-only version (no numpy required).
    Compatible with the JSON format from zeta zero databases.
    """
    import os
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Zeta zeros file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract zeros array
    zeros_list = data.get('zeros', [])
    if not zeros_list:
        raise ValueError("No zeros found in JSON file")
    
    # Sort by n to ensure order
    zeros_list = sorted(zeros_list, key=lambda x: x['n'])
    
    # Limit to max_zeros if specified
    if max_zeros is not None:
        zeros_list = zeros_list[:max_zeros]
    
    # Extract gamma and weights
    gammas = [z['gamma'] for z in zeros_list]
    weights = [z['w'] for z in zeros_list]
    
    # Build metadata
    metadata = {
        'source': data.get('source', 'unknown'),
        'version': data.get('version', 'unknown'),
        'file_K': data.get('K', len(zeros_list)),
        'loaded_K': len(gammas),
        'T': data.get('T', None),
        'accuracy': data.get('accuracy', 'unknown'),
        'gamma_range': (min(gammas), max(gammas)),
        'w_range': (min(weights), max(weights)),
    }
    
    # Add meta section if present
    if 'meta' in data:
        metadata['file_meta'] = data['meta']
    
    if verbose:
        print(f"📂 Loaded ζ-zeros from: {os.path.basename(filepath)}")
        print(f"   Source: {metadata['source']}")
        print(f"   Zeros: {metadata['loaded_K']} (file has {metadata['file_K']})")
        print(f"   γ range: [{metadata['gamma_range'][0]:.6f}, {metadata['gamma_range'][1]:.6f}]")
        if metadata['accuracy'] != 'unknown':
            print(f"   Accuracy: {metadata['accuracy']}")
    
    return gammas, weights, metadata


def find_resonant_gammas(N: int, gammas: List[float], 
                        threshold: float = 0.95) -> List[Dict]:
    """
    Find zeta zeros that resonate with integer N.
    
    A zeta zero γ is considered resonant with N if:
        cos(γ log N) > threshold
    
    This indicates that γ log N ≈ 2πn for some integer n.
    
    Parameters
    ----------
    N : int
        Integer to analyze
    gammas : list of float
        List of zeta zero imaginary parts
    threshold : float, optional
        Cosine threshold for resonance (default: 0.95)
        Higher values (closer to 1.0) = stricter resonance
    
    Returns
    -------
    list of dict
        Resonant zeros sorted by resonance strength.
        Each dict contains:
        - 'index': position in gamma list
        - 'gamma': zeta zero value
        - 'cos': cosine value (resonance strength)
        - 'n': integer component (γ log N / 2π)
    
    Examples
    --------
    >>> gammas = load_zeta_zeros('data/zeta_zeros_10000.json')
    >>> N = 12345678901234567890
    >>> resonant = find_resonant_gammas(N, gammas)
    >>> len(resonant)
    42
    >>> resonant[0]['cos']
    0.9987...
    
    Notes
    -----
    The number of resonant zeros depends on N and the threshold.
    Typical values: 10-100 resonant zeros per semiprime.
    """
    log_N = math.log(N)
    resonant = []
    
    for i, gamma in enumerate(gammas):
        cos_val = math.cos(gamma * log_N)
        if cos_val > threshold:
            n = gamma * log_N / (2 * math.pi)
            resonant.append({
                'index': i,
                'gamma': gamma,
                'cos': cos_val,
                'n': n
            })
    
    return sorted(resonant, key=lambda x: -x['cos'])


def is_true_resonance(gamma: float, N: int, p_digits: int, q_digits: int,
                     threshold: float = 0.01) -> Dict:
    """
    Distinguish true resonance from harmonic overtones.
    
    When a zeta zero resonates with N, it may be:
    - True resonance: reflects actual factor structure
    - Harmonic overtone: numerical coincidence
    
    This function performs a consistency check to filter overtones.
    
    Parameters
    ----------
    gamma : float
        Zeta zero imaginary part
    N : int
        Integer being analyzed
    p_digits : int
        Proposed number of digits in smaller factor
    q_digits : int
        Proposed number of digits in larger factor
    threshold : float, optional
        Consistency threshold (default: 0.01)
        Lower values = stricter filtering
    
    Returns
    -------
    dict
        Consistency metrics:
        - 'pattern_dist': digit pattern distance
        - 'n_q_dist': secondary factor distance
        - 'total_consistency': combined measure
        - 'is_true': True if passes consistency check
    
    Examples
    --------
    >>> check = is_true_resonance(14.134725, N, 38, 39)
    >>> check['is_true']
    True
    >>> check['total_consistency']
    0.0034...
    
    Notes
    -----
    This implements the "harmonic filter" described in Section 5
    of the paper. It reduces false positives from overtone resonances.
    """
    log_N = math.log(N)
    n = gamma * log_N / (2 * math.pi)
    digits_N = len(str(N))
    
    # Primary pattern check
    ratio_p = p_digits / digits_N
    exp_n_p = n * ratio_p
    exp_n_q = n * (1 - ratio_p)
    pattern_dist = abs(exp_n_p - round(exp_n_p)) + abs(exp_n_q - round(exp_n_q))
    
    # Secondary consistency check
    n_p_round = round(exp_n_p)
    log_p_est = n_p_round * 2 * math.pi / gamma
    
    log_q_est = log_N - log_p_est
    n_q_check = gamma * log_q_est / (2 * math.pi)
    n_q_dist = abs(n_q_check - round(exp_n_q))
    
    total_consistency = pattern_dist + n_q_dist
    
    return {
        'pattern_dist': pattern_dist,
        'n_q_dist': n_q_dist,
        'total_consistency': total_consistency,
        'is_true': total_consistency < threshold
    }


def find_factor_signatures(N: int, resonant_gammas: List[Dict],
                          dist_threshold: float = 0.01,
                          use_harmonic_filter: bool = True) -> List[Dict]:
    """
    Detect digit pattern signatures from resonant zeros.
    
    For each resonant zero, test all possible digit patterns to find
    those that match the resonance structure. Returns candidate
    digit patterns (NOT actual factor values).
    
    Parameters
    ----------
    N : int
        Integer to analyze
    resonant_gammas : list of dict
        Output from find_resonant_gammas()
    dist_threshold : float, optional
        Distance threshold for pattern detection (default: 0.01)
    use_harmonic_filter : bool, optional
        Whether to filter harmonic overtones (default: True)
    
    Returns
    -------
    list of dict
        Candidate digit patterns sorted by consistency.
        Each dict contains:
        - 'gamma': zeta zero that produced this signature
        - 'n': integer component
        - 'p_digits': proposed smaller factor digits
        - 'q_digits': proposed larger factor digits
        - 'total_digits': total digit count considered
        - 'n_p', 'n_q': integer components for each factor
        - 'dist': pattern distance
        - 'consistency': overall consistency measure
    
    Examples
    --------
    >>> resonant = find_resonant_gammas(N, gammas)
    >>> signatures = find_factor_signatures(N, resonant)
    >>> len(signatures)
    15
    >>> signatures[0]
    {'gamma': 14.134..., 'p_digits': 38, 'q_digits': 39, ...}
    
    Notes
    -----
    - This detects DIGIT PATTERNS only, not actual factor values
    - Multiple signatures may be detected; best ones ranked first
    - Harmonic filter significantly reduces false positives
    """
    digits_N = len(str(N))
    signatures = []
    
    for r in resonant_gammas:
        gamma = r['gamma']
        n = r['n']
        
        # Consider both digits_N and digits_N + 1
        # (accounting for leading digit uncertainty)
        for total_digits in [digits_N, digits_N + 1]:
            for p_digits in range(1, total_digits):
                q_digits = total_digits - p_digits
                if q_digits < 1:
                    continue
                
                ratio_p = p_digits / total_digits
                expected_n_p = n * ratio_p
                expected_n_q = n * (1 - ratio_p)
                
                dist_p = abs(expected_n_p - round(expected_n_p))
                dist_q = abs(expected_n_q - round(expected_n_q))
                pattern_dist = dist_p + dist_q
                
                if pattern_dist < dist_threshold:
                    # Apply harmonic filter if requested
                    if use_harmonic_filter:
                        check = is_true_resonance(gamma, N, p_digits, q_digits,
                                                 threshold=0.02)
                        if not check['is_true']:
                            continue
                        consistency = check['total_consistency']
                    else:
                        consistency = pattern_dist
                    
                    signatures.append({
                        'gamma': gamma,
                        'n': n,
                        'p_digits': p_digits,
                        'q_digits': q_digits,
                        'total_digits': total_digits,
                        'n_p': round(expected_n_p),
                        'n_q': round(expected_n_q),
                        'dist': pattern_dist,
                        'consistency': consistency
                    })
    
    return sorted(signatures, key=lambda x: x['consistency'])


def estimate_factor_magnitude(gamma: float, n_p: int) -> float:
    """
    Estimate factor magnitude from resonance parameters.
    
    Given a zeta zero γ and integer component n_p, estimates
    the order of magnitude of the corresponding factor.
    
    Parameters
    ----------
    gamma : float
        Zeta zero imaginary part
    n_p : int
        Integer component (from resonance)
    
    Returns
    -------
    float
        Estimated factor magnitude
    
    Examples
    --------
    >>> magnitude = estimate_factor_magnitude(14.134725, 42)
    >>> int(math.log10(magnitude))
    38
    
    Notes
    -----
    This provides an ORDER OF MAGNITUDE estimate only.
    Converting this to an actual prime factor requires
    additional search procedures.
    
    The relationship is: log p ≈ n_p × 2π / γ
    """
    log_p = n_p * 2 * math.pi / gamma
    return math.exp(log_p)


def print_signature_summary(signatures: List[Dict], max_display: int = 10):
    """
    Print formatted summary of detected signatures.
    
    Parameters
    ----------
    signatures : list of dict
        Output from find_factor_signatures()
    max_display : int, optional
        Maximum number to display (default: 10)
    """
    print(f"\n{'='*70}")
    print(f"Detected Factor Signatures: {len(signatures)} total")
    print(f"{'='*70}")
    print(f"{'γ index':<10} {'p_digits':<10} {'q_digits':<10} {'Consistency':<12}")
    print("-" * 70)
    
    for sig in signatures[:max_display]:
        print(f"{sig['gamma']:<10.3f} {sig['p_digits']:<10} "
              f"{sig['q_digits']:<10} {sig['consistency']:<12.6f}")
    
    if len(signatures) > max_display:
        print(f"... and {len(signatures) - max_display} more")
    
    print(f"{'='*70}\n")


# ===============================================
# Example Usage
# ===============================================

if __name__ == "__main__":
    print("=" * 70)
    print("Zeta Zero Resonance Detection - Demo")
    print("=" * 70)
    
    # Load zeta zeros
    print("\nLoading zeta zeros...")
    try:
        gammas, weights, metadata = load_zeta_zeros(
            'zeta_zeros_10000.json',
            verbose=True
        )
        print(f"\n  First zero: γ₁ = {gammas[0]:.6f}")
        print(f"  Last zero:  γ_{len(gammas)} = {gammas[-1]:.6f}")
    except FileNotFoundError:
        print("✗ Data file not found!")
        print("  Please ensure data/zeta_zeros_10000.json exists")
        exit(1)
    
    # Example integer (77-digit semiprime)
    print("\nExample: Analyzing a 77-digit number")
    N = 999999999999999999999999999999999999945999999999999999999999999999999999999829
    print(f"N = {N}")
    print(f"Digits: {len(str(N))}")
    
    # Find resonant zeros
    print("\nStep 1: Finding resonant zeros...")
    resonant = find_resonant_gammas(N, gammas, threshold=0.95)
    print(f"✓ Found {len(resonant)} resonant zeros")
    if resonant:
        print(f"  Strongest resonance: γ = {resonant[0]['gamma']:.6f}, "
              f"cos = {resonant[0]['cos']:.6f}")
    
    # Detect signatures
    print("\nStep 2: Detecting digit patterns...")
    signatures = find_factor_signatures(N, resonant)
    print_signature_summary(signatures)
    
    # Example: estimate magnitude
    if signatures:
        sig = signatures[0]
        mag = estimate_factor_magnitude(sig['gamma'], sig['n_p'])
        print(f"\nExample magnitude estimate:")
        print(f"  Estimated p ≈ 10^{math.log10(mag):.1f}")
        print(f"  Expected digits: {sig['p_digits']}")
    
    # Note
    print("\n" + "=" * 70)
    print("NOTE: These are digit pattern signatures, NOT actual factors.")
    print("Converting patterns to factors requires additional procedures.")
    print("=" * 70)
