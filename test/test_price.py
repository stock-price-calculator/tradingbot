import pytest
from price.calculator import calculateEPS

# @pytest.fixture()
def test_eps():
    result = calculateEPS("005930")
    print(result)
    assert result == []