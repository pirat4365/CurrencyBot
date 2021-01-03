import requests
from parserconf import get_api


class GetApi:
    def __init__(self, base=None, symbols=None):
        self.api = get_api()
        self.base = base
        self.symbols = symbols

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GetApi, cls).__new__(cls)
        return cls.instance

    def send_quotes(self):
        quotes = None
        page = requests.get(self.api, params={
            'base': self.base,
            'symbols': self.symbols
        })
        if page.ok:
            page_ = page.json()['rates']
            for key, value in page_.items():
                quotes = f" {self.base} -> {self.symbols} {round(value, 2)}"
            return quotes

    def all_quotes(self):
        page = requests.get(self.api, params="rates")
        page_ = page.json()['rates']
        quotes = sorted([])
        for key in page_:
            quotes.append(key)
        return ', '.join(quotes)