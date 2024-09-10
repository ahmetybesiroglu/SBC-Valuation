API Reference
=============

This section provides detailed information about the Airtable API interactions in the SBC-Valuation project.

Airtable API Initialization
---------------------------

.. code-block:: python

   from pyairtable import Api

   api = Api(AIRTABLE_API_KEY)

The ``Api`` class from the ``pyairtable`` library is used to initialize the connection to Airtable using the API key stored in the ``AIRTABLE_API_KEY`` environment variable.

Table Initialization
--------------------

.. code-block:: python

   tranches_table = api.table(BASE_ID, TRANCHES_TABLE_ID)
   option_valuations_table = api.table(BASE_ID, OPTION_VALUATIONS_TABLE_ID)
   volatility_data_table = api.table(BASE_ID, VOLATILITY_DATA_TABLE_ID)
   public_comp_set_table = api.table(BASE_ID, PUBLIC_COMP_SET_TABLE_ID)

These lines initialize the connections to specific tables in your Airtable base. The ``BASE_ID`` and respective table IDs are stored as environment variables.

Fetching Records
----------------

Fetching All Records
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   valuation_records = option_valuations_table.all()

This retrieves all records from the Option Valuations table.

Fetching a Specific Record
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   comp_record = public_comp_set_table.get(comp_id)

This fetches a specific record from the Public Comp Set table using the ``comp_id``.

Creating Records
----------------

.. code-block:: python

   vol_record = volatility_data_table.create({
       "ticker": [comp_id],
       "volatility": volatility,
   })

This creates a new record in the Volatility Data table with the specified fields.

Updating Records
----------------

.. code-block:: python

   updated_valuation = option_valuations_table.update(
       valuation_record["id"],
       {
           "option_value": option_value,
           "volatility_id": vol_ids,
           "risk_free_rate": risk_free_rate,
       }
   )

This updates an existing record in the Option Valuations table with new values for ``option_value``, ``volatility_id``, and ``risk_free_rate``.

Error Handling
--------------

The code includes try/except blocks to handle potential errors when interacting with the Airtable API:

.. code-block:: python

   try:
       # API interaction code
   except Exception as e:
       print(f"Error: {e}")

This allows for graceful error handling and logging of any issues that occur during API interactions.

Rate Limiting
-------------

The pyairtable library automatically handles rate limiting by the Airtable API. If you encounter rate limit errors, the library will automatically retry the request after a delay.

For more detailed information about these API interactions and their implementation, please refer to the source code in ``sbc_valuation/run.py``.
