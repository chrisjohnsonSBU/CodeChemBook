import pytest
from codechembook.symbols.chem import Angstrom, wavenumber, degree, sbond, dbond, tbond

def test_basic_symbols():
    """Verify that common chemical string symbols are correct."""
    assert Angstrom == '\u212B'
    assert wavenumber == 'cm\u207B\u00B9'
    assert degree == '\u00B0'

def test_bond_symbols():
    """Verify that bond symbols have the expected representations."""
    assert sbond == '\uFF0D'
    assert dbond == '\uFF1D'
    assert tbond == '\u200A\u2261\u200A'
