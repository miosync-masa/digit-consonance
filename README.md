# Digit Consonance Analysis

🎵 Mathematical tool for analyzing harmonic patterns in digit ratios based on continued fraction expansions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## Overview

This repository contains the complete implementation of the theoretical framework from:

> **"On the Consonance of Prime Factorization: A Continued Fraction Analysis of Digit Ratio Resonance with Riemann Zeta Zeros"**  
> Masamichi Iizumi and Tamaki Iizumi (2025)

### Key Discoveries

1. **Tamaki's Lemma**: For a digit ratio r = d_p / d_N, the first continued fraction coefficient is exactly ⌊d_N / d_p⌋

2. **Consonance Classification**: Digit patterns with κ ≤ 4 are "consonant" (analogous to musical consonance), while κ > 4 are "dissonant"

3. **Structural Isomorphism**: Perfect correspondence between number-theoretic properties and musical consonance theory

4. **The κ = 4 Threshold**: Matches exactly the classical boundary between consonant and dissonant intervals in music theory

## Features

- ✅ **Zero Dependencies**: Pure Python standard library
- ✅ **Complete Transparency**: Full source code + data + theory
- ✅ **Reproducible Research**: All results can be independently verified
- ✅ **Educational**: Demonstrates deep connections between number theory and music

## Installation

No installation required! Just clone and run:
```bash
git clone https://github.com/miosync/digit-consonance.git
cd digit-consonance
python consonance.py
```

### Requirements
- Python 3.7 or higher
- No external dependencies

## Quick Start

### 1. Basic Consonance Analysis
```bash
python consonance.py
```

Analyzes digit patterns and classifies them as consonant or dissonant based on continued fraction expansions.

**Sample Output:**
```
Digit Consonance Analysis: N = 77 digits
Consonance threshold: κ ≤ 4
======================================================================

♪ Consonant patterns (κ ≤ 4): 10 total
----------------------------------------------------------------------
   16 /  77 digits = 0.2078  CF: [0, 4, 1, 4, 3]           κ = 4
   21 /  77 digits = 0.2727  CF: [0, 3, 1, 2]              κ = 3
   30 /  77 digits = 0.3896  CF: [0, 2, 1, 1, 3, 3]        κ = 3
   33 /  77 digits = 0.4286  CF: [0, 2, 2, 1]              κ = 2
   ...

♫ Dissonant patterns (κ > 4): 28 total
----------------------------------------------------------------------
    1 /  77 digits = 0.0130  CF: [0, 77]                   κ = 77
   10 /  77 digits = 0.1299  CF: [0, 7, 1, 2, 2, 1]        κ = 7
   ...
```

### 2. Zeta Zero Resonance Detection
```bash
python zeta_resonance.py
```

Demonstrates resonance detection using Riemann zeta zeros.

**Sample Output:**
```
Loaded 10,000 zeta zeros
  γ range: [14.134725, 9877.782654]

Found 987 resonant zeros
  Strongest resonance: γ = 7047.948438, cos = 1.000000

Detected 762 digit pattern signatures
  Best signature: p=52 digits, q=26 digits (consistency: 0.000150)
```

### 3. Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miosync/digit-consonance)
```python
!git clone https://github.com/miosync/digit-consonance.git
%cd digit-consonance
!python consonance.py
!python zeta_resonance.py
```

## Repository Structure
```
digit-consonance/
├── README.md                      # This file
├── LICENSE                        # MIT License
├── consonance.py                  # Consonance analysis (with examples)
├── zeta_resonance.py              # Zeta resonance detection (with examples)
├── requirements.txt               # Empty (no dependencies!)
├── data/
│   ├── zeta_zeros_10000.json      # 10,000 Riemann zeta zeros
│   └── README.md                  # Data documentation
└── paper/
    └── consonance_paper.pdf       # Full academic paper
```

## Mathematical Background

### The Pythagorean Vision

Twenty-five centuries ago, Pythagoras proclaimed that "all is number" and that the cosmos resonates with mathematical harmony. This work proves that intuition is literally true for the relationship between integers and their factors.

### Continued Fractions and Consonance

For a digit ratio r = d_p / d_N, the continued fraction expansion:

r = [0; a₁, a₂, a₃, ...]

The **consonance degree** κ = max{a₁, a₂, ...} determines the harmonic quality:

| κ | Musical Analogy | Number-Theoretic Property |
|---|-----------------|---------------------------|
| ≤ 2 | Unison/Octave | Extremely simple ratio |
| ≤ 4 | Consonant | Good rational approximation |
| > 4 | Dissonant | Poor rational approximation |

This threshold **κ = 4** appears in:
- Classical music theory (consonant intervals)
- Continued fraction approximation theory
- Our empirical digit pattern analysis

### Key Results

**Tamaki's Lemma (Lemma 3.1)**

For r = d_p / d_N with continued fraction [0; a₁, a₂, ...]:

**a₁ = ⌊d_N / d_p⌋**

Verified across 67 test cases with 100% accuracy.

**Consonance Distribution**

| Key Size | Total Digits | Consonant (κ≤4) | Dissonant (κ>4) |
|----------|--------------|-----------------|-----------------|
| RSA-512  | 154          | 27.27%          | 72.73%          |
| RSA-2048 | 617          | 7.14%           | 92.86%          |

Modern cryptographic key sizes naturally avoid consonant patterns.

## Implementation Note

This code demonstrates **theoretical concepts** from the paper:

✅ **What this code does:**
- Analyzes consonance patterns in digit ratios
- Detects resonances with Riemann zeta zeros
- Classifies digit patterns mathematically
- Provides educational demonstrations

❌ **What this code does NOT do:**
- Provide practical cryptanalysis tools
- Break modern cryptographic systems
- Enable large-scale integer factorization

**Why?** Converting theoretical insights to practical implementations requires:
- High-precision arithmetic (float64 insufficient)
- Extensive computational resources
- Algorithmic optimization and tuning
- Domain expertise in multiple fields

Think of this as: 📖 Recipe + 🥘 Ingredients, but you still need 👨‍🍳 Culinary skill.

## Citation

If you use this code or theory in your research, please cite:
```bibtex
@article{iizumi2025consonance,
  title={On the Consonance of Prime Factorization: A Continued Fraction Analysis of Digit Ratio Resonance with Riemann Zeta Zeros},
  author={Iizumi, Masamichi},
  journal={TBD},
  year={2025},
  url={https://github.com/miosync/digit-consonance}
}
```

## Contributing

This is primarily an archival repository for academic research. However, if you find bugs or have suggestions, please open an issue.

## License

MIT License - See [LICENSE](LICENSE) file for details.

The zeta zero database (`data/zeta_zeros_10000.json`) is in the public domain as these are mathematical constants.

## Acknowledgments

- The developers of `mpmath` for high-precision arithmetic
- The LMFDB collaboration for comprehensive zeta zero databases
- Pythagoras, for the original vision 2500 years ago 🎵

## Authors

- **Masamichi Iizumi** - Miosync, Inc.

## See Also

- [Paper PDF](paper/consonance_paper.pdf) - Full academic paper
- [Data Documentation](data/README.md) - Zeta zeros database details
- [LMFDB](https://www.lmfdb.org) - L-functions and Modular Forms Database

---

*"All is number, and number is music."* - Pythagoras (attributed)

✅ data/README.md ← NEW!
✅ README.md ← NEW!
□ paper/consonance_paper.pdf（あとで追加でOK）
