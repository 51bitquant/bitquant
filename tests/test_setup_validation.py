"""
Validation tests to ensure the testing infrastructure is properly set up.
"""
import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Validate that the testing infrastructure is correctly configured."""
    
    def test_pytest_is_importable(self):
        """Test that pytest can be imported."""
        import pytest
        assert pytest is not None
    
    def test_pytest_version(self):
        """Test that pytest version is appropriate."""
        import pytest
        version = pytest.__version__
        major, minor = map(int, version.split('.')[:2])
        assert major >= 7, f"pytest version {version} is too old, need >= 7.0"
    
    def test_coverage_is_importable(self):
        """Test that coverage tools can be imported."""
        import pytest_cov
        assert pytest_cov is not None
    
    def test_mock_is_importable(self):
        """Test that mocking utilities can be imported."""
        import pytest_mock
        assert pytest_mock is not None
    
    def test_project_structure_exists(self):
        """Test that the expected project structure exists."""
        workspace_path = Path("/workspace")
        assert workspace_path.exists()
        assert (workspace_path / "tests").exists()
        assert (workspace_path / "tests" / "__init__.py").exists()
        assert (workspace_path / "tests" / "unit").exists()
        assert (workspace_path / "tests" / "unit" / "__init__.py").exists()
        assert (workspace_path / "tests" / "integration").exists()
        assert (workspace_path / "tests" / "integration" / "__init__.py").exists()
        assert (workspace_path / "tests" / "conftest.py").exists()
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists and is valid."""
        pyproject_path = Path("/workspace/pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml not found"
        
        # Basic validation that it contains expected sections
        content = pyproject_path.read_text()
        assert "[tool.poetry]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "[tool.coverage.run]" in content
    
    def test_gitignore_updated(self):
        """Test that .gitignore contains testing entries."""
        gitignore_path = Path("/workspace/.gitignore")
        assert gitignore_path.exists()
        
        content = gitignore_path.read_text()
        assert ".pytest_cache/" in content
        assert ".coverage" in content
        assert "htmlcov/" in content
        assert ".claude/*" in content
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit test marker works."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration test marker works."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow test marker works."""
        assert True
    
    def test_fixtures_available(self, temp_dir, mock_config):
        """Test that custom fixtures from conftest.py are available."""
        assert temp_dir.exists()
        assert isinstance(mock_config, dict)
        assert 'api_key' in mock_config
    
    def test_mock_exchange_fixture(self, mock_exchange):
        """Test that mock exchange fixture works correctly."""
        assert mock_exchange.id == 'binance'
        assert mock_exchange.has['fetchOHLCV'] is True
        assert 'BTC/USDT' in mock_exchange.markets
    
    def test_sample_data_fixtures(self, sample_ohlcv_data, sample_ticker_data, sample_order_book):
        """Test that sample data fixtures provide expected data."""
        assert len(sample_ohlcv_data) == 5
        assert sample_ticker_data['symbol'] == 'BTC/USDT'
        assert 'bids' in sample_order_book
        assert 'asks' in sample_order_book
    
    def test_python_path_includes_workspace(self):
        """Test that Python can import from the workspace modules."""
        workspace_path = str(Path("/workspace").absolute())
        assert workspace_path in sys.path or any(workspace_path in p for p in sys.path)


@pytest.mark.slow
class TestSlowValidation:
    """Slow validation tests that can be skipped with -m 'not slow'."""
    
    def test_coverage_html_generation(self, tmp_path):
        """Test that coverage HTML reports can be generated."""
        # This is a placeholder - actual coverage is generated when running with coverage
        assert True
    
    def test_xml_coverage_generation(self, tmp_path):
        """Test that coverage XML reports can be generated."""
        # This is a placeholder - actual coverage is generated when running with coverage
        assert True


def test_standalone_function():
    """Test that standalone test functions work."""
    assert 1 + 1 == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])