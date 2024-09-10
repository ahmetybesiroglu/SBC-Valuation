
# SBC Options Valuation

![Build Status](https://github.com/ahmetybesiroglu/SBC-Valuation/actions/workflows/python.yml/badge.svg)
![Coverage](https://codecov.io/gh/ahmetybesiroglu/SBC-Valuation/branch/main/graph/badge.svg)
![GitHub Pages](https://img.shields.io/website?down_color=red&down_message=offline&up_color=blue&up_message=online&url=https%3A%2F%2Fyourusername.github.io%2FSBC-Valuation)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

This project automates the valuation of stock-based compensation (SBC) options using the Black-Scholes model. It integrates with Airtable for data management, fetching historical stock prices from Yahoo Finance for volatility calculations, and treasury yields for determining risk-free rates. The entire process is streamlined within Airtable, with calculated values being stored back for easy reference.

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Setup](#setup)
  - [Virtual Environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Airtable Structure](#airtable-structure)
  - [Tranches Table](#tranches-table)
  - [Valuations Table](#valuations-table)
  - [Volatilities Table](#volatilities-table)
  - [Public Comp Set Table](#public-comp-set-table)
- [Running the Script](#running-the-script)
- [Additional Information](#additional-information)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## How It Works

1. **User Input**: Users input data into the Tranches table in Airtable.
2. **Valuation Association**: Users associate each valuation with a tranche, which automatically populates grant date, vest date, and expiry date.
3. **Volatility Calculation**: The script fetches historical stock prices for public companies and calculates volatilities based on the selected frequency (daily, weekly, or monthly).
4. **Risk-Free Rate**: The script fetches treasury yields and extrapolates them to match the expected term using predefined yield curves.
5. **Black-Scholes Model**: The script calculates the option values using the Black-Scholes formula.
6. **Data Storage**: The calculated volatilities, risk-free rates, and option values are stored back in Airtable.
7. **Recalculation Mechanism**: The script recalculates values for any entries with an empty `option_value`. Delete the `option_value` for an entry to force recalculation.

## Setup

### Virtual Environment

1. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

### Dependencies

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install dependencies:

1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Install project dependencies:
   ```bash
   poetry install
   ```

### Environment Variables

Create a `.env` file in the root directory of your project and add the following environment variables:

```ini
AIRTABLE_API_KEY=your_airtable_api_key
BASE_ID=your_base_id
TRANCHES_TABLE_ID=your_tranches_table_id
OPTION_VALUATIONS_TABLE_ID=your_valuations_table_id
VOLATILITY_DATA_TABLE_ID=your_volatility_data_table_id
PUBLIC_COMP_SET_TABLE_ID=your_public_comp_set_table_id
```

These variables will be used to interact with your Airtable tables.

## Testing

This project includes unit tests to verify the correctness of the main functions and ensure proper integration with external services (like Airtable and Yahoo Finance).

To run the tests:

1. **Run the tests with Poetry**:
   ```bash
   poetry run pytest
   ```

The tests are located in the `tests/` directory and include coverage for:
- Volatility calculation
- Treasury yield fetching
- Black-Scholes option pricing
- Airtable API integration

## Airtable Structure

### Tranches Table

The Tranches table contains the following fields:

- **Tranche ID**: Auto Number
- **Grant Date**: Date (ISO 8601 format)
- **Vesting Date**: Date (ISO 8601 format)
- **Expiry Date**: Date (ISO 8601 format)

### Valuations Table

The Valuations table contains the following fields:

- **Valuation ID**: Auto Number
- **Public Comp Set**: Link to another record (Array of record IDs from the Public Comp Set table)
- **Valuation Date**: Date (ISO 8601 format)
- **Stock Price**: Currency (Positive number)
- **Strike Price**: Currency (Positive number)
- **Volatility Frequency**: Single select (Daily, Weekly, Monthly)
- **Option Value**: Currency (Calculated value)
- **Expected Term**: Formula (Computed based on Vesting Date and Expiry Date)
- **Tranche ID**: Link to another record (Array of record IDs from the Tranches table)
- **Vesting Date**: Lookup (Array of dates from linked Tranches records)
- **Expiry Date**: Lookup (Array of dates from linked Tranches records)
- **Grant Date**: Lookup (Array of dates from linked Tranches records)
- **Average Volatility**: Rollup (AVERAGE(values) from Volatilities)
- **Risk-Free Rate**: Lookup (Array of yields from Treasury Yields)

### Volatilities Table

The Volatilities table contains the following fields:

- **Volatility ID**: Auto Number
- **Valuation ID**: Link to another record (Array of record IDs from the Valuations table)
- **Ticker**: Text
- **Volatility**: Percent

### Public Comp Set Table

The Public Comp Set table contains the following fields:

- **Comp ID**: Auto Number
- **Ticker**: Text

## Running the Script

After setting up your environment and ensuring your Airtable structure matches the described format, run the script using:

```bash
poetry run python sbc_valuation/run.py
```

The script will process all valuation records that have missing option values and update the results directly in Airtable.

## Additional Information

- The script iterates over all valuation rows with necessary inputs and an empty `option_value` field, recalculating the option value based on updated inputs.
- To trigger a recalculation, simply delete the `option_value` for a specific record.
- Start by filling out the Tranches table with grant dates, vest dates, and expiry dates. Then, associate each valuation with a tranche, and most inputs will be populated automatically. Be sure to manually input the `valuation_date`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For further questions, please contact [ahmetybesiroglu@gmail.com](mailto:ahmetybesiroglu@gmail.com).
