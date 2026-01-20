"""Unit tests for int_extractor function."""

from scraper.main import int_extractor


def test_int_extractor_basic():
    """Test basic integer extraction from price strings."""
    assert int_extractor("Rs. 999") == 999
    assert int_extractor("Rs. 1,234") == 1234
    assert int_extractor("$99.99") == 99
    assert int_extractor("100") == 100


def test_int_extractor_with_decimal():
    """Test extraction stops at decimal point."""
    assert int_extractor("Rs. 999.50") == 999
    assert int_extractor("$99.99") == 99
    assert int_extractor("1234.56") == 1234


def test_int_extractor_with_commas():
    """Test extraction with comma-separated numbers."""
    assert int_extractor("Rs. 1,234") == 1234
    assert int_extractor("10,000") == 10000


def test_int_extractor_empty_string():
    """Test extraction from empty string."""
    assert int_extractor("") == 0


def test_int_extractor_no_digits():
    """Test extraction from string with no digits."""
    assert int_extractor("No price") == 0


def test_int_extractor_leading_text():
    """Test extraction with leading non-digit characters."""
    assert int_extractor("Price: Rs. 999") == 999
    assert int_extractor("Cost $50") == 50


def test_int_extractor_trailing_text():
    """Test extraction with trailing text."""
    assert int_extractor("999 only") == 999
    assert int_extractor("Rs. 500 available") == 500
