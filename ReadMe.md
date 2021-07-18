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
  ```
  
### How to Start trade
   After editing kite inputs.yaml and strategy_inputs.yaml execute
   
    > python3 start_trade.py
