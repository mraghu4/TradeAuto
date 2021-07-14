import yaml
from types import SimpleNamespace

class InputParser:

   input_yaml_file = "inputs.yaml"
   
   def __init__(self):
       with open(self.input_yaml_file,'r') as infile:
          try:
             self.data = yaml.safe_load(infile)
          except yaml.YAMLError as e:
             print(e)

   def get_apikey(self):
       return self.data["inputs"]["api_key"]

   def get_apisecret(self):
       return self.data["inputs"]["api_secret"]
