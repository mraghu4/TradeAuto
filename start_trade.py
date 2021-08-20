import os
import re
import datetime
import time
import logging
import importlib
import sys
from pathlib import Path
from kiteconnect import KiteConnect
from inputs.input_parser import InputParser

#arugments
if "-d" in sys.argv:
   log_level = logging.DEBUG
else:
   log_level = logging.INFO
  

#set logging
logdir = "logs"
if not os.path.exists(logdir):
    os.makedirs(logdir)
file_name = f"log_{time.strftime('%Y%m%d-%H%M%S')}"
logfile = os.path.join(logdir,file_name)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] : %(message)s",
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler()
    ]
)

#Variables
ip = InputParser()
API_KEY = ip.get_apikey()
API_SECRET = ip.get_apisecret()
kite = KiteConnect(api_key=API_KEY)
TOKEN_FILE = os.path.join(logdir,"kite_token")

#definitions
def get_access_token():
    logging.info("Copy {} , login and"
       " provide access token".format(kite.login_url()))
    return input("Enter Token:").strip()


def record_login(access_token):
    time_now = datetime.date.today()
    with open(TOKEN_FILE,"w") as fd:
      fd.write(f"{time_now}:{access_token}")

def get_last_login_date():
    with open(TOKEN_FILE,"r") as fd:
       data = fd.read()
    pre_date = re.search("([\w\-]+)\:",data).group(1)
    return  datetime.datetime.strptime(pre_date,"%Y-%m-%d").date()


def days_from_last_login():
    token_file = Path(TOKEN_FILE)
    if not token_file.exists():
       #never logged in need a new session
       return 1
    pre_date = get_last_login_date()
    date_now = datetime.date.today()
    return (date_now-pre_date).days

def get_last_access_token():
    try:
       with open(TOKEN_FILE,"r") as fd:
          data = fd.read()
       return re.search("\:(\w+)",data).group(1)
    except  e:
       logging.info(f"{TOKEN_FILE} file might be deleted or modified.\n"
            "please do \"rm -f {TOKEN_FILE}\" it and rerun") 


def generate_session():
    if days_from_last_login() > 0: 
       try:
           #generate new token if not logged in last 24 Hours
           data = kite.generate_session(get_access_token(), api_secret=API_SECRET)
       except e:
           logging.info("Not able to connect, Check input params and token passed")
       access_token = data["access_token"]
       record_login(access_token)
    else:
       #use same access if logged in last 24 Hours
       access_token = get_last_access_token()

    kite.set_access_token(access_token)


def main():
    generate_session()
    inputs = ip.get_inputs()
    strategy_mod = importlib.import_module(inputs.strategy.script,package='strategies')
    strategy_class = getattr(strategy_mod,inputs.strategy.classname)
    strategy = strategy_class()
    strategy.start_trade(kite,inputs)

        

if __name__ == "__main__":
    main()
