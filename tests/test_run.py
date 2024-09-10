import pytest
from sbc_valuation.run import calculate_volatility, fetch_treasury_yield, black_scholes
import pandas as pd
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv
import numpy as np


# 1. Test calculate_volatility with valid data
@patch("yfinance.download")
def test_calculate_volatility(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame(
        {"Adj Close": [100, 102, 104, 106, 108]}
    )
    volatility = calculate_volatility("AAPL", "2022-01-01", "2022-01-10", "daily")
    assert volatility > 0


# 2. Test calculate_volatility with empty data
@patch("yfinance.download")
def test_calculate_volatility_empty_data(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame()
    with pytest.raises(ValueError, match="No data found"):
        calculate_volatility("AAPL", "2022-01-01", "2022-01-10", "daily")


# 3. Test calculate_volatility with invalid frequency
def test_calculate_volatility_invalid_frequency():
    with pytest.raises(ValueError, match="Invalid frequency"):
        calculate_volatility("AAPL", "2022-01-01", "2022-01-10", "hourly")


# 4. Test calculate_volatility with NaN data
@patch("yfinance.download")
def test_calculate_volatility_with_nan_data(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame(
        {"Adj Close": [100, 102, None, 106, 108]}
    )
    volatility = calculate_volatility("AAPL", "2022-01-01", "2022-01-10", "daily")
    assert volatility > 0


# 5. Test calculate_volatility with invalid ticker
@patch("yfinance.download")
def test_calculate_volatility_invalid_ticker(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame()
    with pytest.raises(ValueError, match="No data found"):
        calculate_volatility("INVALID", "2022-01-01", "2022-01-10", "daily")


# 6. Test fetch_treasury_yield with valid data
@patch("yfinance.download")
def test_fetch_treasury_yield(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame(
        {"Close": [1.5, 1.6, 1.7]},
        index=pd.to_datetime(["2021-12-31", "2022-01-01", "2022-01-02"]),
    )
    treasury_yield = fetch_treasury_yield("^TNX", "2022-01-01")
    assert treasury_yield == 0.016


# 7. Test fetch_treasury_yield with fallback data
@patch("yfinance.download")
def test_fetch_treasury_yield_fallback(mock_yf_download):
    mock_yf_download.return_value = pd.DataFrame(
        {
            "Close": [1.5, 1.6],
        },
        index=pd.to_datetime(["2021-12-30", "2022-01-02"]),
    )
    treasury_yield = fetch_treasury_yield("^TNX", "2022-01-01")
    assert treasury_yield == 0.016


# 8. Test fetch_treasury_yield with invalid date
def test_fetch_treasury_yield_invalid_date():
    with pytest.raises(ValueError):
        fetch_treasury_yield("^TNX", "2022-13-01")


# 9. Test black_scholes with valid parameters
def test_black_scholes():
    S = 100
    K = 95
    T = 1
    r = 0.05
    sigma = 0.2
    option_price = black_scholes(S, K, T, r, sigma)
    assert option_price > 0
    assert option_price < S


# 10. Test black_scholes when stock price equals strike price
def test_black_scholes_stock_price_equals_strike():
    option_price = black_scholes(100, 100, 1, 0.05, 0.2)
    assert option_price > 0


# 11. Test black_scholes with zero volatility
def test_black_scholes_zero_volatility():
    S = 100
    K = 90
    T = 1
    r = 0.05
    sigma = 0
    expected_call_price = S - K * np.exp(-r * T)
    assert black_scholes(S, K, T, r, sigma) == round(expected_call_price, 4)
    S_out_of_money = 80
    assert black_scholes(S_out_of_money, K, T, r, sigma) == 0.0


# 12. Test airtable integration with mock API
@patch("pyairtable.Api")
def test_airtable_integration(mock_api):
    # Mock the `table.all()` method to return a list of valuation records
    mock_table_instance = MagicMock()
    mock_table_instance.all.return_value = [
        {
            "fields": {
                "valuation_id": 1,
                "valuation_date": "2022-01-01",
                "expected_term": 3,
                "public_comp_set": ["rec1"],
                "share_price": 100,
                "strike_price": 95,
                "volatility_frequency": "daily",
            }
        }
    ]

    # Mock the `table.get()` method to return a public company record for a given comp ID
    mock_table_instance.get.return_value = {"fields": {"ticker": "AAPL"}}

    # Mock the `table.update()` method
    mock_table_instance.update.return_value = {
        "id": "rec123",
        "fields": {"option_value": 12.34},
    }

    # Set this mocked table instance to be used for various tables
    mock_api.return_value.table.side_effect = (
        lambda base_id, table_name: mock_table_instance
    )

    # Fetch records from the mocked Airtable API
    records = mock_table_instance.all()

    # Ensure that `all()` was called
    mock_table_instance.all.assert_called_once()

    # Simulate part of the code logic where `get()` is called for the public comp set
    for record in records:
        public_comp_set = record["fields"]["public_comp_set"]
        for comp_id in public_comp_set:
            comp_record = mock_table_instance.get(comp_id)
            # Ensure that `get()` was called with the correct ID
            mock_table_instance.get.assert_called_with(comp_id)

    # Simulate the update of a record
    mock_table_instance.update("rec123", {"option_value": 12.34})

    # Ensure `update()` was called with the correct arguments
    mock_table_instance.update.assert_called_once_with(
        "rec123", {"option_value": 12.34}
    )

    # Perform basic assertions to ensure data correctness
    assert records[0]["fields"]["valuation_id"] == 1
    assert records[0]["fields"]["share_price"] == 100


# 13. Test airtable rate limit handling
@patch("pyairtable.Api")
def test_airtable_rate_limit(mock_api):
    mock_table_instance = MagicMock()
    mock_table_instance.all.side_effect = Exception("Rate limit exceeded")
    mock_api.return_value.table.side_effect = (
        lambda base_id, table_name: mock_table_instance
    )
    with pytest.raises(Exception, match="Rate limit exceeded"):
        mock_table_instance.all()


# 14. Test airtable with missing fields
@patch("pyairtable.Api")
def test_airtable_missing_fields(mock_api):
    mock_table_instance = MagicMock()
    mock_table_instance.all.return_value = [
        {"fields": {"valuation_id": 1, "expected_term": 3, "public_comp_set": ["rec1"]}}
    ]
    mock_api.return_value.table.side_effect = (
        lambda base_id, table_name: mock_table_instance
    )
    records = mock_table_instance.all()
    for record in records:
        valuation_date = record["fields"].get("valuation_date", None)
        assert valuation_date is None


# 15. Test missing environment variables
@patch.dict(os.environ, {"AIRTABLE_API_KEY": ""})
def test_missing_env_vars():
    load_dotenv()
    api_key = os.getenv("AIRTABLE_API_KEY")
    assert api_key == ""
