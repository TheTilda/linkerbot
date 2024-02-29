import mysql.connector
import random
from config import *


class Database():
    def __init__(self) -> None:
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        test = self
    
    def add_user(self, user_id, username, name, last_name, is_premium, lang):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        print(self.cursor.fetchone())
        print(self.cursor.rowcount)
        if self.cursor.rowcount == -1:
            query = ("INSERT INTO users(user_id, username, name, last_name, is_premium, lang) VALUES(%s,%s,%s,%s,%s,%s)")
            val = (user_id, username, name, last_name, is_premium, lang) 
            try: 
                self.cursor.execute(query,val) 
                self.cnx.commit() 
            except Exception as ex: 
                print(ex)
                self.cnx.rollback() 
            return "succes create user"
        else:
            return "has alredy created"
    def get_user(self, user_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        return self.cursor.fetchone()
    
    def cut_link(self, user_id, link):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        gen_user = ''
        for i in range(15):
            gen_user+= random.choice("abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        self.cursor.execute(f"SELECT * FROM links WHERE link_id = '{gen_user}' ")
        if self.cursor.fetchone():
            for i in range(15):
                gen_user+= random.choice("abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

        query = ("INSERT INTO links(link, link_id, count, owner) VALUES(%s,%s,%s,%s)")
        val = (link, gen_user, 0, user_id) 
        try: 
            self.cursor.execute(query,val) 
            self.cnx.commit() 
        except Exception as ex: 
            print(ex)
            self.cnx.rollback() 

        return gen_user
    
    def get_link(self, link_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT link FROM links WHERE link_id = '{link_id}'")
        return self.cursor.fetchone()['link']

    def add_order(self, channel_id, name, link, count, owner):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        query = ("INSERT INTO orders(channel_id, name, link, count, owner) VALUES(%s,%s,%s,%s,%s)")
        val = (channel_id, name, link, count, owner) 
        try: 
            self.cursor.execute(query,val) 
            self.cnx.commit() 
        except Exception as ex: 
            print(ex)
            self.cnx.rollback() 

    def update_order(self, values):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        query = (f"UPDATE orders SET channel_id = '{values['channel_id']}', link = '{values['link']}', name = '{values['name']}', count = '{values['count']}', state = {values['state']} WHERE id = {values['id']}")
        try: 
            self.cursor.execute(query) 
            self.cnx.commit() 
        except Exception as ex: 
            print(ex)
            self.cnx.rollback() 

    def get_orders_info(self, user_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM orders WHERE owner = '{user_id}'")
        return self.cursor.fetchall()

    def get_order(self, order_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM orders WHERE id = '{order_id}'")
        return self.cursor.fetchone()

    def check_order_user(self, order_id, user_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM orders WHERE owner = {user_id} AND id = '{order_id}'")
        if self.cursor.fetchone() is None:
            return False
        else:
            return True
    def get_op(self):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT * FROM orders WHERE state = 1")
        result_op = []
        op = self.cursor.fetchall()
        users = []
        for i in op:
            self.cursor.execute(f"SELECT balance FROM users WHERE user_id = {i['owner']}")
            if float(self.cursor.fetchone()['balance']) >= price:
                result_op.append(i)
                users.append(int(i['owner']))
        
        return result_op
        
    def get_channel_from_order(self, order_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT channel_id FROM orders WHERE id = {order_id}")
        channel_id = self.cursor.fetchone()['channel_id']
        return channel_id
    
    def buy_op(self, order_id):
        self.cnx = mysql.connector.connect(user='gen_user', password='ta54D=7vdC<3fk',
                                    host='89.23.118.157',
                                    database='default_db')

        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)
        self.cursor.execute(f"SELECT owner FROM orders WHERE id = {order_id}")
        user_id = self.cursor.fetchone()['owner']
        query = (f"UPDATE users SET balance = balance - {price} WHERE user_id = {user_id}")
        try: 
            self.cursor.execute(query) 
            self.cnx.commit() 
        except Exception as ex: 
            print(ex)
            self.cnx.rollback() 

        
