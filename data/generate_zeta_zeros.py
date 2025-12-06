#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Riemann ζ-zero Table Generator (Enhanced Version)
For Λ³ Hybrid Engine Research Paper

- Uses mpmath.zetazero to obtain ρ_n = 1/2 + i*γ_n
- Applies Gaussian window weight w_n = |1/ρ_n| * exp(-(γ/T)^2)
- Embeds metadata: RMS normalization, frequency indicators, etc.
- CLI configurable: K, T, output path, etc.

Copyright (c) 2025 Masamichi Iizumi (Miosync, inc.)
License: Apache 2.0 (see LICENSE file in repository root)
"""

import argparse
import json
import math
import sys
from pathlib import Path

from mpmath import mp, zetazero


def build_zeta_zero_table(K: int, T: float, dps: int = 80, progress_every: int = 50):
    """
    Generate weighted table of first K non-trivial zeros of Riemann ζ-function.

    Parameters
    ----------
    K : int
        Number of zeros to compute
    T : float
        Gaussian bandwidth for weighting
    dps : int
        Decimal precision for mpmath (default: 80)
    progress_every : int
        Progress display interval (0 to disable)

    Returns
    -------
    zeros : list[dict]
        List of zeros with structure: {n, gamma, w}
    meta : dict
        Metadata including RMS, weight range, etc.
    """
    print(f"🔍 Computing ζ-zeros... (K={K}, T={T}, dps={dps})")
    mp.dps = dps

    zeros = []
    w_sq_sum = 0.0

    for n in range(1, K + 1):
        if progress_every and n % progress_every == 0:
            print(f"  Progress: {n}/{K}", file=sys.stderr)

        rho = zetazero(n)                # ρ_n = 1/2 + i*γ_n
        gamma = float(rho.imag)

        # Weight: |1/ρ| * exp(-(γ/T)^2)
        # |1/ρ| provides natural high-frequency damping
        # Gaussian controls bandwidth
        w = (1.0 / math.hypot(0.5, gamma)) * math.exp(- (gamma / T) ** 2)

        w_sq_sum += w * w
        zeros.append({"n": n, "gamma": gamma, "w": w})

    # RMS normalization coefficients
    # rms_raw: simple root-mean-square of weights
    # rms_cos: RMS assuming Σ w_j cos(γu) usage (factor of 0.5)
    rms_raw = math.sqrt(max(1e-300, w_sq_sum) / max(1, K))
    rms_cos = math.sqrt(0.5 * max(1e-300, w_sq_sum))

    gammas = [z["gamma"] for z in zeros]
    ws = [z["w"] for z in zeros]

    # Weighted median of γ (useful for automatic σ_u determination)
    pairs = sorted(zip(gammas, ws), key=lambda t: t[0])
    total_w = sum(ws) or 1.0
    acc = 0.0
    gamma_med = pairs[-1][0]
    for g, w in pairs:
        acc += w
        if acc >= 0.5 * total_w:
            gamma_med = g
            break

    # Metadata
    meta = {
        "gamma_min": gammas[0] if gammas else None,
        "gamma_max": gammas[-1] if gammas else None,
        "w_min": min(ws) if ws else None,
        "w_max": max(ws) if ws else None,
        "w_rms_raw": rms_raw,
        "w_rms_cos": rms_cos,
        "gamma_weighted_median": gamma_med,
        "effective_K_guess": sum(1 for w in ws if w >= max(ws) * math.exp(-9.0)),  # ~3σ estimate
    }

    print(f"✅ Computed {K} zeros successfully!", file=sys.stderr)
    return zeros, meta


def main():
    ap = argparse.ArgumentParser(
        description="Riemann ζ-zero Table Generator for Λ³ Framework"
    )
    ap.add_argument("-K", type=int, default=500, 
                    help="Number of zeros to compute (e.g., 500, 1000, 2000)")
    ap.add_argument("-T", type=float, default=40.0, 
                    help="Gaussian bandwidth (e.g., 35-50)")
    ap.add_argument("--dps", type=int, default=80, 
                    help="mpmath decimal precision")
    ap.add_argument("--out", type=str, default="zeta_zeros.json", 
                    help="Output JSON file path")
    ap.add_argument("--indent", type=int, default=2, 
                    help="JSON indent width (-1 for compact)")
    ap.add_argument("--no-meta", action="store_true", 
                    help="Exclude metadata from output")
    ap.add_argument("--progress-every", type=int, default=50, 
                    help="Progress display interval (0 to disable)")
    args = ap.parse_args()

    K = args.K
    T = args.T

    print("=" * 70)
    print("🌟 Λ³ Riemann ζ-zero Table Generator (Enhanced)")
    print("=" * 70)
    print(f"K={K}, T={T}, dps={args.dps}")
    
    zeros, meta = build_zeta_zero_table(
        K=K, T=T, dps=args.dps, progress_every=args.progress_every
    )

    # Prepare output structure
    table = {
        "source": "mpmath_zetazero",
        "version": "2.0",
        "K": K,
        "T": T,
        "accuracy": f"mpmath dps={args.dps}",
        "zeros": zeros,
    }
    if not args.no_meta:
        table["meta"] = meta

    # Write to file
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    indent = None if args.indent < 0 else args.indent
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(table, f, ensure_ascii=False, indent=indent)

    # Display statistics
    print("\n📊 Statistics:")
    print(f"  Number of zeros: {len(zeros)}")
    print(f"  γ range: [{meta['gamma_min']:.6f}, {meta['gamma_max']:.6f}]")
    print(f"  Weight range: [{meta['w_min']:.6e}, {meta['w_max']:.6e}]")
    print(f"  w_rms_cos: {meta['w_rms_cos']:.6e}")
    print(f"  γ_weighted_median: {meta['gamma_weighted_median']:.6f}")
    print(f"  Effective K (≈3σ): {meta['effective_K_guess']}")

    print("\n" + "=" * 70)
    print(f"💾 Saved to: {out_path.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
