import os
import re
import datetime
import time
import logging
import importlib
import sys
import pytz
from pathlib import Path
from inputs.input_parser import InputParser
from neo_api_client import NeoAPI


#arugments
if "-d" in sys.argv:
   log_level = logging.DEBUG
else:
   log_level = logging.INFO
  

#set logging
ist_tz = pytz.timezone('Asia/Kolkata')
def logtz(*args):
    return datetime.datetime.now(ist_tz).timetuple()

logdir = "logs"
if not os.path.exists(logdir):
    os.makedirs(logdir)
file_name = f"log_{time.strftime('%Y%m%d-%H%M%S')}"
logfile = os.path.join(logdir,file_name)
logging.Formatter.converter = logtz
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
USERNAME = ip.get_username()
PASSWORD = ip.get_password()

def login_neo():
    try:
       client = NeoAPI(consumer_key=API_KEY,consumer_secret=API_SECRET,environment="uat")    
       client.login(mobilenumber=USERNAME, password=PASSWORD)
    except Exception as e:
    logging.info(f"Exception while logging in {e}")
    otp = input("Enter OTP:").strip()
    client.session_2fa(OTP=otp)
    otp = None
    return client

def main():
    inputs = ip.get_inputs()
    strategy_mod = importlib.import_module(inputs.strategy.script,package='strategies')
    strategy_class = getattr(strategy_mod,inputs.strategy.classname)
    strategy = strategy_class()
    client = login_neo()
    strategy.start_trade(client,inputs)

#TODO check and continue previous trade if it exited due to connecitivity issues        

if __name__ == "__main__":
    main()
