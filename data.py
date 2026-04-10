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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DB_FILE = os.path.join(DATA_DIR, 'store.db')

os.makedirs(DATA_DIR, exist_ok=True)

initial_products = [
    {"id": "1", "name": "Coffee", "price": 3.50, "stock": 20},
    {"id": "2", "name": "Tea", "price": 2.00, "stock": 30},
    {"id": "3", "name": "Chocolate", "price": 1.50, "stock": 50},
    {"id": "4", "name": "Bisquits", "price": 2.20, "stock": 40},
    {"id": "5", "name": "En. drink Monster", "price": 1.49, "stock": 50},
    {"id": "6", "name": "En. drink Lucky punch", "price": 1.10, "stock": 15},
    {"id": "7", "name": "En. drink Dynamite", "price": 1.59, "stock": 40},
    {"id": "8", "name": "Cheese", "price": 4.50, "stock": 100},
    {"id": "9", "name": "Smoked mackarel", "price": 4.20, "stock": 50000}
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create the products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    ''')

    # NEW: Create the purchases table for user history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            product_name TEXT,
            qty INTEGER,
            total_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert initial products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        for p in initial_products:
            cursor.execute('''
                INSERT INTO products (id, name, price, stock)
                VALUES (?, ?, ?, ?)
            ''', (p["id"], p["name"], p["price"], p["stock"]))
        print("Database initialized successfully at:", DB_FILE)
    else:
        print("Database already contains data at:", DB_FILE)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()