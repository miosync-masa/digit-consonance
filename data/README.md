# Riemann Zeta Zeros Database

This directory contains the first 10,000 non-trivial zeros of the Riemann zeta function.

## Files

- **zeta_zeros_10000.json** - Pre-computed database (ready to use)
- **generate_zeta_zeros.py** - Generator script (for reproduction/customization)

## Quick Start

### Using Pre-computed Data
```python
from zeta_resonance import load_zeta_zeros

gammas, weights, metadata = load_zeta_zeros('data/zeta_zeros_10000.json')
```

### Regenerating the Database
```bash
cd data
python generate_zeta_zeros.py -K 10000 -T 10000 --dps 80 --out zeta_zeros_10000.json
```

**Requirements:**
- Python 3.7+
- mpmath library: `pip install mpmath`

**Computation time:** ~4 hours on Google Colab A100 GPU

### Custom Parameters

Generate with different settings:
```bash
# Smaller database (faster)
python generate_zeta_zeros.py -K 1000 -T 1000 --out zeta_zeros_1000.json

# Higher precision
python generate_zeta_zeros.py -K 10000 -T 10000 --dps 100

# Different bandwidth
python generate_zeta_zeros.py -K 10000 -T 5000
```

## File Format

**zeta_zeros_10000.json**

JSON structure:
```json
{
    "source": "mpmath_zetazero",
    "version": "2.0",
    "K": 10000,
    "T": 5000.0,
    "accuracy": "mpmath dps=80",
    "zeros": [
        {"n": 1, "gamma": 14.134725141734693790..., "w": 0.061578...},
        {"n": 2, "gamma": 21.022039638771554993..., "w": 0.035078...},
        ...
    ],
    "meta": {
        "computed": "2024-12-06",
        "precision": "80 decimal digits"
    }
}
```

## Fields

- **n**: Index of the zero (1, 2, 3, ...)
- **gamma**: Imaginary part of the zero (ρ = 1/2 + i·γ)
- **w**: Weight factor (used in numerical integration)

## Mathematical Background

The Riemann zeta function ζ(s) has non-trivial zeros at:

ρₙ = 1/2 + i·γₙ

(assuming the Riemann Hypothesis)

The first few values:
- γ₁ = 14.134725...
- γ₂ = 21.022040...
- γ₃ = 25.010858...

## Computation

These zeros were computed using the `mpmath` library with 80-digit precision:
```python
import mpmath
mpmath.mp.dps = 80

# Compute n-th zero
gamma_n = mpmath.zetazero(n).imag
```

Computing all 10,000 zeros takes approximately 1-2 hours on a modern CPU.

## Usage
```python
from zeta_resonance import load_zeta_zeros

# Load zeros
gammas, weights, metadata = load_zeta_zeros('zeta_zeros_10000.json')

print(f"First zero: γ₁ = {gammas[0]}")
# Output: First zero: γ₁ = 14.134725141734693790457251983562470270784257115699243175685567460149963429809...
```

## Verification

You can verify these values against public databases:
- [LMFDB (L-functions and Modular Forms Database)](https://www.lmfdb.org/zeros/zeta/)
- [Odlyzko's tables](http://www.dtc.umn.edu/~odlyzko/zeta_tables/)

## Why Public?

These values are:
1. **Mathematically deterministic** - Anyone can compute them
2. **Publicly available** - Listed in academic databases
3. **Non-secret** - Required for scientific reproducibility
4. **Necessary for research** - Needed to verify paper results

Having the data ≠ Being able to use it effectively for any particular application.

## License

This data is in the public domain. Zeta zeros are mathematical constants, not copyrightable content.

## References

1. Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen Grösse"
2. Edwards, H.M. (1974). "Riemann's Zeta Function"
3. Titchmarsh, E.C. (1986). "The Theory of the Riemann Zeta Function"
4. LMFDB Collaboration. "The L-functions and Modular Forms Database" https://www.lmfdb.org
