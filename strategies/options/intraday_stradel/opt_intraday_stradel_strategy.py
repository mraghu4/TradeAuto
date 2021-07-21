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
          return kite.quote(security)[security]["last_price"]

      def get_closer_options(security,security_price,gap):
          #TODO 
    

      def trade_stradel(slef):
          security = self.inputs.strategy.security
          security_price = self.get_security_price(security)
          security_option_gap = self.inputs.strategy.opt_gap
          put,call = self.get_closer_options(security,
                        security_price,security_option_gap)

          return None

      def watch_adjust_or_exit():
          #TODO
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
          slef.print_description()
          self.execute_strategy() 



