import re
import datetime
import logging
import datetime
import importlib
from pathlib import Path
from kiteconnect import KiteConnect
from inputs.input_parser import InputParser



logging.basicConfig(level=logging.DEBUG)



ip = InputParser()
API_KEY = ip.get_apikey()
API_SECRET = ip.get_apisecret()
kite = KiteConnect(api_key=API_KEY)
TOKEN_FILE = "/tmp/kite_token" 


def get_access_token():
    logging.info("Copy {} , login and"
       " provide access token".format(kite.login_url()))
    return input("Enter Token:").strip()


def record_login(access_token):
    time_now = datetime.date.today()
    fd = open(TOKEN_FILE,"w")
    fd.write("{}:{}".format(time_now,access_token))

def get_last_login_date():
    fd = open(TOKEN_FILE,"r")
    data = fd.read()
    pre_date = re.search("([\w\-]+)\:",data).group(1)
    y,m,d = map(int,pre_date.split("-"))
    return  datetime.date(y,m,d)


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
       fd = open(TOKEN_FILE,"r")
       data = fd.read()
       return re.search("\:(\w+)",data).group(1)
    except  e:
       logging.info("{} file might be deleted or modified.\n"
            "please do \"rm -f {}\" it and rerun".format(TOKEN_FILE,TOKEN_FILE)) 


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
