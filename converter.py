from bs4 import BeautifulSoup
import requests
import json

# Loads currencies local file - only for getting currrency symbols
with open('currencies_supported.json') as file:
    data = json.load(file)

def convert_to_all(amount, input_currency):
    # Change currency symbol for currency code
    for currency in data:
        if currency['symbol'] == input_currency:
            input_currency = currency['cc']
            
    url = 'https://www.xe.com/currencytables/?from={}'.format(input_currency)
    source = requests.get(url).text

    # Pass HTML into BeautifulSoup
    soup = BeautifulSoup(source, 'lxml')

    # Srape currency rate
    table_scraped = soup.find('table', id='historicalRateTbl')
    rows = table_scraped.select('tr')
    output = {}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            output[cols[0].next.next] = float(cols[2].next)

    # Multuply rates by amount and round
    for key, value in output.items():
        output[key] = round(value * amount, 2)

    result = {
        "input": {
            "amount": amount,
            "currency": input_currency
        },

        "output": output
    }

    return json.dumps(result, sort_keys=True)

def convert_between(amount, input_currency, output_currency):
    # Change currency symbol for currency code
    for currency in data:
        if currency['symbol'] == input_currency:
            input_currency = currency['cc']
        if currency['symbol'] == output_currency:
            output_currency = currency['cc']

    url = 'https://www.kurzy.cz/kurzy-men/kurzy.asp?a=X&mena1={}&mena2={}&c={}&d=27.6.2011&convert=P%F8eve%EF+m%ECnu'\
        .format(input_currency, output_currency, amount)
    source = requests.get(url).text

    # Pass HTML into BeautifulSoup
    soup = BeautifulSoup(source, 'lxml')

    # Srape currency rate
    table_scraped = soup.find_all('span', attrs={'class': 'result'})
    output_str = (table_scraped[1].text)

    # Delete whitespaces if needed
    if " " in output_str:
        output_str = output_str.replace(" ", "")

    # Parsing output_str to float and round rate
    output = float(output_str)
    output = round(output, 2)

    result = {
        "input": {
            "amount": amount,
            "currency": input_currency
        },

        "output": {
            output_currency: output
        }
    }

    return json.dumps(result, sort_keys=True)


