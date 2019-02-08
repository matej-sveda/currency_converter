import json

# Loads currencies local file - only for getting currrency symbols
with open('currencies_supported.json') as file:
    data = json.load(file)

cc_and_symbols = []
for currency in data:
    currencies.append(currency['cc'])
    currencies.append(currency['symbol'])

print(currencies)

if 'USD' in currencies:
    print("seš hovno")
else:
    print("oukej no")

print(data)