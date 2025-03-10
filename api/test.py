import requests
ALPHA_VANTAGE_API_KEY = "PNPAH7B7UT76I8OI"
company = "goog"
url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company}&apikey={ALPHA_VANTAGE_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)