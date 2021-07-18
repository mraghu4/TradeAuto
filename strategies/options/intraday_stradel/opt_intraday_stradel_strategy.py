import logging

"""
   Description:
   Params:

"""


class IntradayStradel():
      kite = None
      instrument = None

      def start_trade(self,kite,inputs):
          self.kite = kite
          logging.info(inputs.strategy.description)

