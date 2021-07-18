import re
import datetime
import logging
import datetime
import importlib
from pathlib import Path
from kiteconnect import KiteConnect
from inputs.input_parser import InputParser



logging.basicConfig(level=logging.DEBUG)
"""
 You might want to get debug mode from cmd line args when program starts. you dont want to run in debug mode always.
"""


ip = InputParser()
API_KEY = ip.get_apikey()
API_SECRET = ip.get_apisecret()
kite = KiteConnect(api_key=API_KEY)
TOKEN_FILE = "/tmp/kite_token" 
# File seperator might vary from OS to OS, you might use file seperator from OS module.


def get_access_token():
    logging.info("Copy {} , login and"
       " provide access token".format(kite.login_url()))
    return input("Enter Token:").strip()
    # You might want to accept this from command line instead making interactive


def record_login(access_token):
    time_now = datetime.date.today()
    fd = open(TOKEN_FILE,"w")
    # Consider using 'when open(TOKEN_FILE,"w") as fd':
    # Or, Null check for fd, close the fd after done.
    fd.write("{}:{}".format(time_now,access_token))
    # fd.write(f"{}:{}", time_now,access_token) is short hand notation for format.
    

def get_last_login_date():
    fd = open(TOKEN_FILE,"r")
    # Consider using 'when open(TOKEN_FILE,"w") as fd':
    # Or, Null check for fd, close the fd after done.
    data = fd.read()
    pre_date = re.search("([\w\-]+)\:",data).group(1)
    y,m,d = map(int,pre_date.split("-"))
    # string to date methods are available in Python, you just need to specify what is the format of the input string whether dd-mm-yyyy or mm-dd-yyyy for example.
    return  datetime.date(y,m,d)


def days_from_last_login():
    token_file = Path(TOKEN_FILE)
    if not token_file.exists():
       #never logged in need a new session
       return 1
       # but you're checking for >0 .
       # You can return 'None' alternatively.
    pre_date = get_last_login_date()
    date_now = datetime.date.today()
    return (date_now-pre_date).days

def get_last_access_token():
    try:
       fd = open(TOKEN_FILE,"r")
       # Consider using 'when open(TOKEN_FILE,"w") as fd':
       # Or, Null check for fd, close the fd after done.
       data = fd.read()
       return re.search("\:(\w+)",data).group(1)
     
    except e:
       logging.info("{} file might be deleted or modified.\n"
            "please do \"rm -f {}\" it and rerun".format(TOKEN_FILE,TOKEN_FILE)) 
        # this can of logger.error category.

def generate_session():
    if days_from_last_login() > 0: 
       try:
           #generate new token if not logged in last 24 Hours
           data = kite.generate_session(get_access_token(), api_secret=API_SECRET)
       except e:
           logging.info("Not able to connect, Check input params and token passed")
            # can be error category.
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
