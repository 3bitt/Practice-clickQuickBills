# clickQuickBills - v0.1 - WIP
Simple Python Click library CLI program for tracking bills spendings and resources consumption per month (Electricity, Water, Gas).


Prerequisite:
  - Click library
  
How to use:
  - Clone repo
  - Install Click ( reference: https://click.palletsprojects.com/en/7.x/quickstart/ )
    - In working directory type <code>pip install Click</code>
  - Run <code>python bills.py --help</code>
  
  
  
  
  Info:
  
    - When adding your bills do it in ascending order (2019/01, 2019/02, etc.)
    - Consumption and fee calculations happen only for second and above bills 
    (first one is without calculations - becouse there is nothing to calculate against in this case)  
