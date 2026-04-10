'''Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License. '''
import sqlite3
import os

DATA_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), 'data'))
DB_FILE = os.path.join(DATA_DIR, 'store.db')

class StoreAPI:
    @staticmethod
    def _get_connection():
        return sqlite3.connect(DB_FILE)

    @staticmethod
    def get_all_products():
        conn = StoreAPI._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "name": r[1], "price": r[2], "stock": r[3]} for r in rows]

    @staticmethod
    def get_product(product_id):
        conn = StoreAPI._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, stock FROM products WHERE id=?", (str(product_id),))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2], "stock": row[3]}
        return None

    @staticmethod
    def reduce_stock(product_id, qty):
        conn = StoreAPI._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM products WHERE id=?", (str(product_id),))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Product {product_id} not found")
        
        current_stock = row[0]
        if qty > current_stock:
            conn.close()
            raise ValueError(f"Not enough stock for product {product_id}")
        
        new_stock = current_stock - qty
        cursor.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, str(product_id)))
        conn.commit()
        conn.close()
    @staticmethod
    def log_purchase(username, product_name, qty, total_price):
        conn = StoreAPI._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO purchases (username, product_name, qty, total_price)
            VALUES (?, ?, ?, ?)
        ''', (username, product_name, qty, total_price))
        conn.commit()
        conn.close()
    @staticmethod
    def get_user_history(username):
        conn = StoreAPI._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT product_name, qty, total_price, timestamp 
            FROM purchases 
            WHERE username=? 
            ORDER BY timestamp DESC
        ''', (username,))
        rows = cursor.fetchall()
        conn.close()
        return [{"product_name": r[0], "qty": r[1], "total_price": r[2], "timestamp": r[3]} for r in rows]
