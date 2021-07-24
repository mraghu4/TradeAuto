import time
import logging
from datetime import datetime
import strategies.exitcodes as exitcode

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
              exit(exitcode.EXIT_TIME_TRIGGER)
          else:
              return False

      def get_security_price(self,security):
          return self.kite.quote(security)[security]["last_price"]

      def get_near_options(self,security_price,gap):
          near_price=round(security_price/gap)*gap
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
          self.start_price = security_price
          security_option_gap = self.inputs.strategy.opt_gap
          call,put = self.get_near_options(security_price,security_option_gap)
          logging.info(f"Stradel start with {call} and {put}")
          call_price = self.kite.quote(f"{call}")[call]["last_price"]
          put_price = self.kite.quote(f"{put}")[put]["last_price"]
          logging.info(f"Selling {call} at {call_price}")
          logging.info(f"Selling {put} at {put_price}")
          self.calls.append(call)
          self.puts.append(put)
          self.level = 0
          return None

      def buy_put(self,price):
          #TODO
          return None

      def buy_call(self,price):
          #TODO
          return None


      def _check_and_add_options():
          call_price = 0
          put_price  = 0 
          for c in self.calls:
              call_price = call_price + self.kite.quote(f"{c}")[c]["last_price"]
          for p in self.puts:
              put_price = put_price + self.kite.quote(f"{p}")[p]["last_price"]
          if call_price/2 > put_price :
              #call is double to put.
              #adjust with put which is 1/4th price of call
              self.buy_put(call_price/4)
              self.level = self.level + 1
          if put_price/2 > call_price:
              #put is double to put.
              #adjust with call which is 1/4th price of put
              self.buy_call(put_price/4)
              self.level = self.level + 1

      def check_stop_loss_exit():
          if self.stop_loss_hit():
             self.exit_strategy()
          else:
             self.check_and_remove_options()

      def check_and_remove_options():
          call_price = 0
          put_price  = 0
          for c in self.calls:
              call_price = call_price + self.kite.quote(f"{c}")[c]["last_price"]
          for p in self.puts:
              put_price = put_price + self.kite.quote(f"{p}")[p]["last_price"]
          

      def check_and_adjust(self):
          if self.level < 2 :
              self.check_and_add_options()
          else:
              self.check_stop_loss_exit()

      def watch_adjust_or_exit(self):
          while True:
              self.check_and_adjust()
              time.sleep(1)

          return None


      def execute_strategy(self):
          if self.inputs.strategy.entry.type == "time":
              self.check_exit_time(self.inputs.strategy.exit.time)
              self.wait_till_time(self.inputs.strategy.entry.time)
          self.trade_stradel()
          self.watch_adjust_or_exit()

      def start_trade(self,kite,inputs):
          self.kite = kite
          self.inputs = inputs
          self.print_description()
          self.execute_strategy() 



