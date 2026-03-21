"""Tests for the rate limiting module."""
import time
import pytest
from api_toolkit.rate_limit import InMemoryRateLimiter, get_rate_limiter


def test_allows_within_limit():
    limiter = InMemoryRateLimiter()
    for _ in range(5):
        assert limiter.is_allowed("key", limit=5, window=60)


def test_blocks_over_limit():
    limiter = InMemoryRateLimiter()
    for _ in range(5):
        limiter.is_allowed("key", limit=5, window=60)
    assert not limiter.is_allowed("key", limit=5, window=60)


def test_resets_after_window():
    limiter = InMemoryRateLimiter()
    for _ in range(3):
        limiter.is_allowed("key", limit=3, window=1)
    assert not limiter.is_allowed("key", limit=3, window=1)
    time.sleep(1.1)
    assert limiter.is_allowed("key", limit=3, window=1)


def test_independent_keys():
    limiter = InMemoryRateLimiter()
    for _ in range(5):
        limiter.is_allowed("a", limit=5, window=60)
    assert not limiter.is_allowed("a", limit=5, window=60)
    assert limiter.is_allowed("b", limit=5, window=60)


def test_factory_returns_in_memory():
    assert isinstance(get_rate_limiter("memory"), InMemoryRateLimiter)
