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

      def print_description():
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

      def trade_stradel():
          #TODO
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
          self.execute_strategy() 



