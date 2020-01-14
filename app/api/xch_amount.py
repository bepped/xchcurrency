from flask import jsonify, request, current_app, make_response
from . import api
from .errors import bad_request, not_found
import re

@api.route('/<dt>/<to_curr>/<from_curr>', methods=['GET'])
def xch_amount(dt, to_curr, from_curr):
    
    if current_app.config['DATE_REGEX'].match(dt) is None :
        return bad_request(f'malformed date {dt}')

    amount = request.args.get('amount')
    if amount is None:
        return bad_request(f'amount is not available: {amount}')

    try:
        amount = float(amount)
    except ValueError:
        return bad_request(f'amount not a quantity: {amount}')
    
    to_curr = to_curr.upper()
    from_curr = from_curr.upper()
    
    if to_curr not in current_app.config['DB_EXCH_CURRENCY'].columns:
        return not_found(f'not found currency code: {to_curr}')

    if from_curr not in current_app.config['DB_EXCH_CURRENCY'].columns:
        return not_found(f'not found currency code: {from_curr}')

    if dt not in current_app.config['DB_EXCH_CURRENCY'].index:
        return not_found(f'not found date: {dt}')
        
    to_curr_rate = current_app.config['DB_EXCH_CURRENCY'].loc[dt, to_curr]
    from_curr_rate = current_app.config['DB_EXCH_CURRENCY'].loc[dt, from_curr]
    to_curr_amount = amount * to_curr_rate / from_curr_rate

    n_dec = current_app.config['CURRENCY_NDEC'][to_curr]
    fmt = f'%.{n_dec}f'
    str_amount = fmt % to_curr_amount

    return make_response(jsonify(amount = f"{str_amount}", currency = f"{to_curr}" ), 200)
    
