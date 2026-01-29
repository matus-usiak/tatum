from decimal import Decimal, ROUND_DOWN

import requests

baseUrl = "https://api.tatum.io/v4"
address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

headers = {
    "accept": "application/json",
    "X-Api-Key": "t-69789496ace70350f2244903-a9afc48f474d429ca5f485a0",
    "host": "api.tatum.io"
}


def get_wallet_balance(walletaddress):
    url = f"{baseUrl}/data/wallet/balance/time?chain=ethereum-mainnet&addresses={walletaddress}&time=2099-01-01"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    balance = Decimal(data["result"][0]["balance"])
    return balance.quantize(Decimal("0.00000000"), rounding=ROUND_DOWN)


def get_latest_trx(walletaddress):
    url = f"{baseUrl}/data/transaction/history?chain=ethereum-mainnet&addresses={walletaddress}&transactionTypes" \
          f"=multitoken&sort=desc&pageSize=10"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    chain = []
    tokenaddress = []
    tokenid = []
    i = 0
    while i < 10:
        chain.append(data["result"][i]["chain"])
        tokenaddress.append(data["result"][i]["tokenAddress"])
        tokenid.append(data["result"][i]["tokenId"])
        i += 1
    return chain, tokenid, tokenaddress


def main():
    balance = get_wallet_balance(address)

    transactions = get_latest_trx(address)

    print(f"Current balance: {balance} ETH")

    print(f"Latest trx: {transactions.__getitem__(0)}")


if __name__ == "__main__":
    main()