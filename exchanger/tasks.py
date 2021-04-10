import requests
from celery import shared_task
from LMS.settings import EXCHANGE_RATES_SOURCE
from exchanger.models import ExchangeRate
from datetime import timedelta

CURRENCY_MAP = ["USD", "EUR", "UAH"]
UAH_CODE = "UAH"


@shared_task
def get_exchange_rates():
    resp = requests.get(EXCHANGE_RATES_SOURCE)
    resp = resp.json()

    exchange_rates = [get_exchange_rate(d) for d in filter_out_rates(resp)]
    exchange_rates_with_status = []
    for rate in exchange_rates:
        try:
            old_rate = ExchangeRate.objects.get(id=rate.id)
        except ExchangeRate.DoesNotExist:
            old_rate = rate
        rate.buy_status = get_status(old_rate.buy, rate.buy)
        rate.sell_status = get_status(old_rate.sell, rate.sell)
        exchange_rates_with_status.append(rate)
    ExchangeRate.objects.bulk_update_or_create(exchange_rates_with_status,
                                               ['currency_a',
                                                'currency_b',
                                                'buy',
                                                'buy_status',
                                                'sell',
                                                'sell_status',
                                                'created_time'
                                                ], match_field='currency_a')


def filter_out_rates(rates):
    for r in rates:
        currency_a = r["ccy"]
        currency_b = r["base_ccy"]
        if currency_a not in CURRENCY_MAP:
            continue
        if currency_b not in CURRENCY_MAP:
            continue
        if currency_a != UAH_CODE and currency_b != UAH_CODE:
            continue
        yield r


def get_exchange_rate(rate):
    currency_a = rate["ccy"]
    currency_b = rate["base_ccy"]
    return ExchangeRate(
        id=currency_a + currency_b,
        currency_a=currency_a,
        currency_b=currency_b,
        buy=rate["buy"],
        sell=rate["sale"]
    )


def get_status(a, b):
    a = float(a)
    b = float(b)
    if a > b:
        return -1
    elif a < b:
        return 1
    else:
        return 0