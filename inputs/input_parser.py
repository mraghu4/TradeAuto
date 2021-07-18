import yaml
import logging
from types import SimpleNamespace

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


class InputParser:

   input_yaml_file = "inputs.yaml"
   
   def __init__(self):
       with open(self.input_yaml_file,'r') as infile:
          try:
             data_dict = yaml.safe_load(infile)
             with open("inputs/{}.yaml".format(data_dict["inputs"]["strategy"]["name"])) as stfile:
                  strategy_dict = yaml.safe_load(stfile)
                  data_dict["inputs"]["strategy"].update(strategy_dict)
             self.data =  NestedNamespace(data_dict)
             logging.debug("Inputs:{}".format(self.data))
          except yaml.YAMLError as e:
             print(e)

   def get_inputs(self):
       return self.data.inputs

   def get_apikey(self):
       return self.data.inputs.session.api_key

   def get_apisecret(self):
       return self.data.inputs.session.api_secret
