# from fastapi import FastAPI

from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
import os
from database import Database
from crypt_1 import *

app = Flask(__name__)

db = Database()

@app.route("/")
def index_main():
    return render_template('index.html')


@app.route("/buy-op")
def index():
    user_id = encrypt(request.args.get('user_id'))
    orders = db.get_orders_info(user_id) 
    for i in orders:
        print('Заменяю')
        i['owner'] = str(crypt(i['owner']))

        
    return render_template('index.html', orders = orders )

@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        state = 0
        if request.form.get('state'):
            state = 1
        value = {
            'channel_id' : request.form.get('channel-id'),
            'name' : request.form.get('name'),
            'link' : request.form.get('link'),
            'count' : request.form.get('count'),
            'state' : state,
            'id' : request.args.get('order_id')
        }
        db.update_order(value)
    user_id = encrypt(str(request.args.get('user_id')))

    ord_id = request.args.get('order_id')
    order = db.get_order(ord_id)
    order['owner'] = crypt(order['owner'])

    if db.check_order_user(ord_id, user_id) is True:
        return render_template('edit.html', order = order)
    else:
        return 'Ошибка'

    




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(debug=True, host='0.0.0.0', port=port)