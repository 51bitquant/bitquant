"""
Shared pytest fixtures and configuration for all tests.
"""
import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary."""
    return {
        'api_key': 'test_api_key',
        'api_secret': 'test_api_secret',
        'exchange': 'binance',
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'initial_capital': 10000,
        'risk_per_trade': 0.02,
        'max_positions': 3,
        'commission': 0.001,
        'slippage': 0.0005,
    }


@pytest.fixture
def mock_exchange():
    """Create a mock exchange object."""
    exchange = MagicMock()
    exchange.id = 'binance'
    exchange.has = {
        'fetchOHLCV': True,
        'fetchOrderBook': True,
        'fetchTicker': True,
        'fetchTrades': True,
        'fetchBalance': True,
        'createOrder': True,
        'cancelOrder': True,
        'fetchOrder': True,
        'fetchOrders': True,
        'fetchOpenOrders': True,
        'fetchClosedOrders': True,
    }
    exchange.markets = {
        'BTC/USDT': {
            'id': 'BTCUSDT',
            'symbol': 'BTC/USDT',
            'base': 'BTC',
            'quote': 'USDT',
            'active': True,
            'precision': {'amount': 8, 'price': 2},
            'limits': {
                'amount': {'min': 0.00001, 'max': 9000},
                'price': {'min': 0.01, 'max': 1000000},
                'cost': {'min': 10, 'max': None},
            },
        }
    }
    return exchange


@pytest.fixture
def sample_ohlcv_data():
    """Provide sample OHLCV data for testing."""
    return [
        [1609459200000, 29000.0, 29500.0, 28900.0, 29300.0, 1234.5],  # timestamp, open, high, low, close, volume
        [1609462800000, 29300.0, 29800.0, 29200.0, 29600.0, 1345.6],
        [1609466400000, 29600.0, 30000.0, 29500.0, 29900.0, 1456.7],
        [1609470000000, 29900.0, 30200.0, 29700.0, 30100.0, 1567.8],
        [1609473600000, 30100.0, 30300.0, 29900.0, 30000.0, 1678.9],
    ]


@pytest.fixture
def sample_ticker_data():
    """Provide sample ticker data for testing."""
    return {
        'symbol': 'BTC/USDT',
        'timestamp': 1609477200000,
        'datetime': '2021-01-01T06:00:00.000Z',
        'high': 30300.0,
        'low': 28900.0,
        'bid': 29999.0,
        'bidVolume': 0.5,
        'ask': 30001.0,
        'askVolume': 0.5,
        'vwap': 29750.0,
        'open': 29000.0,
        'close': 30000.0,
        'last': 30000.0,
        'previousClose': 29000.0,
        'change': 1000.0,
        'percentage': 3.45,
        'average': 29500.0,
        'baseVolume': 6283.5,
        'quoteVolume': 186881250.0,
        'info': {}
    }


@pytest.fixture
def sample_order_book():
    """Provide sample order book data for testing."""
    return {
        'symbol': 'BTC/USDT',
        'bids': [
            [29999.0, 0.5],
            [29998.0, 1.0],
            [29997.0, 1.5],
            [29996.0, 2.0],
            [29995.0, 2.5],
        ],
        'asks': [
            [30001.0, 0.5],
            [30002.0, 1.0],
            [30003.0, 1.5],
            [30004.0, 2.0],
            [30005.0, 2.5],
        ],
        'timestamp': 1609477200000,
        'datetime': '2021-01-01T06:00:00.000Z',
        'nonce': None,
    }


@pytest.fixture
def mock_backtest_data():
    """Provide mock data for backtesting."""
    return {
        'dates': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05'],
        'prices': [29000.0, 29300.0, 29600.0, 29900.0, 30000.0],
        'volumes': [1234.5, 1345.6, 1456.7, 1567.8, 1678.9],
        'signals': [0, 1, 0, -1, 0],  # 0: hold, 1: buy, -1: sell
    }


@pytest.fixture
def mock_api_response():
    """Create a mock API response object."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'status': 'success',
        'data': {
            'balance': 10000.0,
            'positions': [],
            'orders': []
        }
    }
    response.text = '{"status": "success", "data": {"balance": 10000.0, "positions": [], "orders": []}}'
    return response


@pytest.fixture
def mock_websocket():
    """Create a mock websocket connection."""
    ws = MagicMock()
    ws.connected = True
    ws.send = MagicMock()
    ws.recv = MagicMock(return_value='{"type": "ping"}')
    ws.close = MagicMock()
    return ws


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def isolated_filesystem(tmp_path):
    """Create an isolated filesystem for testing file operations."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)


def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "requires_network: mark test as requiring network access"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: mark test as requiring API credentials"
    )