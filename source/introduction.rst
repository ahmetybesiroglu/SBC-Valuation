Introduction
============

The SBC-Valuation project is an automated tool for valuing stock-based compensation (SBC) options using the Black-Scholes model. This project streamlines the process of option valuation by integrating with Airtable for data management, fetching historical stock prices from Yahoo Finance for volatility calculations, and retrieving treasury yields to determine risk-free rates.

Key Features
------------

- Automated calculation of option values using the Black-Scholes model
- Integration with Airtable for data input and storage
- Volatility calculation based on historical stock prices
- Risk-free rate determination using treasury yields
- Flexible recalculation mechanism

How It Works
------------

1. Users input data into the Tranches table in Airtable.
2. Each valuation is associated with a tranche, automatically populating grant date, vest date, and expiry date.
3. The script calculates volatilities based on historical stock prices and the selected frequency (daily, weekly, or monthly).
4. Treasury yields are fetched and extrapolated to match the expected term.
5. The Black-Scholes formula is used to calculate option values.
6. Calculated data (volatilities, risk-free rates, and option values) are stored back in Airtable.
7. The script recalculates values for any entries with an empty ``option_value``.

This automated process ensures accurate and up-to-date valuations for SBC options, streamlining financial reporting and decision-making processes.
