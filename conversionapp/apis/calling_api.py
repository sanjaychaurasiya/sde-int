import requests as re


response = re.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/inr/usd.json")
print(response.text)