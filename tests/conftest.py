"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture(autouse=True)
def reset_pari_precision():
    """Reset PARI precision after each test."""
    yield
    try:
        from mcp_parigp import _get_pari

        pari = _get_pari()
        pari.set_real_precision_bits(53)
    except Exception:
        pass
