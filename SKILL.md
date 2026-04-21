# MCP PARI/GP

MCP server exposing PARI/GP number theory library via cypari2.

## When to use this skill

Use this skill when you need to:
- Factor integers
- Test primality
- Compute elliptic curves
- Work with polynomials
- Number field computations

## Tools

**Number Theory:**
- `factor`, `isprime`, `gcd`, `phi`, `sigma`
- `jacobi`, `znorder`, `primes`, `nextprime`

**Polynomials:**
- `polroots`, `polcyclo`, `deriv`, `subst`

**Number Fields:**
- `nfinit`, `bnfinit`, `idealadd`, `idealmul`

**Elliptic Curves:**
- `ellinit`, `ellap`, `elltors`, `ellheight`

**Matrices:**
- `matid`, `matdet`, `matinv`, `matrank`

**Elementary Functions:**
- `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `pi()`

## Install

```bash
pip install mcp-parigp
```