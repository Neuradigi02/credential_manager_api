from decimal import Decimal
import httpx
from src.core.load_config import crypto_payment_gateway_config


async def get_token_rate(base_token_symbol: str, quote_token_symbol: str) -> Decimal:
    """ Fetches the exchange rate between two tokens asynchronously. """
    if not base_token_symbol or not quote_token_symbol:
        raise ValueError("Both base_token_symbol and quote_token_symbol must be provided.")

    url = f"{crypto_payment_gateway_config['BaseURL']}get_currencies_rates"
    params = {"from_currency_symbols": base_token_symbol, "to_currency_symbols": quote_token_symbol}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP errors (e.g., 404, 500)
            crypto_data = response.json()

            if "data" in crypto_data and base_token_symbol in crypto_data["data"]:
                rate = crypto_data["data"][base_token_symbol].get(quote_token_symbol)

                if rate is not None:
                    return Decimal(rate)  # Convert to Decimal safely

            raise ValueError(f"Invalid response format or missing data for {base_token_symbol}/{quote_token_symbol}")

        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error: {str(e)}")
        except (ValueError, KeyError, TypeError) as e:
            raise RuntimeError(f"Unexpected response format: {str(e)}")
        