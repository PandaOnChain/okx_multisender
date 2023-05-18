import time
import ccxt
from termcolor import cprint
import random


def get_balance(exchange, symbol):
    try:
        balance = exchange.fetch_balance()
        return balance['total'][symbol.upper()]
    except KeyError:
        return None


def okx_withdraw(address, amount_to_withdrawal, symbolWithdraw, network, API_KEY, API_SECRET, PASSPHRASE):

    account_okx = ccxt.okx({
        'apiKey': API_KEY,
        'secret': API_SECRET,
        'password': PASSPHRASE,
        'enableRateLimit': True,
    })

    try:
        balance = get_balance(account_okx, symbolWithdraw)
        print(balance)
        info = account_okx.fetch_currencies()
        network_fee = info[symbolWithdraw]['networks'][network]['fee']
        chainName = info[symbolWithdraw]['networks'][network]['id']
        print(str(network_fee) + "\n" + chainName)
        account_okx.withdraw(
            code=symbolWithdraw,
            amount=str(amount_to_withdrawal),
            address=address,
            params={
                "toAddress": address,
                "chainName": chainName,
                "fee": network_fee,
                'pwd': '-',
                'amt': str(amount_to_withdrawal),

            }
        )

        cprint(f">>> Успешно | {address} | {amount_to_withdrawal}", "green")
    except Exception as error:
        cprint(f">>> Неудачно | {address} | ошибка : {error}", "red")


if __name__ == "__main__":

    with open("./wallets.txt", "r") as f:
        wallets_list = [row.strip() for row in f]

    symbolWithdraw = 'ARB'
    network = 'Arbitrum one'  # ETH | BSC | AVAXC | MATIC | ARBITRUM | OPTIMISM | APT

    API_KEY = "###"
    API_SECRET = "###"
    PASSPHRASE = "###"
    AMOUNT_FROM = 1.011
    AMOUNT_TO = 3.011

    cprint('\a\n/// start withdrawing...', 'white')
    for wallet in wallets_list:
        # последня цифра в скобках - число знаков после запятой
        amount_to_withdrawal = round(random.uniform(AMOUNT_FROM, AMOUNT_TO), 2)
        print(amount_to_withdrawal)
        okx_withdraw(wallet, amount_to_withdrawal, symbolWithdraw,
                     network, API_KEY, API_SECRET, PASSPHRASE)
        time.sleep(random.randint(2, 4))
