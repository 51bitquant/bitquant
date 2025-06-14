# Testing Infrastructure

This directory contains the testing infrastructure for the crypto-trading-toolkit project.

## Setup

The project uses Poetry for dependency management and pytest for testing. All testing dependencies are already configured in `pyproject.toml`.

## Running Tests

```bash
# Run all tests
poetry run test
# or
poetry run tests

# Run tests with coverage
poetry run pytest --cov=backtest --cov=binance_api --cov=bybit --cov=ccxt_study --cov=crawl_exchanges_datas --cov=huobi_api --cov=technical_indicators --cov=weixinbot --cov-report=html --cov-report=xml

# Run only unit tests
poetry run pytest -m unit

# Run only integration tests
poetry run pytest -m integration

# Skip slow tests
poetry run pytest -m "not slow"

# Run tests in verbose mode
poetry run pytest -v

# Run a specific test file
poetry run pytest tests/test_setup_validation.py

# Run tests with specific pattern
poetry run pytest -k "test_exchange"
```

## Test Markers

The following markers are available:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (may require external resources)
- `@pytest.mark.slow` - Slow tests
- `@pytest.mark.requires_network` - Tests requiring network access
- `@pytest.mark.requires_api_key` - Tests requiring API credentials

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures and pytest configuration
├── README.md            # This file
├── unit/                # Unit tests
│   └── __init__.py
├── integration/         # Integration tests
│   └── __init__.py
└── test_setup_validation.py  # Validation tests for the testing infrastructure
```

## Available Fixtures

The `conftest.py` file provides numerous fixtures for testing:

- `temp_dir` - Temporary directory for test files
- `mock_config` - Mock configuration dictionary
- `mock_exchange` - Mock exchange object
- `sample_ohlcv_data` - Sample OHLCV data
- `sample_ticker_data` - Sample ticker data
- `sample_order_book` - Sample order book data
- `mock_backtest_data` - Mock data for backtesting
- `mock_api_response` - Mock API response
- `mock_websocket` - Mock websocket connection
- `isolated_filesystem` - Isolated filesystem for file operations

## Coverage Reports

When running with coverage, reports are generated in:
- Terminal output (with missing lines)
- HTML report in `htmlcov/` directory
- XML report as `coverage.xml`

## Writing Tests

1. Place unit tests in `tests/unit/`
2. Place integration tests in `tests/integration/`
3. Use appropriate markers for test categorization
4. Follow the naming convention: `test_*.py` or `*_test.py`
5. Use fixtures from `conftest.py` to avoid code duplication

Example test file:

```python
import pytest
from unittest.mock import Mock

@pytest.mark.unit
def test_example_function(mock_config):
    # Your test implementation
    assert mock_config['api_key'] == 'test_api_key'

@pytest.mark.integration
@pytest.mark.requires_network
def test_api_connection(mock_exchange):
    # Test requiring network access
    assert mock_exchange.id == 'binance'
```