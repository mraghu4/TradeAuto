import time
import os
import logging
import traceback
import pytz
import pandas as pd
from datetime import datetime
import strategies.exitcodes as exitcodes
"""
   Description:
   Params:
aaa
   Done:
        1) stradle with stop losses. then move strand if one stoploss hit
        2) exit on stoploss or target hit
        3) enter and exit based on time
        4) final trade report
   TODO:
        1) Continue trade which closed due to program exit

    BUGS:
	1) Live PnL being calcluated only based on open postions
          consider profit/Loss from closed postions
	2) Postion exit price overlap different level entries of smae insturment
       

"""


class IntradayMultiStradel():
      kite = None
      instrument = None
      inputs = None
      calls = []
      puts  = []
      positions = []
      sl_orders = []
      level = 0
      exit_flag = None
      exit_message = None
      ist_tz = pytz.timezone('Asia/Kolkata')
      data = []
      columns = ["Type", "SL_Order_ID","Trade Count","Option",
                 "Entry","Entry Time","Security at Entry",
                 "Exit","Exit Time","Security at Exit"]
      trade_count = 0
      total_entry_val = 0
      offset = 0
      stop_loss_multiplier = 1
      adjust_stop_time = "14:00"

      def print_description(self):
          logging.info(self.inputs.strategy.description)

      def wait_till_time(self,entry_time):
          while True:
              if (datetime.now(self.ist_tz).time() >=
                      datetime.strptime(entry_time,'%H:%M').time()):
                  return
              logging.info(f"No trade will happen untill time is {entry_time}")
              time.sleep(60)

      def get_csv_file(self):
          logdir = "logs"
          if not os.path.exists(logdir):
             os.makedirs(logdir)
          file_name = f"csv_{time.strftime('%Y%m%d-%H%M%S')}"
          csv_report = os.path.join(logdir,file_name)
          return csv_report


      def check_exit_time(self,exit_time):
          if (datetime.now(self.ist_tz).time() >=
                  datetime.strptime(exit_time,'%H:%M').time()):
              logging.info("Current time beyond stragtegy exit time")
              self.close_all_positions()
              self.exit_flag = exitcodes.EXIT_TIMETRIGGER
              self.exit_message = "Exit time reached"
              return True
          else:
              return False

      def get_security_price(self,security):
          return self.kite.quote(security)[security]["last_price"]

      def get_near_options(self,security_price,gap):
          near_price=round(security_price/gap)*gap
          self.start_price = near_price
          near_ce=(f"{self.inputs.strategy.opt_name}"
                   f"{self.inputs.strategy.opt_year}"
                   f"{self.inputs.strategy.opt_month}"
                   f"{self.inputs.strategy.opt_day}"
                   f"{near_price}"
                   "CE")
          near_pe=(f"{self.inputs.strategy.opt_name}"
                   f"{self.inputs.strategy.opt_year}"
                   f"{self.inputs.strategy.opt_month}"
                   f"{self.inputs.strategy.opt_day}"
                   f"{near_price}"
                   "PE")
          return near_ce,near_pe

      def validate_and_get_avg_price_of_order(self,order_id):
          orders =self.kite.orders()
          for order in orders:
              if order['order_id'] == order_id :
                  if  order['status'] == 'REJECTED':
                      logging.error(order['status_message'])
                      self.close_all_positions()
                      self.exit_flag = exitcodes.EXIT_ORDER_PLACE_FAILURE
                      self.exit_message = "Order rejected"
                  else: 
                      return order['average_price']

      def quote_all_positions(self):
          for p in self.positions:
              price = self.kite.quote(f"{p}")[p]["last_price"]
              logging.info(f"{p} at price: {price}")


      def record_trade(self,option,price,trade_type,sl_order_id):
          self.quote_all_positions()
          self.trade_count = self.trade_count + 1
          if option.endswith("CE"):
             opt_type = "CE"
             if trade_type ==  "Entry":
                self.calls.append(option)
             else:
                self.calls.remove(option)
          elif option.endswith("PE"):
             opt_type = "PE"
             if trade_type ==  "Entry":
                self.puts.append(option)
             else:
                self.puts.remove(option)
          if sl_order_id > 0:
             self.sl_orders.append(sl_order_id)
             logging.info(self.kite.order_history(sl_order_id))
          time_now = datetime.now(self.ist_tz)
          security,security_price = self.quote_security()
          if trade_type ==  "Entry":
             self.positions.append(option)
             self.odf = self.odf.append({"Type":opt_type,
                               "Option":option,
                               "Entry":price,
                               "Entry Time":time_now,
                               "Security at Entry": security_price,
                               "Trade Count":self.trade_count,
                               "SL_Order_ID":sl_order_id},
                               ignore_index=True)
          else:
             self.positions.remove(option)
             max_match_trade_cnt = max(self.odf.query(f"Option == {option}")['Trade Count'])
             self.odf.loc[self.odf.Option == option,
                 ["Exit","Exit Time","Security at Exit","Trade Count"]] = [price,time_now,security_price,max_match_trade_cnt]
          logging.info(f"Level:\n{self.level}")
          logging.info(f"Data Frame:\n{self.odf}")
          logging.info(f"CALLS :\n{self.calls}")
          logging.info(f"PUTS :\n{self.puts}")
          logging.info(f"POSTIONS :\n{self.positions}")
          logging.info(f"SL Orders :\n{self.sl_orders}")
 
           
      def trade_stradel(self):
          security = self.inputs.strategy.security
          security_price = self.get_security_price(security)
          security_option_gap = self.inputs.strategy.opt_gap
          call,put = self.get_near_options(security_price,security_option_gap)
          logging.info(f"Creating Stradel with {call} and {put}")
          self.sell_security(call)
          self.sell_security(put)
          self.level = 0
          return None

      def quote_security(self):
          main_security = self.inputs.strategy.security
          main_security_price = self.get_security_price(main_security)
          logging.info(f"{main_security} is now at {main_security_price}")
          return main_security,main_security_price
          

      def sell_security(self,security):
          self.quote_security()
          tradesymbol = security.split(":")[1]
          print(tradesymbol)
          price = 0
          if self.inputs.realtrade:
            try:
                order_id = self.kite.place_order(tradingsymbol=tradesymbol,
                                exchange=self.kite.EXCHANGE_NFO,
                                transaction_type=self.kite.TRANSACTION_TYPE_SELL,
                                quantity=self.inputs.strategy.lotsize,
                                variety=self.kite.VARIETY_REGULAR,
                                order_type=self.kite.ORDER_TYPE_MARKET,
                                product=self.kite.PRODUCT_MIS)
                price = self.validate_and_get_avg_price_of_order(order_id) 
                logging.info(f"Sold {security} at price {price}"
                             f" and quantity {self.inputs.strategy.lotsize}")
            except Exception as e:
                logging.info(f"Order placement failed: {e.message}")
            try:
                sl_order_id = self.kite.place_order(tradingsymbol=tradesymbol,
                                exchange=self.kite.EXCHANGE_NFO,
                                transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                quantity=self.inputs.strategy.lotsize,
                                variety=self.kite.VARIETY_REGULAR,
                                order_type=self.kite.ORDER_TYPE_SL,
                                trigger_price=int(price * self.stop_loss_multiplier),
                                price= int(self.offset + (price * self.stop_loss_multiplier)),
                                product=self.kite.PRODUCT_MIS)
                logging.info(f"Placed SL order for {tradesymbol} ID: {sl_order_id}")
                sl_order_id = int(sl_order_id)
            except Exception as e:
                logging.info(f"Stop Loss Order placement failed: {e.message}")

          else:
            price = self.kite.quote(f"{security}")[security]["last_price"]
            logging.info(f"Sold {security} at price {price}")
          if price > 0:
             self.record_trade(security,price,"Entry",sl_order_id)
          

      def buy_security(self,security):
          self.quote_security()
          tradesymbol = security.split(":")[1]
          price = 0 
          if self.inputs.realtrade:
            try:
                order_id = self.kite.place_order(tradingsymbol=tradesymbol,
                                exchange=self.kite.EXCHANGE_NFO,
                                transaction_type=self.kite.TRANSACTION_TYPE_BUY,
                                quantity=self.inputs.strategy.lotsize,
                                variety=self.kite.VARIETY_REGULAR,
                                order_type=self.kite.ORDER_TYPE_MARKET,
                                product=self.kite.PRODUCT_MIS)
                price = self.validate_and_get_avg_price_of_order(order_id) 
                logging.info(f"Bought {security} at price {price}"
                             f" and quantity {self.inputs.strategy.lotsize}")
            except Exception as e:
                logging.info(f"Order placement failed: {e.message}")
          else:
            price = self.kite.quote(f"{security}")[security]["last_price"]
            logging.info(f"Bought {security} at price {price}")
          if price > 0:
            self.record_trade(security,price,"Exit",0)

      def sl_order_executed(self):
          ret =  False
          for order in self.sl_orders:
              order_report =  self.kite.order_history(order)[-1]
              status = order_report['status']
              if status == "COMPLETE":
                 logging.info(f"SL Order {order} is Executed")
                 self.sl_orders.remove(order)
                 price = order_report['average_price']
                 security = self.odf.loc[self.odf["SL_Order_ID"] == order, 'Option'].iloc[0]
                 self.record_trade(security,price,"Exit",0)
                 logging.info(f"Active SL Orders : {self.sl_orders}")
                 ret = True
          return ret

      def get_ltp_of_order(self,order_id):
          instument = self.odf.loc[self.odf["SL_Order_ID"] == order_id, 'Option'].iloc[0]
          ltp = self.kite.ltp(instument)[instument]['last_price']
          logging.info(f" {instument} is at {ltp}")
          return ltp

      def get_sl_trigger_price(self,order_id):
          return self.kite.order_history(order_id)[-1]['trigger_price']

      def update_trigger_of_exiting_sl_order(self):
          for sl_order in self.sl_orders:
              ltp = self.get_ltp_of_order(sl_order)
              old_trigger_price = self.get_sl_trigger_price(sl_order)
              new_trigger_price = int(ltp * self.stop_loss_multiplier)
              new_price = int(self.offset + (ltp * self.stop_loss_multiplier))
              if new_trigger_price < old_trigger_price:
                  self.kite.modify_order(variety=self.kite.VARIETY_REGULAR,
                                         order_type=self.kite.ORDER_TYPE_SL,
                                         order_id=sl_order,
                                         price=new_price,
                                         trigger_price=new_trigger_price)
                  logging.info(f"Changed Order {sl_order} Trigger price to {new_trigger_price} and Price to {new_price}")
  

      def check_and_add_options(self):
          if self.sl_order_executed():
             self.update_trigger_of_exiting_sl_order()
             if (datetime.now(self.ist_tz).time() >=
                  datetime.strptime(self.adjust_stop_time,'%H:%M').time()):
                 #Time is close to exit. don't trade new stradel
                 return
             self.trade_stradel()

      def generate_report(self):
          if self.odf.shape[0] < 1:
             #return if no trades happened
             return 
          share_PnL = self.odf["Entry"].sum() - self.odf["Exit"].sum()
          total_PnL = share_PnL * self.inputs.strategy.lotsize
          logging.info(self.odf)
          self.odf.to_csv(self.get_csv_file())
          logging.info(f"Total Profit/Loss: {total_PnL}")

      def cancel_all_sl_orders(self):
          for order in self.sl_orders:
              self.kite.cancel_order(variety=self.kite.VARIETY_REGULAR,
                                     order_id = order)

      def close_all_positions(self):
          self.cancel_all_sl_orders()
          for p in self.positions[:]:
              self.buy_security(p)
          logging.info("Closed all positions")
          self.generate_report()

      def stop_loss_hit(self):
          total_current_val = 0 
          for p in self.positions:
             total_current_val = (total_current_val +
                                 self.kite.quote(f"{p}")[p]["last_price"])
          lossp = ((total_current_val - self.total_entry_val) / 
                   self.total_entry_val * 100)
          if lossp > self.inputs.strategy.stoploss:
             return True
          return False
          

      def check_stop_loss_exit(self):
          if self.total_entry_val == 0:
               self.total_entry_val = self.odf["Entry"].sum()
          if self.stop_loss_hit():
               self.close_all_positions()
               self.exit_flag = exitcodes.EXIT_STOPLOSS
               self.exit_message = "Stoploss hit"

      def check_target_hit_exit(self):
          total_entry_val = self.odf["Entry"].sum()
          total_current_val = 0
          for p in self.positions:
             total_current_val = total_current_val + self.kite.quote(f"{p}")[p]["last_price"]
          profitp = (total_entry_val-total_current_val)/total_entry_val * 100
          logging.info(f"\n\tTotal Entry Value: {total_entry_val}"
                       f"\n\tTotal Current value: {total_current_val}"
                       f"\n\tProfit: {profitp}%")
          if profitp > self.inputs.strategy.target:
             self.close_all_positions()
             self.exit_flag = exitcodes.EXIT_TARTGET
             self.exit_message = "Target reached"

      def check_and_adjust(self):
          self.check_target_hit_exit()
          self.check_exit_time(self.inputs.strategy.exit.time)
          self.check_and_add_options()
          self.check_stop_loss_exit()

      def watch_adjust_or_exit(self):
          while True:
              if self.exit_flag :
                  logging.info(f"Exiting due to: {self.exit_message}")
                  exit(self.exit_flag)
              try:
                self.check_and_adjust()
              except Exception as e:
                logging.info(f"Exception occuredi{e}")
                logging.info(traceback.format_exc())
              time.sleep(5)

      def execute_strategy(self):
          if self.inputs.strategy.entry.type == "time":
              if self.check_exit_time(self.inputs.strategy.exit.time):
                 exit(exitcodes.EXIT_TIMETRIGGER)
              self.wait_till_time(self.inputs.strategy.entry.time)
          self.trade_stradel()
          self.watch_adjust_or_exit()

      def start_trade(self,kite,inputs):
          self.kite = kite
          self.inputs = inputs
          self.odf = pd.DataFrame(self.data,columns=self.columns)
          self.offset = self.inputs.strategy.offset
          self.adjust_stop_time = self.inputs.strategy.adjust_stop_time
          self.stop_loss_multiplier = self.stop_loss_multiplier + (self.inputs.strategy.order_stop_loss / 100)
          self.print_description()
          self.execute_strategy() 



