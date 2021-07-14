import logging
from kiteconnect import KiteConnect



logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="m84lyrd6ym1wsj58")
print(kite.login_url())

#data = kite.generate_session("iVkPZM8Z5FU03QU2HMd3a6ynk5G8cdv2", api_secret="r4oqcwqn4o8mi7fwez1rfampid88sj45")
kite.set_access_token("2SRUWSVLg6wmIGAUB3m3JuB3SH9aXN1x")

#print(data["access_token"])

# Place an order
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

# Fetch all orders
kite.orders()

