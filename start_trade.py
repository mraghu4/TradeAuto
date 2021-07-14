import logging
from kiteconnect import KiteConnect
from inputs.input_parser import InputParser



logging.basicConfig(level=logging.DEBUG)



ip = InputParser()
API_KEY = ip.get_apikey()
API_SECRET = ip.get_apisecret()
kite = KiteConnect(api_key=API_KEY)


def get_access_token():
    logging.info("Copy {} , login and provide access token".format(kite.login_url()))
    return input("Enter Token:").strip()


def record_login(access_token):
#TODO
def last_login():
#TODO
def get_last_access_token():
#TODO

def generate_session():
    if last_login() > 24: 
       #generate new token if not logged in last 24 Hours
       data = kite.generate_session(get_access_token(), api_secret=API_SECRET)
       access_token = data["access_token"]
       record_login(access_token)
    else:
       #use same access if logged in last 24 Hours
       access_token = get_last_access_token()

    kite.set_access_token(data["access_token"])


def main():
    generate_session()
    
    
        

if __name__ == "__main__":
    main()
