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


def get_latest_transactions(walletaddress):
    url = f"{baseUrl}/data/transaction/history?chain=ethereum-mainnet&addresses={walletaddress}&transactionTypes" \
          f"=fungible,multitoken&sort=desc&pageSize=10"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    direction = []
    amount = []
    tokenname = []
    i = 0
    while i < 10:
        # get data from transaction which are needed to get token info
        chain = data["result"][i]["chain"]
        tokenaddress = data["result"][i]["tokenAddress"]
        direction.append(data["result"][i]["transactionSubtype"])
        amount.append(data["result"][i]["amount"])

        url = f"{baseUrl}/data/tokens?chain={chain}&tokenAddress={tokenaddress}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tokendata = response.json()
        tokenname.append(tokendata["name"])
        i += 1
    return tokenname, direction, amount


def get_popular_tokens():
    url = f"{baseUrl}/data/tokens/popular?chain=ethereum-mainnet&timeframe=1d&pagesize=10"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "rank": item.get("rank"),
            "symbol": item.get("symbol"),
            "priceUSD": item.get("priceUSD"),
            "priceChanges": item.get("priceChanges", {}).get("1d")
        }
        for item in data.get("data", [])
    ]


def main():
    balance = get_wallet_balance(address)

    transactions = get_latest_transactions(address)

    top10 = get_popular_tokens()

    print(f"Current balance: {balance} ETH\n")

    print("Latest transactions:")
    names, directions, amounts = transactions

    for name, direction, amount in zip(names, directions, amounts):
        if direction == "incoming":
            print(f"+ {amount}, {name}")
        elif direction == "outgoing":
            print(f"- {amount}, {name}")

    print("\nTop 10 popular tokens:")

    for token in top10:
        print(f"{token['rank']}. {token['symbol']}, {token['priceUSD']:.2f} USD, {token['priceChanges']}")


if __name__ == "__main__":
    main()
