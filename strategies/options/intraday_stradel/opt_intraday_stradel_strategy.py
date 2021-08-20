import time
import logging
import traceback
from datetime import datetime
import strategies.exitcodes as exitcodes
"""
   Description:
   Params:

"""


class IntradayStradel():
      kite = None
      instrument = None
      inputs = None
      calls = []
      puts  = []
      positions = []
      exit_flag = None
      RANGE_MULTIPLIER = 12

      def print_description(self):
          logging.info(self.inputs.strategy.description)

      def wait_till_time(self,entry_time):
          while True:
              if (datetime.now().time() >=
                      datetime.strptime(entry_time,'%H:%M').time()):
                  return
              time.sleep(60)

      def check_exit_time(self,exit_time):
          if (datetime.now().time() >=
                  datetime.strptime(exit_time,'%H:%M').time()):
              logging.info("Current time beyond stragtegy exit time")
              self.close_all_positions()
              self.exit_flag = exitcodes.EXIT_TIMETRIGGER
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
    

      def trade_stradel(self):
          security = self.inputs.strategy.security
          security_price = self.get_security_price(security)
          security_option_gap = self.inputs.strategy.opt_gap
          call,put = self.get_near_options(security_price,security_option_gap)
          logging.info(f"Stradel start with {call} and {put}")
          call_price = self.kite.quote(f"{call}")[call]["last_price"]
          put_price = self.kite.quote(f"{put}")[put]["last_price"]
          logging.info(f"Selling {call} at {call_price}")
          logging.info(f"Selling {put} at {put_price}")
          #TODO add sell trades 
          self.calls.append(call)
          self.puts.append(put)
          self.positions.append(call)
          self.positions.append(put)
          self.level = 0
          return None

      def price_opt_pair(self,opt_chain,price,key):
          return dict({key:abs(price - opt_chain[key]["last_price"])})

      def get_security_near_price(self,price,opt_type):
          opt_list = []
          opt_dict = {}
          start = int(self.start_price - (self.RANGE_MULTIPLIER * self.inputs.strategy.opt_gap))
          end = int(self.start_price + (self.RANGE_MULTIPLIER * self.inputs.strategy.opt_gap))
          for val in range(start,end,self.inputs.strategy.opt_gap):
              opt_list.append(f"{self.inputs.strategy.opt_name}"
                             f"{self.inputs.strategy.opt_year}"
                             f"{self.inputs.strategy.opt_month}"
                             f"{self.inputs.strategy.opt_day}"
                             f"{val}{opt_type}")
          opt_chain = self.kite.quote(opt_list)
          logging.debug(opt_chain)
          opt_price_lst = [self.price_opt_pair(opt_chain,price,k) for k in opt_list]
          for item in opt_price_lst:
              opt_dict.update(item)
          return min(opt_dict,key=opt_dict.get)

      def quote_security(self):
          main_security = self.inputs.strategy.security
          main_security_price = self.get_security_price(security)
          logging.info(f"{main_security} is now at {main_security_price}")
          

      def sell_put(self,price):
          self.quote_security()
          security = self.get_security_near_price(price,"PE")
          price = self.kite.quote(f"{security}")[security]["last_price"]
          logging.info(f"Selling {security} at {price}")
          #TODO sell code
          self.positions.append(security)
          return None

      def sell_call(self,price):
          self.quote_security()
          security = self.get_security_near_price(price,"CE")
          price = self.kite.quote(f"{security}")[security]["last_price"]
          logging.info(f"Selling {security} at {price}")
          #TODO sell code
          self.positions.append(security)
          return None

      def buy_security(self,security):
          price = self.kite.quote(f"{security}")[security]["last_price"]
          logging.info(f"Buying {security} at {price}")
          #TODO buy market order

      def check_and_add_options(self):
          call_price = 0
          put_price  = 0 
          for c in self.calls:
              call_price = call_price + self.kite.quote(f"{c}")[c]["last_price"]
              logging.debug(f"{c} is at price {call_price}")
          for p in self.puts:
              put_price = put_price + self.kite.quote(f"{p}")[p]["last_price"]
              logging.debug(f"{p} is at price {put_price}")
          if call_price/2 > put_price :
              #call is double to put.
              #adjust with put which is 1/4th price of call
              self.sell_put(call_price/4)
              self.level = self.level + 1
          if put_price/2 > call_price:
              #put is double to put.
              #adjust with call which is 1/4th price of put
              self.sell_call(put_price/4)
              self.level = self.level + 1

      def close_all_positions(self):
          for p in self.positions:
              p_price = self.kite.quote(f"{p}")[p]["last_price"]
              self.buy_security(p)
          logging.info("Closed all positions")

      def stop_loss_hit(self):
          #TODO 
          return False

      def check_stop_loss_exit(self):
          if self.stop_loss_hit():
             self.close_all_positions()
             self.exit_flag = exitcodes.EXIT_STOPLOSS
          else:
             self.check_and_remove_options()

      def check_and_remove_options(self):
          call_price = 0
          put_price  = 0
          for c in self.calls:
              call_price = call_price + self.kite.quote(f"{c}")[c]["last_price"]
          for p in self.puts:
              put_price = put_price + self.kite.quote(f"{p}")[p]["last_price"]
          #TODO check and remvoe options

      def check_target_hit_exit(self):
          #TODO check target hit and exit
          pass    

      def check_and_adjust(self):
          self.check_target_hit_exit()
          self.check_exit_time(self.inputs.strategy.exit.time)
          if self.level < 2 :
              self.check_and_add_options()
          else:
              self.check_stop_loss_exit()

      def watch_adjust_or_exit(self):
          while True:
              if self.exit_flag :
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
          self.print_description()
          self.execute_strategy() 



