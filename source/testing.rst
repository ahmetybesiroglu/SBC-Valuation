Testing
=======

The SBC-Valuation project includes a comprehensive test suite to ensure the reliability and correctness of its core functions.

Running Tests
-------------

To run the test suite:

1. Ensure you're in the project's root directory.
2. Activate your virtual environment.
3. Run the following command:

   .. code-block:: bash

      poetry run pytest

Test Coverage
-------------

The test suite covers the following key areas:

1. Volatility Calculation
   
   - Tests the ``calculate_volatility`` function with various inputs.
   - Includes tests for valid data, empty data, and invalid frequencies.

2. Treasury Yield Fetching
   
   - Tests the ``fetch_treasury_yield`` function.
   - Includes tests for valid dates and fallback scenarios.

3. Black-Scholes Model
   
   - Tests the ``black_scholes`` function with various inputs.
   - Includes edge cases like zero volatility and when stock price equals strike price.

4. Airtable Integration
   
   - Tests the integration with the Airtable API.
   - Includes tests for fetching records, updating records, and handling rate limits.

5. Environment Variable Handling
   
   - Tests the proper loading and usage of environment variables.

Adding New Tests
----------------

When adding new features or modifying existing ones, please ensure to update or add corresponding tests in the ``tests/test_run.py`` file.

Continuous Integration
----------------------

This project uses GitHub Actions for continuous integration. The CI pipeline runs the test suite on every push to the main branch and on all pull requests. Refer to ``.github/workflows/python.yml`` for the CI configuration.
