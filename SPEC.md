# SPEC.md — mcp-parigp

## Purpose

An MCP (Model Context Protocol) server that exposes all functionality from the cypari2 library (Python interface to PARI/GP number theory library). This allows AI assistants to perform number theory computations including arithmetic, algebraic number theory, elliptic curves, modular forms, and more.

## Scope

- Expose PARI/GP number theory functions via MCP tools
- Support both exact (integer/rational) and floating-point computations
- Include algebraic number theory functions (nfinit, bnfinit, elliptic curves)
- Include polynomial operations and factorization
- Support modular arithmetic and elliptic curve computations
- Handle PARI objects conversion to/from Python types

NOT in scope:
- Interactive GP calculator mode
- Graphics/output plotting functions

## Public API / Interface

### MCP Server
- Server name: `mcp-parigp`
- Transport: stdio
- Single `pari` instance shared across all tools

### Core PARI Functions (auto-generated wrapper)

**Arithmetic & Basic Math:**
- `abs`, `cos`, `sin`, `tan`, `acos`, `asin`, `atan`, `cosh`, `sinh`, `tanh`, `acosh`, `asinh`, `atanh`
- `exp`, `log`, `sqrt`, `pow`, `mod`
- `factorial`, `binomial`, `fibonacci`, `lucas`

**Number Theory:**
- `factor`, `gcd`, `lcm`, `bezout`, `ispower`, `isprime`, `nextprime`, `prevprime`
- `phi` (Euler totient), `sigma` (divisor sum), `moebius`, `jacobi`
- `znorder`, `znstar`, `bnfinit`, `bnrinit`, `quadratic_forms`
- `ellinit`, `elladd`, `ellsub`, `ellmul`, `ellpow`, `ellorder`, `ellisor`, `elllog`
- `ellap`, `elltors`, `elllocalred`, `ellglobalred`, `ellinit`

**Polynomials:**
- `Pol`, `Polrev`, `Vec`, `Vecrev`, `Ser`
- `polroots`, `polrootspadic`, `factor`, `factorpadic`, `gcd`, `deriv`, `integ`
- `polcyclo`, `polchebyshev`, `polsubcyclo`, `polhermite`, `pollegendre`
- `subst`, `eval`, `resultant`, `disc`, `norm`, `trace`

**Algebraic Numbers:**
- `nfinit`, `bnfinit`, `bnrinit`, `idealadd`, `idealmul`, `idealpow`, `idealfactor`
- `mod`, `Mod`, `lift`, `centerlift`, `algdep`

**Matrix Operations:**
- `matid`, `matzero`, `matadd`, `matsub`, `matmul`, `matpow`, `mateigen`, `matcharpoly`
- `matdet`, `matinv`, `matrank`, `matker`, `matimage`, `hess`

**Conversions:**
- `List`, `Col`, `Colrev`, `Vec`, `Vecsmall`, `Mat`, `Set`, `Map`
- `gen_to_python` - Convert PARI object to Python native type
- `python_to_gen` - Convert Python object to PARI object

**Utility:**
- `pari_version` - Get PARI version
- `set_real_precision` / `get_real_precision` - Control floating-point precision
- `allocatemem` - Manage PARI stack size
- `setrand` / `getrand` - Random seed control
- `primes` - Generate prime numbers

### String Evaluation
- `eval` - Evaluate arbitrary PARI/GP expression string

## Data Formats

- Input: Python types (int, float, str, list) converted to PARI
- Output: PARI objects converted back to Python types
- Complex numbers: represented as tuples (real, imag) or PARI complex type

## Edge Cases

1. Very large integers - handled by PARI's arbitrary precision
2. Zero division - returns infinity or raises error appropriately
3. Non-invertible matrices - returns error
4. Invalid polynomial coefficients - raises TypeError
5. Prime beyond limit - raises ValueError
6. Stack overflow - user can increase with allocatemem

## Performance & Constraints

- Default PARI stack: 8MB
- Default real precision: 53 bits
- All computations are exact except when using floating-point
