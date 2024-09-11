# Homework #5

## Task Overview

Create a console tool that retrieves **EUR** and **USD** exchange rates from the **National Bank of Poland's (NBP)** public API for the last few days. Limit the tool to display exchange rates for a maximum of **10 days**. Use **Aiohttp** to send requests to the API. Follow the **SOLID** principles and handle network request errors correctly.

### Example:

```bash
py .\main.py 2
```

### Expected Output:

```json
[
  {
    '03.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  },
  {
    '02.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  }
]
```

### Requirements:
1. Fetch **EUR** and **USD** exchange rates using the [NBP public API](https://api.nbp.pl/api/exchangerates/tables/a/2023-10-25?format=json).
2. Display exchange rates for up to **10 days**.
3. Use **Aiohttp** for sending HTTP requests.
4. Handle network errors properly.
5. Follow **SOLID** principles.