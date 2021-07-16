"""
   Description:
   Params:

"""


class IntradayStradel():
      kite = None
      instrument = None

      def __init__(self,kite):
          slef.kite = kite

      def load_strategy_params(params_file):
          #TODO          
          

      def start_trade():
           load_strategy_params()
           spot_price = kite.quote(instrument)
           l1_instruments = get_l1_insturments(instrument,spot_price)
           #TODO 
