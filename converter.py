from bs4 import BeautifulSoup
import requests
import json

def error_msg(type, msg):
    err = {type: msg}
    return json.dumps(err)

def local_currency_file():
    with open('currencies_supported.json', encoding='utf8') as data:
        return json.load(data)

def check_currency(user_input):
    try:
        result = [curr for curr in local_currency_file() if curr['cc'] == user_input or curr['symbol'] == user_input]
        if result != []:
            return result[0]['cc']
        else:
            raise NameError
    except:
        return error_msg('Error', "Entered currency code or symbol not found! Mind the upper casing!")

def web_scrape_all_rates(amount, input_currency):
    try:
        url = 'https://www.xe.com/currencytables/?from={}'.format(input_currency)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
    except:
        return error_msg('Error', "Exchange website not responding, please check your connection!")

    # Scrapes currency rate
    table_scraped = soup.find('table', id='historicalRateTbl')
    rows = table_scraped.select('tr')
    rates = {}
    for cur in rows:
        cols = cur.find_all('td')
        if len(cols) > 0:
            rates[cols[0].next.next] = float(cols[2].next)

    # Multiplies rates by amount and round
    for key, value in rates.items():
        rates[key] = round(value * amount, 2)
    return rates

def web_scrape_rate(amount, input_currency, output_currency):
    try:
        url = 'https://www.kurzy.cz/kurzy-men/kurzy.asp?a=X&mena1={}&mena2={}&c={}&d=latest&convert=P%F8eve%EF+m%ECnu' \
            .format(input_currency, output_currency, amount)
        source = requests.get(url).text
    except:
        return error_msg('Error', "Exchange website not responding, please check your connection!")

    soup = BeautifulSoup(source, 'html.parser')

    table_scraped = soup.find_all('span', attrs={'class': 'result'})
    output_str = (table_scraped[1].text)

    if " " in output_str:
        output_str = output_str.replace(" ", "")

    rate = float(output_str)
    rate = round(rate, 2)
    return rate

def convert_between(amount, input_currency, output_currency):
    # Check amount type and value
    try:
        if type(amount) not in [int, float] or amount <= 0:
            raise ValueError
    except:
        return error_msg('Error', "Amount has to be a number greater than zero!")

    input_currency_checked = check_currency(input_currency)
    output_currency_checked = check_currency(output_currency)

    # If currency 3-letter code not found, return an error message defined in check_currency()
    if len(input_currency_checked) != 3:
        return input_currency_checked
    elif len(output_currency_checked) != 3:
        return output_currency_checked
    else:
        result = {
            "input": {
                "amount": amount,
                "currency": input_currency_checked
            },

            "output": {
                output_currency_checked: web_scrape_rate(amount, input_currency_checked, output_currency_checked)
            }
        }
        return json.dumps(result, sort_keys=True)

def convert_to_all(amount, input_currency):
    # Check amount type and value
    try:
        if type(amount) not in [int, float] or amount <= 0:
            raise ValueError
    except:
        return error_msg('Error', "Amount has to be a number greater than zero!")

    input_currency_checked = check_currency(input_currency)

    # If currency 3-letter code not found, return an error message defined in check_currency()
    if len(input_currency_checked) != 3:
        return input_currency_checked

    else:
        result = {
            "input": {
                "amount": amount,
                "currency": input_currency_checked
            },

            "output": web_scrape_all_rates(amount, input_currency_checked)
        }
        return json.dumps(result, sort_keys=True)
