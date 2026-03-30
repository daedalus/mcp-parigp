"""MCP server for cypari2 (PARI/GP number theory library)."""

from typing import Any

import cypari2
from fastmcp import FastMCP

__version__ = "0.1.0"

mcp = FastMCP("mcp-parigp")

__all__ = [
    "mcp",
    "get_pari_version",
    "eval_expression",
    "set_real_precision",
    "get_real_precision",
    "set_real_precision_bits",
    "get_real_precision_bits",
    "allocatemem",
    "stacksize",
    "stacksizemax",
    "setrand",
    "getrand",
    "primes",
    "prime",
    "factor",
    "isprime",
    "gcd",
    "lcm",
    "bezout",
    "phi",
    "sigma",
    "moebius",
    "jacobi",
    "legendre",
    "znorder",
    "znstar",
    "factorial",
    "binomial",
    "fibonacci",
    "lucas",
    "polcyclo",
    "polchebyshev",
    "pollegendre",
    "polhermite",
    "polroots",
    "polrootsmod",
    "polrootspadic",
    "factorpadic",
    "deriv",
    "integ",
    "resultant",
    "disc",
    "norm",
    "trace",
    "subst",
    "Mod",
    "lift",
    "centerlift",
    "nfinit",
    "bnfinit",
    "bnrinit",
    "idealadd",
    "idealmul",
    "idealpow",
    "idealfactor",
    "ellinit",
    "elladd",
    "ellmul",
    "ellorder",
    "elllog",
    "ellap",
    "elltors",
    "ellglobalred",
    "elllocalred",
    "ellheight",
    "ellj",
    "elleta",
    "ellwp",
    "ellzeta",
    "matid",
    "matzero",
    "matdet",
    "matinv",
    "matrank",
    "matker",
    "matimage",
    "mateigen",
    "matcharpoly",
    "hess",
    "List",
    "Vec",
    "Col",
    "Mat",
    "Set",
    "Pol",
    "Polrev",
    "Ser",
    "pi",
    "euler",
    "Catalan",
    "complex",
    "I",
    "one",
    "zero",
    "abs",
    "sqrt",
    "exp",
    "log",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sinh",
    "cosh",
    "tanh",
    "asinh",
    "acosh",
    "atanh",
    "agm",
    "airy",
    "genus2red",
    "algdep",
    "vector",
    "matrix",
    "polsubcyclo",
    "init_primes",
    "addprimes",
    "removeprimes",
    "ispower",
    "is_square",
    "nextprime",
    "prevprime",
    "Qfb",
    "qfbsolve",
    "qfbclassno",
    "quadregulator",
    "quadratic_forms",
    "hilbert",
    "bessel",
    "besselh",
    "theta",
    "weber",
    "eta",
    "modular_lambda",
    "modulr_sym",
    "cusp_form",
    "eisenstein",
    "bnrL1",
    "bnrrootnumber",
    "dirichlet",
    "lfun",
    "lfuntheta",
]

_pari = None


def _get_pari() -> cypari2.Pari:
    """Get or create the shared PARI instance."""
    global _pari
    if _pari is None:
        _pari = cypari2.Pari()
    return _pari


def _convert_to_python(obj: Any) -> Any:
    """Convert PARI object to Python native type."""
    if obj is None:
        return None
    # Handle PARI Gen objects - try .python() first, fall back to str()
    if hasattr(obj, "python"):
        try:
            return obj.python()
        except NotImplementedError:
            return str(obj)
    # Handle iterable objects (lists, vectors, etc.)
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        try:
            return [_convert_to_python(x) for x in obj]
        except TypeError:
            return str(obj)
    return obj


@mcp.tool()
def eval_expression(expr: str, timeout: int = 60) -> Any:
    """Evaluate a PARI/GP expression string.

    Args:
        expr: A PARI/GP expression as a string (e.g., "x^2 + 1", "factor(100)", "prime(10)").
            For multiple computations, ALWAYS use vector expressions like "vector(15, n, qfbclassno(-4*n))"
            instead of for-loops with print statements. For-loops may cause timeouts.
        timeout: Maximum execution time in seconds (default 60). Note: This is a best-effort timeout
            and may not work reliably for long-running PARI operations written in C.

    Returns:
        The result of the evaluation converted to Python types.

    Example:
        >>> eval_expression("factor(100)")
        [[2, 2], [5, 2]]
        >>> eval_expression("prime(10)")
        29
        >>> eval_expression("vector(15, n, qfbclassno(-4*n))")
        [1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 4, 1, 2]
    """
    import signal
    from typing import Any

    class TimeoutError(Exception):
        pass

    def timeout_handler(signum: int, frame: Any) -> Any:  # type: ignore[arg-type]
        raise TimeoutError(f"Expression evaluation timed out after {timeout} seconds")

    pari = _get_pari()
    result = None
    timeout_error: list[Exception | None] = [None]

    def evaluate() -> None:
        nonlocal result
        try:
            result = pari(expr)
        except Exception as e:
            timeout_error[0] = e

    import threading

    thread = threading.Thread(target=evaluate)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        raise TimeoutError(f"Expression evaluation timed out after {timeout} seconds")
    if timeout_error[0]:
        raise timeout_error[0]

    return _convert_to_python(result)


@mcp.tool()
def get_pari_version() -> str:
    """Get the PARI/GP version string.

    Returns:
        String describing the PARI version.

    Example:
        >>> get_pari_version()
        'GP/PARI CALCULATOR Version 2.15...'
    """
    return cypari2.Pari.pari_version()


@mcp.tool()
def set_real_precision(n: int) -> int:
    """Set the PARI default real precision in decimal digits.

    Args:
        n: Number of decimal digits for precision.

    Returns:
        The previous precision value.

    Example:
        >>> set_real_precision(50)
        15
    """
    pari = _get_pari()
    return pari.set_real_precision(n)


@mcp.tool()
def get_real_precision() -> int:
    """Get the current PARI default real precision in decimal digits.

    Returns:
        Current precision in decimal digits.

    Example:
        >>> get_real_precision()
        15
    """
    pari = _get_pari()
    return pari.get_real_precision()


@mcp.tool()
def set_real_precision_bits(n: int) -> int:
    """Set the PARI default real precision in bits.

    Args:
        n: Number of bits of precision.

    Returns:
        The previous precision in bits.

    Example:
        >>> set_real_precision_bits(200)
        53
    """
    pari = _get_pari()
    return pari.set_real_precision_bits(n)


@mcp.tool()
def get_real_precision_bits() -> int:
    """Get the current PARI default real precision in bits.

    Returns:
        Current precision in bits.

    Example:
        >>> get_real_precision_bits()
        53
    """
    pari = _get_pari()
    return pari.get_real_precision_bits()


@mcp.tool()
def allocatemem(size: int = 0, sizemax: int = 0) -> str:
    """Change the PARI stack size.

    Args:
        size: New stack size in bytes. If 0, doubles current size.
        sizemax: Maximum stack size in bytes. If 0, uses current maximum.

    Returns:
        Status message from PARI.

    Example:
        >>> allocatemem(10**7)
        'PARI stack size set to 10000000 bytes...'
    """
    pari = _get_pari()
    return pari.allocatemem(size, sizemax)


@mcp.tool()
def stacksize() -> int:
    """Get the current PARI stack size in bytes.

    Returns:
        Current stack size.

    Example:
        >>> stacksize()
        8000000
    """
    pari = _get_pari()
    return pari.stacksize()


@mcp.tool()
def stacksizemax() -> int:
    """Get the maximum PARI stack size in bytes.

    Returns:
        Maximum stack size.

    Example:
        >>> stacksizemax()
        536870912
    """
    pari = _get_pari()
    return pari.stacksizemax()


@mcp.tool()
def setrand(seed: int) -> None:
    """Set PARI's random number seed.

    Args:
        seed: A positive integer or a GEN of type t_VECSMALL.

    Example:
        >>> setrand(42)
    """
    pari = _get_pari()
    pari.setrand(seed)


@mcp.tool()
def getrand() -> Any:
    """Get PARI's current random number seed.

    Returns:
        The current random seed.

    Example:
        >>> getrand()
        [1, 2, 3, ...]
    """
    pari = _get_pari()
    return _convert_to_python(pari.getrand())


@mcp.tool()
def primes(n: int = 0, end: int = 0) -> list:
    """Return prime numbers.

    Args:
        n: Either an integer (first n primes), or a list [a,b] for range, or start of range.
        end: End of prime range if n is a start value.

    Returns:
        List of prime numbers.

    Example:
        >>> primes(10)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        >>> primes(100, 200)
        [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    """
    pari = _get_pari()
    if end != 0:
        result = pari.primes(n, end)
    else:
        result = pari.primes(n)
    return _convert_to_python(result)


@mcp.tool()
def prime(n: int) -> int:
    """Return the nth prime (1-indexed).

    Args:
        n: Which prime to return (1-indexed).

    Returns:
        The nth prime.

    Example:
        >>> prime(10)
        29
    """
    pari = _get_pari()
    return int(pari.prime(n))


@mcp.tool()
def factor(n: int) -> list:
    """Factor an integer.

    Args:
        n: Integer to factor.

    Returns:
        Factorization as list of [prime, exponent] pairs.

    Example:
        >>> factor(100)
        [[2, 2], [5, 2]]
    """
    pari = _get_pari()
    result = pari.factor(n)
    return _convert_to_python(result)


@mcp.tool()
def isprime(n: int) -> bool:
    """Test if an integer is prime.

    Args:
        n: Integer to test.

    Returns:
        True if n is prime, False otherwise.

    Example:
        >>> isprime(29)
        True
        >>> isprime(28)
        False
    """
    pari = _get_pari()
    return bool(pari.isprime(n))


@mcp.tool()
def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The gcd of a and b.

    Example:
        >>> gcd(48, 18)
        6
    """
    pari = _get_pari()
    return int(pari.gcd(a, b))


@mcp.tool()
def lcm(a: int, b: int) -> int:
    """Compute the least common multiple of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The lcm of a and b.

    Example:
        >>> lcm(4, 6)
        12
    """
    pari = _get_pari()
    return int(pari.lcm(a, b))


@mcp.tool()
def bezout(a: int, b: int) -> tuple:
    """Compute the Bezout identity: gcd(a,b) = a*u + b*v.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Tuple (g, u, v) where g = gcd(a,b) and a*u + b*v = g.

    Example:
        >>> bezout(48, 18)
        (6, -1, 3)
    """
    pari = _get_pari()
    result = pari.bezout(a, b)
    return tuple(int(x) for x in result)


@mcp.tool()
def phi(n: int) -> int:
    """Compute Euler's totient function phi(n).

    Args:
        n: Positive integer.

    Returns:
        phi(n) - count of integers <= n that are coprime to n.

    Example:
        >>> phi(10)
        4
    """
    pari = _get_pari()
    return int(pari.eulerphi(n))


@mcp.tool()
def sigma(n: int, k: int = 1) -> int:
    """Compute the sum of k-th powers of divisors of n.

    Args:
        n: Positive integer.
        k: Power exponent (default 1).

    Returns:
        Sum of k-th powers of divisors of n.

    Example:
        >>> sigma(10)
        18
        >>> sigma(10, 2)
        130
        >>> eval_expression("vector(10, n, sigma(n))")
        [1, 3, 4, 7, 6, 12, 8, 15, 13, 18]
    """
    pari = _get_pari()
    return int(pari.sigma(n, k))


@mcp.tool()
def moebius(n: int) -> int:
    """Compute the Möbius function mu(n).

    Args:
        n: Positive integer.

    Returns:
        mu(n): 1 if n is square-free with even number of prime factors,
               -1 if square-free with odd number of factors,
               0 if n has a squared prime factor.

    Example:
        >>> moebius(10)
        1
        >>> moebius(30)
        -1
        >>> moebius(12)
        0
        >>> eval_expression("vector(15, n, moebius(n))")
        [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0, -1, 1]
    """
    pari = _get_pari()
    return int(pari.moebius(n))


@mcp.tool()
def jacobi(a: int, n: int) -> int:
    """Compute the Jacobi symbol (a/n).

    Args:
        a: Integer.
        n: Odd positive integer.

    Returns:
        The Jacobi symbol (a/n), which is -1, 0, or 1.

    Example:
        >>> jacobi(10, 21)
        -1
    """
    pari = _get_pari()
    return int(pari.kronecker(a, n))


@mcp.tool()
def legendre(a: int, p: int) -> int:
    """Compute the Legendre symbol (a/p).

    Args:
        a: Integer.
        p: Odd prime.

    Returns:
        The Legendre symbol (a/p): -1, 0, or 1.

    Example:
        >>> legendre(10, 13)
        -1
    """
    pari = _get_pari()
    return int(pari.legendre(a, p))


@mcp.tool()
def znorder(x: int, n: int) -> int:
    """Compute the multiplicative order of x modulo n.

    Args:
        x: Integer coprime to n.
        n: Positive integer.

    Returns:
        The smallest k > 0 such that x^k ≡ 1 (mod n).

    Example:
        >>> znorder(2, 5)
        4
    """
    pari = _get_pari()
    return int(pari.znorder(x, n))


@mcp.tool()
def znstar(n: int) -> list:
    """Compute the structure of (Z/nZ)*.

    Args:
        n: Positive integer.

    Returns:
        [N, cyc, gen] where N = phi(n), cyc gives the cyclic decomposition,
        and gen gives generators.

    Example:
        >>> znstar(12)
        [2, [2, 2], [...]]
    """
    pari = _get_pari()
    return _convert_to_python(pari.znstar(n))


@mcp.tool()
def factorial(n: int) -> int:
    """Compute the factorial n!.

    Args:
        n: Non-negative integer.

    Returns:
        n! as an integer.

    Example:
        >>> factorial(5)
        120
    """
    pari = _get_pari()
    return int(pari.factorial(n))


@mcp.tool()
def binomial(n: int, k: int) -> int:
    """Compute the binomial coefficient C(n,k).

    Args:
        n: Non-negative integer.
        k: Non-negative integer.

    Returns:
        The binomial coefficient C(n,k).

    Example:
        >>> binomial(10, 3)
        120
    """
    pari = _get_pari()
    return int(pari.binomial(n, k))


@mcp.tool()
def fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number.

    Args:
        n: Non-negative integer.

    Returns:
        The nth Fibonacci number.

    Example:
        >>> fibonacci(10)
        55
        >>> eval_expression("vector(10, n, fibonacci(n))")
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    pari = _get_pari()
    return int(pari.fibonacci(n))


@mcp.tool()
def lucas(n: int) -> int:
    """Compute the nth Lucas number.

    Args:
        n: Non-negative integer.

    Returns:
        The nth Lucas number.

    Example:
        >>> lucas(10)
        123
        >>> eval_expression("vector(10, n, lucas(n))")
        [2, 1, 3, 4, 7, 11, 18, 29, 47, 76]
    """
    pari = _get_pari()
    # Lucas numbers: L_n = F_{n-1} + F_{n+1}
    fnm1 = pari.fibonacci(n - 1) if n > 0 else 2
    fnp1 = pari.fibonacci(n + 1)
    return int(fnm1 + fnp1)


@mcp.tool()
def polcyclo(n: int, v: str = "x") -> Any:
    """Compute the nth cyclotomic polynomial.

    Args:
        n: Positive integer.
        v: Variable name (default 'x').

    Returns:
        The nth cyclotomic polynomial.

    Example:
        >>> polcyclo(5)
        x^4 + x^3 + x^2 + x + 1
    """
    pari = _get_pari()
    return _convert_to_python(pari.polcyclo(n, v))


@mcp.tool()
def polchebyshev(n: int, v: str = "x") -> Any:
    """Compute the nth Chebyshev polynomial of the first kind.

    Args:
        n: Non-negative integer.
        v: Variable name (default 'x').

    Returns:
        The nth Chebyshev polynomial T_n(x).

    Example:
        >>> polchebyshev(3)
        4*x^3 - 3*x
    """
    pari = _get_pari()
    return _convert_to_python(pari.polchebyshev(n, v))


@mcp.tool()
def pollegendre(n: int, v: str = "x") -> Any:
    """Compute the nth Legendre polynomial.

    Args:
        n: Non-negative integer.
        v: Variable name (default 'x').

    Returns:
        The nth Legendre polynomial P_n(x).

    Example:
        >>> pollegendre(3)
        5/2*x^3 - 3/2*x
    """
    pari = _get_pari()
    return _convert_to_python(pari.pollegendre(n, v))


@mcp.tool()
def polhermite(n: int, v: str = "x") -> Any:
    """Compute the nth Hermite polynomial (probabilists' version).

    Args:
        n: Non-negative integer.
        v: Variable name (default 'x').

    Returns:
        The nth Hermite polynomial He_n(x).

    Example:
        >>> polhermite(3)
        x^3 - 3*x
    """
    pari = _get_pari()
    return _convert_to_python(pari.polhermiter(n, v))


@mcp.tool()
def polroots(pol: str) -> list:
    """Compute the complex roots of a polynomial.

    Args:
        pol: Polynomial as a string (e.g., "x^3 - 1").

    Returns:
        List of roots with multiplicities.

    Example:
        >>> polroots("x^2 + 1")
        [-I, I]
    """
    pari = _get_pari()
    return _convert_to_python(pari.polroots(pol))


@mcp.tool()
def polrootsmod(pol: str, p: int) -> list:
    """Compute the roots of a polynomial modulo p.

    Args:
        pol: Polynomial as a string.
        p: Prime modulus.

    Returns:
        List of roots modulo p.

    Example:
        >>> polrootsmod("x^2 + 1", 5)
        [2, 3]
    """
    pari = _get_pari()
    return _convert_to_python(pari.polrootsmod(pol, p))


@mcp.tool()
def polrootspadic(pol: str, p: int, n: int = 1) -> list:
    """Compute the p-adic roots of a polynomial.

    Args:
        pol: Polynomial as a string.
        p: Prime p.
        n: p-adic precision.

    Returns:
        List of p-adic roots.

    Example:
        >>> polrootspadic("x^2 - 2", 2, 5)
        [1 + 2 + 2^2 + 2^3 + 2^4 + O(2^5)]
    """
    pari = _get_pari()
    return _convert_to_python(pari.polrootspadic(pol, p, n))


@mcp.tool()
def factorpadic(pol: str, p: int, n: int = 1) -> list:
    """Factor a polynomial over the p-adic numbers.

    Args:
        pol: Polynomial as a string.
        p: Prime p.
        n: p-adic precision.

    Returns:
        Factorization as list of [factor, exponent] pairs.

    Example:
        >>> factorpadic("x^2 - 2", 2, 5)
    """
    pari = _get_pari()
    return _convert_to_python(pari.factorpadic(pol, p, n))


@mcp.tool()
def deriv(pol: str, v: str = "x") -> Any:
    """Compute the derivative of a polynomial.

    Args:
        pol: Polynomial as a string.
        v: Variable name.

    Returns:
        The derivative polynomial.

    Example:
        >>> deriv("x^3 + 2*x")
        3*x^2 + 2
    """
    pari = _get_pari()
    return _convert_to_python(pari.deriv(pol, v))


@mcp.tool()
def integ(pol: str, v: str = "x") -> Any:
    """Compute the integral of a polynomial.

    Args:
        pol: Polynomial as a string.
        v: Variable name.

    Returns:
        The integral polynomial (constant term is 0).

    Example:
        >>> integ("x^2")
        1/3*x^3
    """
    pari = _get_pari()
    return _convert_to_python(pari.integ(pol, v))


@mcp.tool()
def resultant(pol1: str, pol2: str, v: str = "x") -> int:
    """Compute the resultant of two polynomials.

    Args:
        pol1: First polynomial.
        pol2: Second polynomial.
        v: Variable name.

    Returns:
        The resultant as an integer.

    Example:
        >>> resultant("x^2 - 1", "x^3 - 1")
        0
    """
    pari = _get_pari()
    return int(pari.resultant(pol1, pol2, v))


@mcp.tool()
def disc(pol: str, v: str = "x") -> int:
    """Compute the discriminant of a polynomial.

    Args:
        pol: Polynomial.
        v: Variable name.

    Returns:
        The discriminant.

    Example:
        >>> disc("x^3 - 3*x + 1")
        81
    """
    pari = _get_pari()
    return int(pari.disc(pol, v))


@mcp.tool()
def norm(pol: Any, v: str = "x") -> Any:
    """Compute the norm of a polynomial/algebraic number.

    Args:
        pol: Polynomial or algebraic number.
        v: Variable name.

    Returns:
        The norm.

    Example:
        >>> norm("Mod(x, x^2 + 1)")
    """
    pari = _get_pari()
    return _convert_to_python(pari.norm(pol, v))


@mcp.tool()
def trace(pol: Any, v: str = "x") -> Any:
    """Compute the trace of a polynomial/algebraic number.

    Args:
        pol: Polynomial or algebraic number.
        v: Variable name.

    Returns:
        The trace.

    Example:
        >>> trace("Mod(x, x^2 + 1)")
    """
    pari = _get_pari()
    return _convert_to_python(pari.trace(pol, v))


@mcp.tool()
def subst(pol: str, v: str, expr: Any) -> Any:
    """Substitute a variable in a polynomial.

    Args:
        pol: Polynomial.
        v: Variable to replace.
        expr: Expression to substitute.

    Returns:
        The substituted polynomial.

    Example:
        >>> subst("x^2 + 1", "x", "y + 1")
        (y + 1)^2 + 1
    """
    pari = _get_pari()
    return _convert_to_python(pari.subst(pol, v, expr))


@mcp.tool()
def Mod(a: Any, b: Any) -> Any:
    """Create a modular number or polynomial.

    Args:
        a: Value.
        b: Modulus (integer or polynomial).

    Returns:
        The modular object.

    Example:
        >>> Mod(2, 17)
        Mod(2, 17)
    """
    pari = _get_pari()
    return _convert_to_python(pari.Mod(a, b))


@mcp.tool()
def lift(mod: Any) -> Any:
    """Lift a modular object (remove Mod wrapper).

    Args:
        mod: A modular object.

    Returns:
        The lifted value.

    Example:
        >>> lift(Mod(2, 17))
        2
    """
    pari = _get_pari()
    return _convert_to_python(pari.lift(mod))


@mcp.tool()
def centerlift(mod: Any) -> Any:
    """Lift a modular object with centered representatives.

    Args:
        mod: A modular object.

    Returns:
        The centered lift.

    Example:
        >>> centerlift(Mod(10, 17))
        -7
    """
    pari = _get_pari()
    return _convert_to_python(pari.centerlift(mod))


@mcp.tool()
def nfinit(pol: str) -> Any:
    """Initialize a number field defined by a polynomial.

    Args:
        pol: Defining polynomial as a string.

    Returns:
        The number field structure.

    Example:
        >>> nf = nfinit("x^2 + 1")
        >>> nf
        [y^2 + 1, [...], ...]
    """
    pari = _get_pari()
    return _convert_to_python(pari.nfinit(pol))


@mcp.tool()
def bnfinit(pol: str, do_buchall: int = 0) -> Any:
    """Initialize a number field with Buchmann's algorithm.

    Args:
        pol: Defining polynomial.
        do_buchall: Compute full Buchmann's algorithm (default 0).

    Returns:
        The BNF structure.

    Example:
        >>> bnf = bnfinit("x^2 + 1")
    """
    pari = _get_pari()
    return _convert_to_python(pari.bnfinit(pol, do_buchall))


@mcp.tool()
def bnrinit(nf: Any, modulus: Any, sign: int = 1) -> Any:
    """Initialize a ray number field (class field).

    Args:
        nf: Number field from nfinit.
        modulus: Modulus for ray class group.
        sign: 1 for full, -1 for real.

    Returns:
        The BNR structure.

    Example:
        >>> bnrinit(nfinit("x^2 + 1"), 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.bnrinit(nf, modulus, sign))


@mcp.tool()
def idealadd(nf: Any, ideal1: Any, ideal2: Any) -> Any:
    """Add two ideals in a number field.

    Args:
        nf: Number field structure.
        ideal1: First ideal.
        ideal2: Second ideal.

    Returns:
        The sum ideal.

    Example:
        >>> nf = nfinit("x^2 + 1")
        >>> idealadd(nf, 2, 3)
    """
    pari = _get_pari()
    return _convert_to_python(pari.idealadd(nf, ideal1, ideal2))


@mcp.tool()
def idealmul(nf: Any, ideal1: Any, ideal2: Any) -> Any:
    """Multiply two ideals in a number field.

    Args:
        nf: Number field structure.
        ideal1: First ideal.
        ideal2: Second ideal.

    Returns:
        The product ideal.

    Example:
        >>> nf = nfinit("x^2 + 1")
    """
    pari = _get_pari()
    return _convert_to_python(pari.idealmul(nf, ideal1, ideal2))


@mcp.tool()
def idealpow(nf: Any, ideal: Any, n: int) -> Any:
    """Compute a power of an ideal.

    Args:
        nf: Number field structure.
        ideal: Ideal to power.
        n: Exponent.

    Returns:
        The ideal^n.

    Example:
        >>> nf = nfinit("x^2 + 1")
    """
    pari = _get_pari()
    return _convert_to_python(pari.idealpow(nf, ideal, n))


@mcp.tool()
def idealfactor(nf: Any, ideal: Any) -> list:
    """Factor an ideal in a number field.

    Args:
        nf: Number field structure.
        ideal: Ideal to factor.

    Returns:
        Factorization as [prime_ideals, exponents].

    Example:
        >>> nf = nfinit("x^2 + 1")
    """
    pari = _get_pari()
    return _convert_to_python(pari.idealfactor(nf, ideal))


@mcp.tool()
def ellinit(pol: str, sign: int = 1) -> Any:
    """Initialize an elliptic curve.

    Args:
        pol: Short Weierstrass equation (e.g., "y^2 = x^3 - x").
        sign: 1 for minimal model.

    Returns:
        The elliptic curve structure.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.ellinit(pol, sign))


@mcp.tool()
def elladd(E1: Any, E2: Any) -> Any:
    """Add two points on an elliptic curve.

    Args:
        E1: Elliptic curve (or point).
        E2: Elliptic curve (or point).

    Returns:
        The sum point.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.elladd(E1, E2))


@mcp.tool()
def ellmul(E: Any, n: int, P: Any = None) -> Any:
    """Multiply a point on an elliptic curve by an integer.

    Args:
        E: Elliptic curve structure.
        n: Integer multiplier.
        P: Point (optional, if E is a point).

    Returns:
        The point [n]P.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    if P is not None:
        return _convert_to_python(pari.ellmul(E, P, n))
    return _convert_to_python(pari.ellmul(E, n))


@mcp.tool()
def ellorder(E: Any, P: Any) -> int:
    """Compute the order of a point on an elliptic curve.

    Args:
        E: Elliptic curve structure.
        P: Point on the curve.

    Returns:
        The order of P.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return int(pari.ellorder(E, P))


@mcp.tool()
def elllog(E: Any, P: Any, G: Any) -> int:
    """Compute the discrete logarithm of a point on an elliptic curve.

    Args:
        E: Elliptic curve structure.
        P: Point.
        G: Base point.

    Returns:
        The integer n such that n*G = P.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return int(pari.elllog(E, P, G))


@mcp.tool()
def ellap(E: Any, p: int) -> int:
    """Compute the trace of Frobenius for an elliptic curve at prime p.

    Args:
        E: Elliptic curve structure.
        p: Prime.

    Returns:
        The trace of Frobenius a_p.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
        >>> ellap(E, 5)
        -2
    """
    pari = _get_pari()
    return int(pari.ellap(E, p))


@mcp.tool()
def elltors(E: Any) -> list:
    """Compute the torsion subgroup of an elliptic curve.

    Args:
        E: Elliptic curve structure.

    Returns:
        [order, structure, generators].

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
        >>> elltors(E)
    """
    pari = _get_pari()
    return _convert_to_python(pari.elltors(E))


@mcp.tool()
def ellglobalred(E: Any) -> list:
    """Compute the global reduction type of an elliptic curve.

    Args:
        E: Elliptic curve structure.

    Returns:
        [conductor, Kodaira type, global Tamagawa number].

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.ellglobalred(E))


@mcp.tool()
def elllocalred(E: Any, p: int) -> list:
    """Compute the local reduction type at prime p.

    Args:
        E: Elliptic curve structure.
        p: Prime.

    Returns:
        [Kodaira type, exponent, Tamagawa number, conductor exponent].

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.elllocalred(E, p))


@mcp.tool()
def ellheight(E: Any, P: Any, flags: int = 0) -> float:
    """Compute the canonical height of a point on an elliptic curve.

    Args:
        E: Elliptic curve structure.
        P: Point on the curve.
        flags: Computation flags.

    Returns:
        The canonical height.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return float(pari.ellheight(E, P, flags))


@mcp.tool()
def ellj(E: Any) -> Any:
    """Compute the j-invariant of an elliptic curve.

    Args:
        E: Elliptic curve structure or polynomial.

    Returns:
        The j-invariant.

    Example:
        >>> ellj("x^3 - x")
        1728
    """
    pari = _get_pari()
    return _convert_to_python(pari.ellj(E))


@mcp.tool()
def elleta(E: Any) -> list:
    """Compute the eta-quotients for an elliptic curve.

    Args:
        E: Elliptic curve structure.

    Returns:
        [eta1, eta2, eta3].

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.elleta(E))


@mcp.tool()
def ellwp(E: Any, n: int = 6, flags: int = 0) -> Any:
    """Compute the Weierstrass p-function.

    Args:
        E: Elliptic curve structure.
        n: Number of terms (default 6).
        flags: Computation flags.

    Returns:
        The Weierstrass p-function.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.ellwp(E, n, flags))


@mcp.tool()
def ellzeta(E: Any, z: Any) -> Any:
    """Compute the Weierstrass zeta function.

    Args:
        E: Elliptic curve structure.
        z: Point.

    Returns:
        The zeta value.

    Example:
        >>> E = ellinit("y^2 = x^3 - x")
    """
    pari = _get_pari()
    return _convert_to_python(pari.ellzeta(E, z))


@mcp.tool()
def matid(n: int) -> Any:
    """Create an n x n identity matrix.

    Args:
        n: Size of the matrix.

    Returns:
        The n x n identity matrix.

    Example:
        >>> matid(3)
        [1, 0, 0; 0, 1, 0; 0, 0, 1]
    """
    pari = _get_pari()
    return _convert_to_python(pari.matid(n))


@mcp.tool()
def matzero(m: int, n: int = 0) -> Any:
    """Create a zero matrix.

    Args:
        m: Number of rows (or size if n=0).
        n: Number of columns (default 0).

    Returns:
        The zero matrix.

    Example:
        >>> matzero(3)
        [0, 0, 0; 0, 0, 0; 0, 0, 0]
    """
    pari = _get_pari()
    if n == 0:
        n = m
    # Create zero matrix using matrix with zeros
    entries = [0] * (m * n)
    return _convert_to_python(pari.matrix(m, n, entries))


@mcp.tool()
def matdet(m: Any) -> Any:
    """Compute the determinant of a matrix.

    Args:
        m: Square matrix.

    Returns:
        The determinant.

    Example:
        >>> matdet("[1, 2; 3, 4]")
        -2
    """
    pari = _get_pari()
    return _convert_to_python(pari.matdet(m))


@mcp.tool()
def matinv(m: Any) -> Any:
    """Compute the inverse of a matrix.

    Args:
        m: Invertible square matrix.

    Returns:
        The inverse matrix.

    Example:
        >>> matinv("[1, 2; 3, 4]")
    """
    pari = _get_pari()
    return _convert_to_python(pari.matinv(m))


@mcp.tool()
def matrank(m: Any) -> int:
    """Compute the rank of a matrix.

    Args:
        m: Matrix.

    Returns:
        The rank.

    Example:
        >>> matrank("[1, 2; 2, 4]")
        1
    """
    pari = _get_pari()
    return int(pari.matrank(m))


@mcp.tool()
def matker(m: Any) -> Any:
    """Compute the kernel of a matrix.

    Args:
        m: Matrix.

    Returns:
        Basis of the kernel.

    Example:
        >>> matker("[1, 2; 2, 4]")
    """
    pari = _get_pari()
    return _convert_to_python(pari.matker(m))


@mcp.tool()
def matimage(m: Any) -> Any:
    """Compute the image of a matrix.

    Args:
        m: Matrix.

    Returns:
        Basis of the image.

    Example:
        >>> matimage("[1, 2; 2, 4]")
    """
    pari = _get_pari()
    return _convert_to_python(pari.matimage(m))


@mcp.tool()
def mateigen(m: Any) -> list:
    """Compute the eigenvalues of a matrix.

    Args:
        m: Square matrix.

    Returns:
        List of eigenvalues.

    Example:
        >>> mateigen("[1, 2; 2, 1]")
        [3, -1]
    """
    pari = _get_pari()
    return _convert_to_python(pari.mateigen(m))


@mcp.tool()
def matcharpoly(m: Any, v: str = "x") -> Any:
    """Compute the characteristic polynomial of a matrix.

    Args:
        m: Square matrix.
        v: Variable name.

    Returns:
        The characteristic polynomial.

    Example:
        >>> matcharpoly("[1, 2; 3, 4]")
        x^2 - 5*x - 2
    """
    pari = _get_pari()
    return _convert_to_python(pari.matcharpoly(m, v))


@mcp.tool()
def hess(m: Any) -> Any:
    """Compute the Hessenberg form of a matrix.

    Args:
        m: Square matrix.

    Returns:
        The Hessenberg matrix.

    Example:
        >>> hess("[1, 2, 3; 4, 5, 6; 7, 8, 9]")
    """
    pari = _get_pari()
    return _convert_to_python(pari.hess(m))


@mcp.tool()
def List(x: Any = None) -> Any:
    """Create an empty list or convert to a list.

    Args:
        x: Optional object to convert.

    Returns:
        A PARI list.

    Example:
        >>> L = List()
        >>> L.listput(42, 1)
    """
    pari = _get_pari()
    if x is None:
        return _convert_to_python(pari.List())
    return _convert_to_python(pari.List(x))


@mcp.tool()
def Vec(x: Any, n: int = 0) -> Any:
    """Convert to a row vector.

    Args:
        x: Object to convert.
        n: Optional length specification.

    Returns:
        Row vector.

    Example:
        >>> Vec("[1, 2, 3]")
        [1, 2, 3]
    """
    pari = _get_pari()
    return _convert_to_python(pari.Vec(x, n))


@mcp.tool()
def Col(x: Any, n: int = 0) -> Any:
    """Convert to a column vector.

    Args:
        x: Object to convert.
        n: Optional length specification.

    Returns:
        Column vector.

    Example:
        >>> Col("[1, 2, 3]")
    """
    pari = _get_pari()
    return _convert_to_python(pari.Col(x, n))


@mcp.tool()
def Mat(x: Any) -> Any:
    """Convert to a matrix.

    Args:
        x: Object to convert.

    Returns:
        Matrix.

    Example:
        >>> Mat("[1, 2, 3]")
        [1, 2, 3]
    """
    pari = _get_pari()
    return _convert_to_python(pari.Mat(x))


@mcp.tool()
def Set(x: Any) -> list:
    """Convert to a set.

    Args:
        x: Object to convert.

    Returns:
        Sorted list of unique elements.

    Example:
        >>> Set("[1, 2, 1, 3]")
        [1, 2, 3]
    """
    pari = _get_pari()
    return _convert_to_python(pari.Set(x))


@mcp.tool()
def Pol(x: Any, v: str = "x") -> Any:
    """Convert to a polynomial.

    Args:
        x: Vector of coefficients or scalar.
        v: Variable name.

    Returns:
        Polynomial.

    Example:
        >>> Pol("[1, 2, 3]")
        x^2 + 2*x + 3
    """
    pari = _get_pari()
    return _convert_to_python(pari.Pol(x, v))


@mcp.tool()
def Polrev(x: Any, v: str = "x") -> Any:
    """Convert to a polynomial (reverse order).

    Args:
        x: Vector of coefficients (constant term first).
        v: Variable name.

    Returns:
        Polynomial.

    Example:
        >>> Polrev("[1, 2, 3]")
        3*x^2 + 2*x + 1
    """
    pari = _get_pari()
    return _convert_to_python(pari.Polrev(x, v))


@mcp.tool()
def Ser(x: Any, v: str = "x", d: int = 0) -> Any:
    """Convert to a power series.

    Args:
        x: Polynomial or vector.
        v: Variable name.
        d: Precision (number of terms).

    Returns:
        Power series.

    Example:
        >>> Ser("x + 1", "x", 5)
        1 + x + O(x^5)
    """
    pari = _get_pari()
    return _convert_to_python(pari.Ser(x, v, d))


@mcp.tool()
def pi(precision: int = 0) -> float:
    """Get the value of pi.

    Args:
        precision: Optional precision in bits.

    Returns:
        Value of pi.

    Example:
        >>> pi()
        3.14159265358979
    """
    pari = _get_pari()
    return float(pari.pi(precision))


@mcp.tool()
def euler(precision: int = 0) -> float:
    """Get Euler's constant.

    Args:
        precision: Optional precision in bits.

    Returns:
        Euler's constant gamma.

    Example:
        >>> euler()
        0.5772156649015329
    """
    pari = _get_pari()
    return float(pari.euler(precision))


@mcp.tool()
def Catalan(precision: int = 0) -> float:
    """Get Catalan's constant.

    Args:
        precision: Optional precision in bits.

    Returns:
        Catalan's constant G.

    Example:
        >>> Catalan()
        0.915965594177219
    """
    pari = _get_pari()
    return float(pari.Catalan(precision))


@mcp.tool()
def complex(real: float, imag: float) -> complex:  # type: ignore[valid-type]
    """Create a complex number.

    Args:
        real: Real part.
        imag: Imaginary part.

    Returns:
        Complex number.

    Example:
        >>> complex(1, 2)
        1 + 2*I
    """
    pari = _get_pari()
    return complex(pari.complex(real, imag))  # type: ignore[call-arg]


@mcp.tool()
def I() -> complex:  # type: ignore[valid-type]
    """Get the imaginary unit.

    Returns:
        The imaginary unit I = sqrt(-1).

    Example:
        >>> I()
        I
    """
    pari = _get_pari()
    return complex(pari.I())  # type: ignore[call-arg]


@mcp.tool()
def one() -> int:
    """Get the integer 1.

    Returns:
        Integer 1.

    Example:
        >>> one()
        1
    """
    pari = _get_pari()
    return int(pari.one())


@mcp.tool()
def zero() -> int:
    """Get the integer 0.

    Returns:
        Integer 0.

    Example:
        >>> zero()
        0
    """
    pari = _get_pari()
    return int(pari.zero())


@mcp.tool()
def abs(x: Any, precision: int = 0) -> Any:
    """Compute absolute value.

    Args:
        x: Number or object.
        precision: Optional precision.

    Returns:
        Absolute value.

    Example:
        >>> abs(-5)
        5
    """
    pari = _get_pari()
    return _convert_to_python(pari.abs(x, precision))


@mcp.tool()
def sqrt(x: Any, precision: int = 0) -> Any:
    """Compute square root.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        Square root.

    Example:
        >>> sqrt(2)
        1.414213562373095
    """
    pari = _get_pari()
    return _convert_to_python(pari.sqrt(x, precision))


@mcp.tool()
def exp(x: Any, precision: int = 0) -> Any:
    """Compute exponential.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        e^x.

    Example:
        >>> exp(1)
        2.71828182845905
    """
    pari = _get_pari()
    return _convert_to_python(pari.exp(x, precision))


@mcp.tool()
def log(x: Any, precision: int = 0) -> Any:
    """Compute natural logarithm.

    Args:
        x: Positive number.
        precision: Optional precision.

    Returns:
        log(x).

    Example:
        >>> log(2)
        0.693147180559945
    """
    pari = _get_pari()
    return _convert_to_python(pari.log(x, precision))


@mcp.tool()
def sin(x: Any, precision: int = 0) -> Any:
    """Compute sine.

    Args:
        x: Number (in radians).
        precision: Optional precision.

    Returns:
        sin(x).

    Example:
        >>> sin(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.sin(x, precision))


@mcp.tool()
def cos(x: Any, precision: int = 0) -> Any:
    """Compute cosine.

    Args:
        x: Number (in radians).
        precision: Optional precision.

    Returns:
        cos(x).

    Example:
        >>> cos(0)
        1
    """
    pari = _get_pari()
    return _convert_to_python(pari.cos(x, precision))


@mcp.tool()
def tan(x: Any, precision: int = 0) -> Any:
    """Compute tangent.

    Args:
        x: Number (in radians).
        precision: Optional precision.

    Returns:
        tan(x).

    Example:
        >>> tan(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.tan(x, precision))


@mcp.tool()
def asin(x: Any, precision: int = 0) -> Any:
    """Compute arcsine.

    Args:
        x: Number in [-1, 1].
        precision: Optional precision.

    Returns:
        arcsin(x).

    Example:
        >>> asin(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.asin(x, precision))


@mcp.tool()
def acos(x: Any, precision: int = 0) -> Any:
    """Compute arccosine.

    Args:
        x: Number in [-1, 1].
        precision: Optional precision.

    Returns:
        arccos(x).

    Example:
        >>> acos(1)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.acos(x, precision))


@mcp.tool()
def atan(x: Any, precision: int = 0) -> Any:
    """Compute arctangent.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        arctan(x).

    Example:
        >>> atan(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.atan(x, precision))


@mcp.tool()
def sinh(x: Any, precision: int = 0) -> Any:
    """Compute hyperbolic sine.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        sinh(x).

    Example:
        >>> sinh(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.sinh(x, precision))


@mcp.tool()
def cosh(x: Any, precision: int = 0) -> Any:
    """Compute hyperbolic cosine.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        cosh(x).

    Example:
        >>> cosh(0)
        1
    """
    pari = _get_pari()
    return _convert_to_python(pari.cosh(x, precision))


@mcp.tool()
def tanh(x: Any, precision: int = 0) -> Any:
    """Compute hyperbolic tangent.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        tanh(x).

    Example:
        >>> tanh(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.tanh(x, precision))


@mcp.tool()
def asinh(x: Any, precision: int = 0) -> Any:
    """Compute inverse hyperbolic sine.

    Args:
        x: Number.
        precision: Optional precision.

    Returns:
        asinh(x).

    Example:
        >>> asinh(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.asinh(x, precision))


@mcp.tool()
def acosh(x: Any, precision: int = 0) -> Any:
    """Compute inverse hyperbolic cosine.

    Args:
        x: Number >= 1.
        precision: Optional precision.

    Returns:
        acosh(x).

    Example:
        >>> acosh(1)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.acosh(x, precision))


@mcp.tool()
def atanh(x: Any, precision: int = 0) -> Any:
    """Compute inverse hyperbolic tangent.

    Args:
        x: Number in (-1, 1).
        precision: Optional precision.

    Returns:
        atanh(x).

    Example:
        >>> atanh(0)
        0
    """
    pari = _get_pari()
    return _convert_to_python(pari.atanh(x, precision))


@mcp.tool()
def agm(x: Any, y: Any = None, precision: int = 0) -> Any:
    """Compute the arithmetic-geometric mean.

    Args:
        x: First number.
        y: Second number (if None, uses x and 1).
        precision: Optional precision.

    Returns:
        AGM(x, y).

    Example:
        >>> agm(1, 2)
        1.456791031...
    """
    pari = _get_pari()
    if y is None:
        return _convert_to_python(pari.agm(x, precision))
    return _convert_to_python(pari.agm(x, y, precision))


@mcp.tool()
def airy(z: Any) -> tuple:
    """Compute Airy functions Ai(z) and Bi(z).

    Args:
        z: Complex argument.

    Returns:
        [Ai, Bi].

    Example:
        >>> airy(0)
        [0.3550280539..., 0.259285...]

    """
    pari = _get_pari()
    return _convert_to_python(pari.airy(z))


@mcp.tool()
def genus2red(P: Any, p: int = 0) -> Any:
    """Reduce a genus 2 curve.

    Args:
        P: Hyperelliptic polynomial y^2 = P.
        p: Optional prime for local reduction.

    Returns:
        Reduction data.

    Example:
        >>> genus2red("x^5 - 1")
    """
    pari = _get_pari()
    if p == 0:
        return _convert_to_python(pari.genus2red(P))
    return _convert_to_python(pari.genus2red(P, p))


@mcp.tool()
def algdep(x: Any, k: int, flag: int = 0) -> Any:
    """Find polynomial of degree k with integer coefficients approximating x.

    Args:
        x: Real/complex/p-adic number.
        k: Degree of polynomial.
        flag: Optional accuracy flag.

    Returns:
        Polynomial.

    Example:
        >>> algdep(sqrt(2), 2)
        x^2 - 2
    """
    pari = _get_pari()
    return _convert_to_python(pari.algdep(x, k, flag))


@mcp.tool()
def vector(n: int, entries: list = None) -> Any:
    """Create a vector of length n.

    Args:
        n: Length.
        entries: List of entries (optional).

    Returns:
        Vector.

    Example:
        >>> vector(3, [1, 2, 3])
        [1, 2, 3]
    """
    pari = _get_pari()
    if entries is None:
        return _convert_to_python(pari.vector(n))
    return _convert_to_python(pari.vector(n, entries))


@mcp.tool()
def matrix(m: int, n: int = 0, entries: list = None) -> Any:
    """Create an m x n matrix.

    Args:
        m: Number of rows (or size if n=0).
        n: Number of columns (default 0).
        entries: List of entries (optional).

    Returns:
        Matrix.

    Example:
        >>> matrix(2, 3, [1, 2, 3, 4, 5, 6])
        [1, 2, 3; 4, 5, 6]
    """
    pari = _get_pari()
    if entries is None:
        if n == 0:
            return _convert_to_python(pari.matrix(m))
        return _convert_to_python(pari.matrix(m, n))
    return _convert_to_python(pari.matrix(m, n, entries))


@mcp.tool()
def polsubcyclo(n: int, d: int, v: str = "x") -> list:
    """Compute sub-cyclotomic polynomials.

    Args:
        n: Cyclotomic field order.
        d: Degree of subfield.
        v: Variable name.

    Returns:
        List of polynomials.

    Example:
        >>> polsubcyclo(8, 4)
        [x^4 + 1]
    """
    pari = _get_pari()
    return _convert_to_python(pari.polsubcyclo(n, d, v))


@mcp.tool()
def init_primes(M: int) -> None:
    """Initialize the primes table up to M.

    Args:
        M: Upper bound for primes.

    Example:
        >>> init_primes(1000)
    """
    pari = _get_pari()
    pari.init_primes(M)


@mcp.tool()
def addprimes(primes: list = None) -> list:
    """Add primes to the factorisation table.

    Args:
        primes: List of primes to add (or None to get current list).

    Returns:
        Current list of extra primes.

    Example:
        >>> addprimes([10007])
    """
    pari = _get_pari()
    if primes is None:
        return _convert_to_python(pari.addprimes())
    return _convert_to_python(pari.addprimes(primes))


@mcp.tool()
def removeprimes(primes: list = None) -> list:
    """Remove primes from the factorisation table.

    Args:
        primes: List of primes to remove (or None to clear).

    Returns:
        Updated list of extra primes.

    Example:
        >>> removeprimes([10007])
    """
    pari = _get_pari()
    if primes is None:
        return _convert_to_python(pari.removeprimes())
    return _convert_to_python(pari.removeprimes(primes))


@mcp.tool()
def ispower(n: int, k: int = 0) -> Any:
    """Test if n is a perfect k-th power.

    Args:
        n: Integer.
        k: Exponent (0 or omitted means test any power).

    Returns:
        k (exponent) if n is a perfect k-th power, else 0.

    Example:
        >>> ispower(64)
        6
    """
    pari = _get_pari()
    if k == 0:
        return _convert_to_python(pari.ispower(n))
    return _convert_to_python(pari.ispower(n, k))


@mcp.tool()
def is_square(n: int) -> bool:
    """Test if n is a perfect square.

    Args:
        n: Integer.

    Returns:
        True if n is a perfect square.

    Example:
        >>> is_square(25)
        True
    """
    pari = _get_pari()
    # Check if n is a perfect square using ispower(n)
    result = pari.ispower(n)
    if result == 0:
        return False
    return result == 2


@mcp.tool()
def nextprime(n: int) -> int:
    """Find the next prime after n.

    Args:
        n: Integer.

    Returns:
        The smallest prime > n.

    Example:
        >>> nextprime(10)
        11
    """
    pari = _get_pari()
    return int(pari.nextprime(n))


@mcp.tool()
def prevprime(n: int) -> int:
    """Find the previous prime before n.

    Args:
        n: Integer > 2.

    Returns:
        The largest prime < n.

    Example:
        >>> prevprime(10)
        7
    """
    pari = _get_pari()
    return int(pari.prevprime(n))


@mcp.tool()
def Qfb(a: int, b: int, c: int, D: int = 0, precision: int = 0) -> Any:
    """Create a binary quadratic form.

    Args:
        a, b, c: Coefficients (ax^2 + bxy + cy^2).
        D: Optional Shanks' distance.
        precision: Optional precision.

    Returns:
        Binary quadratic form.

    Example:
        >>> Qfb(1, 0, 1)
        Qfb(1, 0, 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.Qfb(a, b, c, D, precision))


@mcp.tool()
def qfbsolve(Q: Any, n: int) -> Any:
    """Solve Q(x) = n for binary quadratic form Q.

    Args:
        Q: Binary quadratic form.
        n: Integer to represent.

    Returns:
        Solution vector or 0.

    Example:
        >>> qfbsolve(Qfb(1, 0, 1), 5)
    """
    pari = _get_pari()
    return _convert_to_python(pari.qfbsolve(Q, n))


@mcp.tool()
def qfbclassno(D: int, flags: int = 0) -> int:
    """Compute the class number of binary quadratic form discriminant D.

    Args:
        D: Discriminant (D ≡ 0, 1 mod 4, D > 0).
        flags: Computation flags.

    Returns:
        Class number.

    Example:
        >>> qfbclassno(5)
        1
        >>> eval_expression("vector(15, n, qfbclassno(-4*n))")
        [1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 4, 1, 2]
    """
    pari = _get_pari()
    return int(pari.qfbclassno(D, flags))


@mcp.tool()
def quadregulator(D: int, precision: int = 0) -> Any:
    """Compute the regulator of real quadratic field.

    Args:
        D: Discriminant of real quadratic field.
        precision: Optional precision.

    Returns:
        Regulator.

    Example:
        >>> quadregulator(5)
    """
    pari = _get_pari()
    return _convert_to_python(pari.quadregulator(D, precision))


@mcp.tool()
def quadratic_forms(D: int) -> list:
    """Compute reduced binary quadratic forms of discriminant D.

    Args:
        D: Discriminant (D ≡ 0, 1 mod 4, D ≠ 0).

    Returns:
        List of reduced forms.

    Example:
        >>> quadratic_forms(-3)
    """
    pari = _get_pari()
    return _convert_to_python(pari.quadratic_forms(D))


@mcp.tool()
def hilbert(n: int, m: int, p: int = 0) -> int:
    """Compute the Hilbert symbol (n, m) or (n, m)_p.

    Args:
        n: Integer.
        m: Integer.
        p: Prime (0 for infinite place).

    Returns:
        Hilbert symbol (1 or -1).

    Example:
        >>> hilbert(-1, 5)
        1
    """
    pari = _get_pari()
    return int(pari.hilbert(n, m, p))


@mcp.tool()
def bessel(nu: Any, x: Any, precision: int = 0) -> Any:
    """Compute the Bessel function J_nu(x).

    Args:
        nu: Order.
        x: Argument.
        precision: Optional precision.

    Returns:
        Bessel J value.

    Example:
        >>> bessel(0, 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.bessel(nu, x, precision))


@mcp.tool()
def besselh(nu: Any, x: Any, precision: int = 0) -> Any:
    """Compute the Bessel function H_nu(x).

    Args:
        nu: Order.
        x: Argument.
        precision: Optional precision.

    Returns:
        Bessel H value.

    Example:
        >>> besselh(0, 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.besselh(nu, x, precision))


@mcp.tool()
def theta(z: Any, tau: Any, precision: int = 0) -> Any:
    """Compute the theta function theta(z, tau).

    Args:
        z: Complex parameter.
        tau: Lattice parameter.
        precision: Optional precision.

    Returns:
        Theta value.

    Example:
        >>> theta(0, I)
    """
    pari = _get_pari()
    return _convert_to_python(pari.theta(z, tau, precision))


@mcp.tool()
def weber(z: Any, flag: int = 0, precision: int = 0) -> Any:
    """Compute the Weber function.

    Args:
        z: Complex parameter.
        flag: Which variant (0, 1, or 2).
        precision: Optional precision.

    Returns:
        Weber function value.

    Example:
        >>> weber(1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.weber(z, flag, precision))


@mcp.tool()
def eta(z: Any, flag: int = 0, precision: int = 0) -> Any:
    """Compute the Dedekind eta function.

    Args:
        z: Complex parameter with positive imaginary part.
        flag: Optional flag.
        precision: Optional precision.

    Returns:
        Eta value.

    Example:
        >>> eta(I)
    """
    pari = _get_pari()
    return _convert_to_python(pari.eta(z, flag, precision))


@mcp.tool()
def modular_lambda(tau: Any, precision: int = 0) -> Any:
    """Compute the modular lambda function.

    Args:
        tau: Lattice parameter (Im(tau) > 0).
        precision: Optional precision.

    Returns:
        Lambda value.

    Example:
        >>> modular_lambda(I)
    """
    pari = _get_pari()
    return _convert_to_python(pari.modular_lambda(tau, precision))


@mcp.tool()
def modulr_sym(s: Any, g: int = 1, precision: int = 0) -> Any:
    """Compute the modular symbol.

    Args:
        s: Complex number.
        g: Weight.
        precision: Optional precision.

    Returns:
        Modular symbol.

    Example:
        >>> modulr_sym(1 + I)
    """
    pari = _get_pari()
    return _convert_to_python(pari.modulr_sym(s, g, precision))


@mcp.tool()
def cusp_form(q: Any, weight: int = 1, v: int = 1) -> Any:
    """Create a cusp form from its q-expansion.

    Args:
        q: q-expansion.
        weight: Weight.
        v: Variable number.

    Returns:
        Cusp form.

    Example:
        >>> cusp_form("q - q^5")
    """
    pari = _get_pari()
    return _convert_to_python(pari.cusp_form(q, weight, v))


@mcp.tool()
def eisenstein(k: int, n: int = 1, precision: int = 0) -> Any:
    """Compute the Eisenstein series E_k(q).

    Args:
        k: Weight (even >= 2).
        n: Harmonic rank (default 1).
        precision: Optional precision.

    Returns:
        q-expansion of E_k.

    Example:
        >>> eisenstein(4)
    """
    pari = _get_pari()
    return _convert_to_python(pari.eisenstein(k, n, precision))


@mcp.tool()
def bnrL1(bnr: Any, s: Any = None, flag: int = 0) -> Any:
    """Compute the first derivative of Artin L-function.

    Args:
        bnr: BNR structure from bnrinit.
        s: Complex parameter (optional).
        flag: Computation flag.

    Returns:
        L'-value.

    Example:
        >>> bnr = bnrinit(nfinit("x^2 + 1"), 1)
    """
    pari = _get_pari()
    if s is None:
        return _convert_to_python(pari.bnrL1(bnr, flag))
    return _convert_to_python(pari.bnrL1(bnr, s, flag))


@mcp.tool()
def bnrrootnumber(bnr: Any, character: Any = None, flag: int = 0) -> Any:
    """Compute the root number of Artin L-function.

    Args:
        bnr: BNR structure.
        character: Dirichlet character (optional).
        flag: Computation flag.

    Returns:
        Root number (±1).

    Example:
        >>> bnr = bnrinit(nfinit("x^2 + 1"), 1)
    """
    pari = _get_pari()
    if character is None:
        return _convert_to_python(pari.bnrrootnumber(bnr, flag))
    return _convert_to_python(pari.bnrrootnumber(bnr, character, flag))


@mcp.tool()
def dirichlet(s: Any, chi: Any, precision: int = 0) -> Any:
    """Compute Dirichlet L-function.

    Args:
        s: Complex parameter.
        chi: Dirichlet character.
        precision: Optional precision.

    Returns:
        L(s, chi).

    Example:
        >>> dirichlet(2, 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.dirichlet(s, chi, precision))


@mcp.tool()
def lfun(s: Any, F: Any = None, r: int = 0) -> Any:
    """Compute general L-function.

    Args:
        s: Complex parameter.
        F: L-function data (optional).
        r: Derivative order.

    Returns:
        L(s) or its r-th derivative.

    Example:
        >>> lfun(2, 1)
    """
    pari = _get_pari()
    return _convert_to_python(pari.lfun(s, F, r))


@mcp.tool()
def lfuntheta(t: Any, F: Any, precision: int = 0) -> Any:
    """Compute theta function of L-function.

    Args:
        t: Real parameter.
        F: L-function data.
        precision: Optional precision.

    Returns:
        Theta value.

    Example:
    """
    pari = _get_pari()
    return _convert_to_python(pari.lfuntheta(t, F, precision))
