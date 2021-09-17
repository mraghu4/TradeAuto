import logging
from kiteconnect import KiteConnect



logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="m84lyrd6ym1wsj58")
print(kite.login_url())

#data = kite.generate_session("WOBV6emxxCLsqYYrNJE5THjYZMlUsIEK", api_secret="boud3qal7mgpra74yhxj1gbaovghscxq")
#kite.set_access_token(data["access_token"])
kite.set_access_token("WOBV6emxxCLsqYYrNJE5THjYZMlUsIEK")

#print(data["access_token"])

def get_avg_price_of_order(order_id):
    orders = kite.orders()
    for order in orders:
        print(order,order_id) 
        if order['order_id'] == order_id:
           return order['average_price']

# Place an order
"""
try:
    order_id = kite.place_order(tradingsymbol="BANKNIFTY21SEP35000PE",
                                exchange=kite.EXCHANGE_NFO,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=25,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC)

    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))
"""

#print(kite.orders())
#print(kite.order_history(210824400551980))
print(get_avg_price_of_order('210824400551980'))

# Fetch all orders
#print(kite.holdings())
#print(kite.quote('NSE:NIFTY BANK')["NSE:NIFTY BANK"]["last_price"])
#print(kite.quote(['NFO:BANKNIFTY2180535000CE','NFO:BANKNIFTY2180535000PE']))
#print(kite.quote('NFO:BANKNIFTY2180535000CE'))
"""
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

ps = kite.positions()
print(ps)


print()
"""
