import logging
from kiteconnect import KiteConnect



logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="m84lyrd6ym1wsj58")
print(kite.login_url())

#data = kite.generate_session("U4N3vYQEX01bQCky5k5Y0rNFUm66SzRp", api_secret="vo3u61mppb2o7r6ler2ck7edh8z0grot")
#kite.set_access_token(data["access_token"])
kite.set_access_token("mOlh4gSPghi0hcAjuS3HI3NwT5Ug2plk")

#print(data["access_token"])

# Place an order
"""
try:
    order_id = kite.place_order(tradingsymbol="DODLA",
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC)

    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))
"""
# Fetch all orders
#print(kite.holdings())
#print(kite.quote('NSE:NIFTY BANK')["NSE:NIFTY BANK"]["last_price"])
#print(kite.quote(['NFO:BANKNIFTY2180535000CE','NFO:BANKNIFTY2180535000PE']))
#print(kite.quote('NFO:BANKNIFTY2180535000CE'))
l = []
price = 364
for val in range(35000 - 1200,35000 +1200,100):
    l.append(f"NFO:BANKNIFTY21805{val}CE")
opt_chain = kite.quote(l)
print(opt_chain)
def price_opt_pair(key):
    return dict({key:abs(price - opt_chain[key]["last_price"])})
price_dict = {}
lst = list(map(price_opt_pair,l))
print(lst)
for n in lst:
  price_dict.update(n)
print(price_dict)
near = min(price_dict,key=price_dict.get)
print(near)
print(price_dict[near])

