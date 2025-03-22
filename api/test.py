import http.client

conn = http.client.HTTPSConnection("yahoo-finance-real-time1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
    'x-rapidapi-host': "yahoo-finance-real-time1.p.rapidapi.com"
}

conn.request("GET", "/stock/get-quote-summary?symbol=WOOF&lang=en-US&region=US", headers=headers)

res = conn.getresponse()
print(res.read().decode("utf-8"))