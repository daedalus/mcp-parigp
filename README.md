# mcp-parigp

> MCP server exposing cypari2 (PARI/GP) number theory library

[![PyPI](https://img.shields.io/pypi/v/mcp-parigp.svg)](https://pypi.org/project/mcp-parigp/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-parigp.svg)](https://pypi.org/project/mcp-parigp/)
[![Coverage](https://codecov.io/gh/daedalus/mcp-parigp/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/mcp-parigp)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

mcp-name: io.github.daedalus/mcp-parigp

## Install

```bash
pip install mcp-parigp
```

## Usage

### As MCP Server

Run directly:
```bash
mcp-parigp
```

Or use with an MCP client by configuring in your settings:

```json
{
  "mcpServers": {
    "mcp-parigp": {
      "command": "mcp-parigp"
    }
  }
}
```

### In Python

```python
from mcp_parigp import eval_expression, factor, isprime

# Evaluate PARI/GP expressions
result = eval_expression("factor(100)")
print(result)  # [[2, 2], [5, 2]]

# Factor integers
print(factor(100))  # [[2, 2], [5, 2]]

# Test primality
print(isprime(29))  # True
```

## API

### Number Theory
- `factor(n)` - Factor an integer
- `isprime(n)` - Test if n is prime
- `gcd(a, b)` - Greatest common divisor
- `phi(n)` - Euler's totient function
- `sigma(n, k)` - Sum of k-th power of divisors
- `jacobi(a, n)` - Jacobi symbol
- `znorder(x, n)` - Multiplicative order modulo n
- `primes(n)` - First n primes
- `nextprime(n)` - Next prime after n

### Polynomials
- `polroots(pol)` - Find roots of polynomial
- `polcyclo(n)` - n-th cyclotomic polynomial
- `deriv(pol)` - Derivative of polynomial
- `subst(pol, v, expr)` - Substitute in polynomial

### Number Fields
- `nfinit(pol)` - Initialize number field
- `bnfinit(pol)` - Initialize with Buchmann's algorithm
- `idealadd(nf, a, b)` - Add ideals
- `idealmul(nf, a, b)` - Multiply ideals

### Elliptic Curves
- `ellinit(eq)` - Initialize elliptic curve
- `ellap(E, p)` - Trace of Frobenius at p
- `elltors(E)` - Torsion subgroup
- `ellheight(E, P)` - Canonical height

### Matrices
- `matid(n)` - n×n identity matrix
- `matdet(m)` - Matrix determinant
- `matinv(m)` - Matrix inverse
- `matrank(m)` - Matrix rank

### Elementary Functions
- `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`
- `exp`, `log`, `sqrt`, `abs`
- `pi()`, `euler()`, `I()`

## Development

```bash
git clone https://github.com/daedalus/mcp-parigp.git
cd mcp-parigp
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypysrc/
```
