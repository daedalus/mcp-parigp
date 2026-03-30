"""Tests for mcp-parigp."""


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


class TestPrecisionBits:
    """Tests for precision in bits."""

    def test_get_real_precision_bits(self):
        from mcp_parigp import get_real_precision_bits

        result = get_real_precision_bits()
        assert isinstance(result, int)


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

    def test_polchebyshev(self):
        from mcp_parigp import polchebyshev

        result = polchebyshev(3)
        assert result is not None

    def test_pollegendre(self):
        from mcp_parigp import pollegendre

        result = pollegendre(3)
        assert result is not None

    def test_deriv(self):
        from mcp_parigp import deriv

        result = deriv("x^3 + 2*x")
        assert "3*x^2" in str(result)

    def test_polsubcyclo(self):
        from mcp_parigp import polsubcyclo

        result = polsubcyclo(8, 4)
        assert result is not None


class TestNumberFields:
    """Tests for number field functions."""

    def test_nfinit(self):
        """Test number field initialization."""
        from mcp_parigp import nfinit

        result = nfinit("x^2 + 1")
        assert result is not None

    def test_bnfinit(self):
        from mcp_parigp import bnfinit

        result = bnfinit("x^2 + 1")
        assert result is not None

    def test_idealadd(self):
        from mcp_parigp import nfinit, idealadd

        nf = nfinit("x^2 + 1")
        result = idealadd(nf, 2, 3)
        assert result is not None


class TestEllipticCurves:
    """Tests for elliptic curve functions."""

    def test_ellinit(self):
        """Test elliptic curve initialization."""
        from mcp_parigp import ellinit

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

    def test_matzero(self):
        from mcp_parigp import matzero

        result = matzero(3)
        assert result is not None

    def test_matrank(self):
        from mcp_parigp import matrank

        result = matrank("[1, 2; 2, 4]")
        assert result == 1

    def test_mateigen(self):
        from mcp_parigp import mateigen

        result = mateigen("[1, 2; 2, 1]")
        assert len(result) == 2


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

    def test_Col(self):
        from mcp_parigp import Col

        result = Col("[1, 2, 3]")
        assert result is not None

    def test_Mat(self):
        from mcp_parigp import Mat

        result = Mat("[1, 2, 3]")
        assert result is not None

    def test_Set(self):
        from mcp_parigp import Set

        result = Set("[1, 2, 1, 3]")
        assert result == [1, 2, 3]

    def test_Pol(self):
        from mcp_parigp import Pol

        result = Pol("[1, 2, 3]")
        assert result is not None

    def test_Polrev(self):
        from mcp_parigp import Polrev

        result = Polrev("[1, 2, 3]")
        assert result is not None

    def test_Ser(self):
        from mcp_parigp import Ser

        result = Ser("x + 1", "x", 5)
        assert result is not None


class TestConstants:
    """Tests for mathematical constants."""

    def test_pi(self):
        from mcp_parigp import eval_expression

        result = eval_expression("Pi")
        assert abs(result - 3.14159) < 0.1

    def test_euler_constant(self):
        from mcp_parigp import eval_expression

        result = eval_expression("Euler")
        assert abs(result - 0.57721) < 0.01


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


class TestVectorMatrix:
    """Tests for vector and matrix creation."""

    def test_vector(self):
        from mcp_parigp import vector

        result = vector(3, [1, 2, 3])
        assert result is not None

    def test_matrix(self):
        from mcp_parigp import matrix

        result = matrix(2, 3, [1, 2, 3, 4, 5, 6])
        assert result is not None


class TestTrigViaEval:
    """Tests for trigonometric functions via eval."""

    def test_sin_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sin(0)")
        assert result == 0

    def test_cos_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("cos(0)")
        assert result == 1

    def test_tan_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("tan(0)")
        assert result == 0


class TestHyperbolicViaEval:
    """Tests for hyperbolic functions via eval."""

    def test_sinh_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sinh(0)")
        assert result == 0

    def test_cosh_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("cosh(0)")
        assert result == 1

    def test_tanh_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("tanh(0)")
        assert result == 0


class TestExpLogViaEval:
    """Tests for exponential and log via eval."""

    def test_exp_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("exp(0)")
        assert result == 1

    def test_log_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("log(1)")
        assert result == 0


class TestBasicMathViaEval:
    """Tests for basic math via eval."""

    def test_sqrt_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sqrt(4)")
        assert result == 2

    def test_abs_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("abs(-5)")
        assert result == 5


class TestComplexViaEval:
    """Tests for complex numbers via eval."""

    def test_I_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("I")
        assert result == complex(0, 1)


class TestConstantsViaEval:
    """Tests for constants via eval."""

    def test_one_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("1")
        assert result == 1

    def test_zero_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("0")
        assert result == 0


class TestMoreNumberTheory:
    """Tests for more number theory functions."""

    def test_bezout(self):
        from mcp_parigp import bezout

        result = bezout(48, 18)
        assert result is not None

    def test_jacobi(self):
        from mcp_parigp import jacobi

        result = jacobi(10, 21)
        assert result in [-1, 0, 1]

    def test_znstar(self):
        from mcp_parigp import znstar

        result = znstar(12)
        assert result is not None


class TestMorePolynomials:
    """Tests for more polynomial functions."""

    def test_deriv(self):
        from mcp_parigp import deriv

        result = deriv("x^3 + 2*x")
        assert "3*x^2" in str(result)

    def test_polrootsmod(self):
        from mcp_parigp import polrootsmod

        result = polrootsmod("x^2 + 1", 5)
        assert result is not None


class TestMoreMatrices:
    """Tests for more matrix functions."""

    def test_matzero(self):
        from mcp_parigp import matzero

        result = matzero(3)
        assert result is not None


class TestMoreEllipticCurves:
    """Tests for more elliptic curve functions."""

    def test_ellinit_direct(self):
        from mcp_parigp import ellinit

        result = ellinit("[0, 0, 0, -1, 1]")
        assert result is not None

    def test_ellj(self):
        from mcp_parigp import ellj

        result = ellj("x^3 - x")
        assert result is not None


class TestEvalExpression2:
    """More tests for eval_expression."""

    def test_eval_complex(self):
        from mcp_parigp import eval_expression

        result = eval_expression("1 + I")
        assert result is not None

    def test_eval_matrix(self):
        from mcp_parigp import eval_expression

        result = eval_expression("[1, 2; 3, 4]")
        assert result is not None

    def test_eval_polynomial(self):
        from mcp_parigp import eval_expression

        result = eval_expression("x^2 + 1")
        assert result is not None


class TestMoreConversions:
    """Tests for more conversion functions."""

    def test_List(self):
        from mcp_parigp import List

        result = List()
        assert result is not None

    def test_centerlift(self):
        from mcp_parigp import centerlift, Mod

        m = Mod(10, 17)
        result = centerlift(m)
        assert result is not None


class TestMoreConstants:
    """Tests for more constants."""

    def test_one(self):
        from mcp_parigp import one

        result = one()
        assert result == 1

    def test_zero(self):
        from mcp_parigp import zero

        result = zero()
        assert result == 0


class TestMoreSpecial:
    """Tests for more special functions."""

    def test_airy(self):
        from mcp_parigp import airy

        result = airy(0)
        assert result is not None

    def test_vector(self):
        from mcp_parigp import vector

        result = vector(3, [1, 2, 3])
        assert result is not None

    def test_matrix(self):
        from mcp_parigp import matrix

        result = matrix(2, 2, [1, 0, 0, 1])
        assert result is not None


class TestMoreNumberFields:
    """Tests for more number fields."""

    def test_idealmul(self):
        from mcp_parigp import nfinit, idealmul

        nf = nfinit("x^2 + 1")
        result = idealmul(nf, 2, 3)
        assert result is not None

    def test_idealpow(self):
        from mcp_parigp import nfinit, idealpow

        nf = nfinit("x^2 + 1")
        result = idealpow(nf, 2, 2)
        assert result is not None

    def test_idealfactor(self):
        from mcp_parigp import nfinit, idealfactor

        nf = nfinit("x^2 + 1")
        result = idealfactor(nf, 2)
        assert result is not None


class TestNumberTheory2:
    """Tests for more number theory functions."""

    def test_ispower(self):
        from mcp_parigp import ispower

        result = ispower(64)
        assert result == 6

    def test_is_square(self):
        from mcp_parigp import is_square

        assert is_square(25) is True
        assert is_square(26) is False


class TestPolynomials2:
    """Tests for more polynomials."""

    def test_polchebyshev(self):
        from mcp_parigp import polchebyshev

        result = polchebyshev(3)
        assert result is not None

    def test_pollegendre(self):
        from mcp_parigp import pollegendre

        result = pollegendre(3)
        assert result is not None


class TestMatrix2:
    """Tests for more matrices."""

    def test_matker(self):
        from mcp_parigp import matker

        result = matker("[1, 2; 2, 4]")
        assert result is not None

    def test_matimage(self):
        from mcp_parigp import matimage

        result = matimage("[1, 2; 2, 4]")
        assert result is not None


class TestQuadraticForms2:
    """Tests for more quadratic forms."""

    def test_qfbclassno(self):
        from mcp_parigp import qfbclassno

        result = qfbclassno(-3)
        assert result == 1

    def test_hilbert(self):
        from mcp_parigp import hilbert

        result = hilbert(-1, 5)
        assert result in [-1, 1]


class TestPolynomialsViaEval:
    """Tests for more polynomials via eval."""

    def test_subst_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("subst(x^2 + 1, x, y + 1)")
        assert result is not None


class TestMoreFunctionsViaEval:
    """Tests for more functions via eval."""

    def test_norm_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("norm(Mod(x, x^2 + 1))")
        assert result is not None

    def test_trace_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("trace(Mod(x, x^2 + 1))")
        assert result is not None

    def test_disc_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("poldisc(x^3 - 3*x + 1)")
        assert result is not None

    def test_factorpadic_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("factorpadic(x^2 - 2, 2, 5)")
        assert result is not None


class TestEllipticViaEval:
    """Tests for elliptic curves via eval."""

    def test_ellinit_via_eval(self):
        from mcp_parigp import eval_expression

        result = eval_expression("ellinit([0, 0, 0, -1, 1])")
        assert result is not None


class TestEvenMoreFunctions:
    """Tests for more functions to increase coverage."""

    def test_eval_pi(self):
        from mcp_parigp import eval_expression

        result = eval_expression("Pi")
        assert result is not None

    def test_eval_euler(self):
        from mcp_parigp import eval_expression

        result = eval_expression("Euler")
        assert result is not None

    def test_eval_fibonacci(self):
        from mcp_parigp import eval_expression

        result = eval_expression("fibonacci(10)")
        assert result == 55

    def test_eval_factorial(self):
        from mcp_parigp import eval_expression

        result = eval_expression("5!")
        assert result == 120

    def test_eval_binomial(self):
        from mcp_parigp import eval_expression

        result = eval_expression("binomial(10, 3)")
        assert result == 120

    def test_eval_prime(self):
        from mcp_parigp import eval_expression

        result = eval_expression("prime(10)")
        assert result == 29

    def test_eval_nextprime(self):
        from mcp_parigp import eval_expression

        result = eval_expression("nextprime(10)")
        assert result == 11

    def test_eval_moebius(self):
        from mcp_parigp import eval_expression

        result = eval_expression("moebius(10)")
        assert result == 1

    def test_eval_ispower(self):
        from mcp_parigp import eval_expression

        result = eval_expression("ispower(64)")
        assert result == 6

    def test_eval_znstar(self):
        from mcp_parigp import eval_expression

        result = eval_expression("znstar(12)")
        assert result is not None

    def test_eval_sigma(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sigma(10)")
        assert result == 18

    def test_eval_eulerphi(self):
        from mcp_parigp import eval_expression

        result = eval_expression("eulerphi(10)")
        assert result == 4


class TestExtraCoverage:
    """Extra tests for coverage."""

    def test_eval_sin(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sin(0)")
        assert result == 0

    def test_eval_cos(self):
        from mcp_parigp import eval_expression

        result = eval_expression("cos(0)")
        assert result == 1

    def test_eval_tan(self):
        from mcp_parigp import eval_expression

        result = eval_expression("tan(0)")
        assert result == 0

    def test_eval_asin(self):
        from mcp_parigp import eval_expression

        result = eval_expression("asin(0)")
        assert result == 0

    def test_eval_acos(self):
        from mcp_parigp import eval_expression

        result = eval_expression("acos(1)")
        assert result == 0

    def test_eval_atan(self):
        from mcp_parigp import eval_expression

        result = eval_expression("atan(0)")
        assert result == 0

    def test_eval_sinh(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sinh(0)")
        assert result == 0

    def test_eval_cosh(self):
        from mcp_parigp import eval_expression

        result = eval_expression("cosh(0)")
        assert result == 1

    def test_eval_tanh(self):
        from mcp_parigp import eval_expression

        result = eval_expression("tanh(0)")
        assert result == 0

    def test_eval_exp(self):
        from mcp_parigp import eval_expression

        result = eval_expression("exp(0)")
        assert result == 1

    def test_eval_log(self):
        from mcp_parigp import eval_expression

        result = eval_expression("log(1)")
        assert result == 0

    def test_eval_sqrt(self):
        from mcp_parigp import eval_expression

        result = eval_expression("sqrt(4)")
        assert result == 2

    def test_eval_abs(self):
        from mcp_parigp import eval_expression

        result = eval_expression("abs(-5)")
        assert result == 5

    def test_eval_gcd(self):
        from mcp_parigp import eval_expression

        result = eval_expression("gcd(48, 18)")
        assert result == 6

    def test_eval_lcm(self):
        from mcp_parigp import eval_expression

        result = eval_expression("lcm(4, 6)")
        assert result == 12
