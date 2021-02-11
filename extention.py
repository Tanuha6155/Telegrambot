import requests
import json
from config import keys

class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base} = {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'{quote} - Не удалось обработать валюту')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'{base} - Не удалось обработать валюту')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать валюту {amount}')

        if float(amount) <= 0:
            raise ConversionException('Число должно быть больше 0.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * float(amount), 2)

        return total_base