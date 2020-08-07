"""Currency converter solution for week 2 API practice task."""

import re
from decimal import Decimal

from bs4 import BeautifulSoup


def convert(
        amount: Decimal, cur_from: str, cur_to: str, date: str,
        requests: object
) -> Decimal:
    """Convert given amount of one currency to another.

    Using RUR as an intermediate currency.

    https://cbr.ru/development/SXML/

    :param date: date on which the exchange rate is requested
    """
    intermediate_currency_code = 'RUR'

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    if date and re.match(r'^\d{2}[.-/]\d{2}[.-/]\d{4}$', date):
        url += f'?date_req={date}'
    else:
        print("Invalid date format. Using current exchange rate.")

    response = requests.get(url)
    response.raise_for_status()
    exchange_rate_data = BeautifulSoup(response.text, 'html.parser')
    print(exchange_rate_data)

    if cur_from == intermediate_currency_code:
        source_rate = Decimal('1.0')
    else:
        source_rate = get_cbr_rate(cur_from, exchange_rate_data)

    if cur_to == intermediate_currency_code:
        target_rate = Decimal('1.0')
    else:
        target_rate = get_cbr_rate(cur_to, exchange_rate_data)

    result = (amount * source_rate) / target_rate
    return result.quantize(Decimal('.0001'))


def get_cbr_rate(
        currency_code: str, exchange_rate_data: BeautifulSoup
) -> Decimal:
    """Get currency rate from CBR exchange market xml."""
    currency_data = exchange_rate_data.find(
        'charcode', text=currency_code
    ).find_parent('valute')
    denomination_rate = int(currency_data.find('nominal').text)
    rate = Decimal(currency_data.find('value').text.replace(',', '.'))
    return rate / denomination_rate
