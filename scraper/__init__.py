"""
Python Web Scraper Package

A web scraper for extracting product information from e-commerce sites.
"""

from scraper.main import (
    int_extractor,
    get_amazon_results,
    get_snapdeal_results,
    get_results
)

__version__ = "1.0.0"
__all__ = [
    "int_extractor",
    "get_amazon_results",
    "get_snapdeal_results",
    "get_results"
]
