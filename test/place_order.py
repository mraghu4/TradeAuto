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
print(kite.quote('NSE:NIFTY BANK')["NSE:NIFTY BANK"]["last_price"])
print(kite.quote(['NFO:BANKNIFTY2180535000CE','NFO:BANKNIFTY2180535000PE']))
print(kite.quote('NFO:BANKNIFTY2180535000CE'))

