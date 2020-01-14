XCHANGE CURRENCY

Application developed on lubuntu 18.04 with python 3.6.9

To install the application, open a shell and  execute the following commands in the xchcurrency directory

1) sudo apt install python3-venv [if not present] 
2) python3 -m venv venv
3) source venv/bin/activate
4) pip install -r requirements.txt
5) export FLASK_APP=xchcurrency.py
6) flask run

(You can skip the first 3 commands if you not use virtual environments)

if you want to execute unit tests, replace the last command with
> flask test

When the app is up and running to verify the service, open another shell and execute a request with the following pattern:
http --json GET http://127.0.0.1:5000/api/v1/[refdate]/[tocurr]/[fromcurr]?amount=[amount]

Examples:
1)  http --json GET http://127.0.0.1:5000/api/v1/JPY/USD?amount=123.1234
2)  http --json GET http://127.0.0.1:5000/ap1/v1/XYZ/USD?amount)123.1212

etc..

