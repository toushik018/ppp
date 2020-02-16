import requests 
import json
from steemengine.tokenobject import Token

def formatting(data):
  balance = data['balance']
  stake = data['stake']
  deligation =data['delegationsIn']
  delegationOut = data['delegationsOut']
  response = "Balance:{0}\nStake:{1}apx\nDelegationIn:{2}apx\nDelegationOut:{3}apx".format(balance,stake,deligation,delegationOut)
  return response

def balance(username):
  url = "https://api.steem-engine.com/rpc/contracts"

  payload = "[{\"method\": \"find\", \"jsonrpc\": \"2.0\", \"params\": {\"contract\": \"tokens\", \"table\": \"balances\", \"query\": { \"account\": \""+username+"\"}, \"limit\": 1000, \"offset\": 0, \"indexes\": []}, \"id\": 1}]"
  headers = {
          'User-Agent': "steemengine v0.5.0",
          'Content-Type': "application/json",
          'Cache-Control': "no-cache",
          }

  response = requests.request("POST", url, data=payload, headers=headers)
  result2 = response.json()[0]["result"]
  for i in result2:
    if 'APX' in i.values():
      data = formatting(i)
      return data


def price(symble):
  try:
    token = Token(symble.upper())
    market_info = token.get_market_info()
    last_price = float(market_info["lastPrice"])
    return last_price
  except Exception as e:
    print(e)
    return None
