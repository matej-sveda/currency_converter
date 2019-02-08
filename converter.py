from bs4 import BeautifulSoup
import requests
import json

def error_msg(type, msg):
    err = {type: msg}
    return json.dumps(err)

def convert(amount, input_currency, output_currency=None):
    input_currency = input_currency.upper()
    output_currency = output_currency.upper()
    # Loads local file and creates a list of available currencies
    with open('currencies_supported.json') as file:
        data = json.load(file)
        currencies = []
        for currency in data:
            currencies.append(currency['cc'])
            currencies.append(currency['symbol'])
            
    try:
        if type(amount) not in [int, float] or amount <= 0:
            raise RuntimeError
    except:
        return error_msg('ValueError', "Amount has to be a number greater than zero!")

    try:
        if input_currency not in currencies or output_currency not in currencies:
            if output_currency is None and input_currency in currencies:
                pass
            else:
                raise NameError
    except:
        return error_msg('NameError', "Entered currency code or symbol not found! Mind the letter casing!")

    # Case executed without output_currency argument
    if output_currency is None:
        # Changes currency symbol for currency code
        for currency in data:
            if input_currency == currency['symbol']:
                input_currency = currency['cc']

        url = 'https://www.xe.com/currencytables/?from={}'.format(input_currency)
        source = requests.get(url).text
        # Passes HTML into BeautifulSoup
        soup = BeautifulSoup(source, 'lxml')

        # Scrapes currency rate
        table_scraped = soup.find('table', id='historicalRateTbl')
        rows = table_scraped.select('tr')
        output = {}
        for cur in rows:
            cols = cur.find_all('td')
            if len(cols) > 0:
                output[cols[0].next.next] = float(cols[2].next)

        # Multiplies rates by amount and round
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

    # Case executed without output_currency argument
    else:
        # Changes currency symbol for currency code
        for currency in data:
            if currency['symbol'] == input_currency:
                input_currency = currency['cc']
            if currency['symbol'] == output_currency:
                output_currency = currency['cc']

        url = 'https://www.kurzy.cz/kurzy-men/kurzy.asp?a=X&mena1={}&mena2={}&c={}&d=27.6.2011&convert=P%F8eve%EF+m%ECnu'\
            .format(input_currency, output_currency, amount)
        source = requests.get(url).text

        # Passes HTML into BeautifulSoup
        soup = BeautifulSoup(source, 'lxml')

        # Srapes currency rate
        table_scraped = soup.find_all('span', attrs={'class': 'result'})
        output_str = (table_scraped[1].text)

        # Deletes whitespaces if needed
        if " " in output_str:
            output_str = output_str.replace(" ", "")

        # Parses output_str to float and round rate
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

        # Returns json result
        return json.dumps(result, sort_keys=True)

convert(10, "USD", "EUR")