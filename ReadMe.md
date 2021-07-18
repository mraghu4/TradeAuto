# TradeAuto
### Description
  Automation of your daily trading using Zehrodha kite python API.
### Scope
  - User have choice to select strategy
  - User have choice to modify the stragey params like Stop loss, profit target, entry condition, exit condition etc.
  - Software will trade based on inputs and creates a report once exit condition met
  - Design should alow to plugin new strategies
  
### Pre-requisites
  - python
  - kiteconnect api
  ```
     pip3 install --upgrade pip 
     pip3 install kiteconnect      
     pip3 install pathlib
     pip3 install pyyaml
     pip3 install logger
  Dependencies can be handled in two ways: 
  - One: create a requirements.txt and enumerate all the needed modules, single command will install all dependencies
  - Two: creaete w wheels package for the whole project, installation of wheel pull the dependencies and install the curren project as well.
  
  Use .gitingore in pycache folders to avoid pushing them.
    
### How to Start trade
   After editing kite inputs.yaml and strategy_inputs.yaml execute
   
    > python3 start_trade.py
