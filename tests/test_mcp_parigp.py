"""Tests for mcp_parigp."""



class TestEvalExpression:
    """Tests for eval_expression."""

    def test_eval_simple_expression(self):
        """Test evaluating a simple expression."""
        from mcp_parigp import eval_expression

        result = eval_expression("1 + 1")
        assert result == 2

    def test_eval_factor(self):
        """Test evaluating factor expression."""
        from mcp_parigp import eval_expression

        result = eval_expression("factor(100)")
        assert result == [[2, 2], [5, 2]]


class TestGetPariVersion:
    """Tests for get_pari_version."""

    def test_get_pari_version(self):
        """Test getting PARI version."""
        from mcp_parigp import get_pari_version

        version = get_pari_version()
        assert isinstance(version, str)
        assert "PARI" in version


class TestPrecision:
    """Tests for precision functions."""

    def test_set_real_precision(self):
        """Test setting real precision."""
        from mcp_parigp import get_real_precision, set_real_precision

        old = set_real_precision(50)
        assert old == 15  # default
        current = get_real_precision()
        assert current == 50
        set_real_precision(15)  # reset


class TestStackManagement:
    """Tests for stack management functions."""

    def test_stacksize(self):
        """Test getting stack size."""
        from mcp_parigp import stacksize

        size = stacksize()
        assert isinstance(size, int)
        assert size > 0

    def test_stacksizemax(self):
        """Test getting max stack size."""
        from mcp_parigp import stacksizemax

        max_size = stacksizemax()
        assert isinstance(max_size, int)
        assert max_size > 0


class TestRandom:
    """Tests for random functions."""

    def test_setrand_getrand(self):
        """Test setting and getting random seed."""
        from mcp_parigp import getrand, setrand

        setrand(42)
        seed = getrand()
        assert isinstance(seed, (list, int))


class TestNumberTheoryBasic:
    """Tests for basic number theory functions."""

    def test_factor(self):
        """Test integer factorization."""
        from mcp_parigp import factor

        result = factor(100)
        assert result == [[2, 2], [5, 2]]

    def test_isprime(self):
        """Test primality testing."""
        from mcp_parigp import isprime

        assert isprime(29) is True
        assert isprime(28) is False

    def test_gcd(self):
        """Test GCD computation."""
        from mcp_parigp import gcd

        assert gcd(48, 18) == 6

    def test_lcm(self):
        """Test LCM computation."""
        from mcp_parigp import lcm

        assert lcm(4, 6) == 12

    def test_phi(self):
        """Test Euler's totient function."""
        from mcp_parigp import phi

        assert phi(10) == 4
        assert phi(1) == 1

    def test_sigma(self):
        """Test divisor sum function."""
        from mcp_parigp import sigma

        assert sigma(10) == 18

    def test_moebius(self):
        """Test Möbius function."""
        from mcp_parigp import moebius

        assert moebius(10) == 1
        assert moebius(12) == 0


class TestPrimes:
    """Tests for prime functions."""

    def test_primes_first_n(self):
        """Test getting first n primes."""
        from mcp_parigp import primes

        result = primes(5)
        assert result == [2, 3, 5, 7, 11]

    def test_prime_n(self):
        """Test getting nth prime."""
        from mcp_parigp import prime

        assert prime(10) == 29

    def test_nextprime(self):
        """Test nextprime function."""
        from mcp_parigp import nextprime

        result = nextprime(10)
        assert result == 11


class TestCombinatorics:
    """Tests for combinatorial functions."""

    def test_factorial(self):
        """Test factorial."""
        from mcp_parigp import factorial

        assert factorial(5) == 120
        assert factorial(0) == 1

    def test_binomial(self):
        """Test binomial coefficient."""
        from mcp_parigp import binomial

        assert binomial(10, 3) == 120

    def test_fibonacci(self):
        """Test Fibonacci numbers."""
        from mcp_parigp import fibonacci

        assert fibonacci(10) == 55

    def test_lucas(self):
        """Test Lucas numbers."""
        from mcp_parigp import lucas

        assert lucas(10) == 123


class TestPolynomials:
    """Tests for polynomial functions."""

    def test_polcyclo(self):
        """Test cyclotomic polynomial."""
        from mcp_parigp import polcyclo

        result = polcyclo(5)
        assert "x^4" in str(result) and "x^3" in str(result)

    def test_polroots(self):
        """Test polynomial roots."""
        from mcp_parigp import polroots

        result = polroots("x^2 + 1")
        assert len(result) == 2


class TestNumberFields:
    """Tests for number field functions."""

    def test_nfinit(self):
        """Test number field initialization."""
        from mcp_parigp import nfinit

        result = nfinit("x^2 + 1")
        assert result is not None


class TestEllipticCurves:
    """Tests for elliptic curve functions."""

    def test_ellinit(self):
        """Test elliptic curve initialization."""
        from mcp_parigp import ellinit

        # Use vector format for short Weierstrass form: [a1, a2, a3, a4, a6]
        # For y^2 = x^3 - x, we have: a1=0, a2=0, a3=0, a4=-1, a6=1
        result = ellinit("[0, 0, 0, -1, 1]")
        assert result is not None


class TestMatrices:
    """Tests for matrix functions."""

    def test_matid(self):
        """Test identity matrix."""
        from mcp_parigp import matid

        result = matid(3)
        assert result is not None

    def test_matdet(self):
        """Test matrix determinant."""
        from mcp_parigp import matdet

        result = matdet("[1, 2; 3, 4]")
        assert result == -2


class TestConversions:
    """Tests for conversion functions."""

    def test_Mod(self):
        """Test Mod function."""
        from mcp_parigp import Mod, lift

        m = Mod(2, 17)
        assert lift(m) == 2

    def test_Vec(self):
        """Test Vec conversion."""
        from mcp_parigp import Vec

        result = Vec("[1, 2, 3]")
        assert result == [1, 2, 3]


class TestConstants:
    """Tests for mathematical constants."""

    def test_pi(self):
        """Test pi constant via eval."""
        from mcp_parigp import eval_expression

        result = eval_expression("Pi")
        assert abs(result - 3.14159) < 0.1


class TestQuadraticForms:
    """Tests for quadratic forms."""

    def test_qfbclassno(self):
        """Test class number."""
        from mcp_parigp import qfbclassno

        result = qfbclassno(-3)
        assert result == 1


class TestHilbert:
    """Tests for Hilbert symbol."""

    def test_hilbert(self):
        """Test Hilbert symbol."""
        from mcp_parigp import hilbert

        result = hilbert(-1, 5)
        assert result in [-1, 1]
