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
import tkinter as tk
from tkinter import messagebox
from models import Cart  
from api import StoreAPI 
from login_widget import show_login

class GUI:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        
        self.root.withdraw() 
        self.root.title("Small internet store simulation")
        
        self.cart = Cart() 
        
        show_login(on_success=self.on_login_success, master=self.root)

    def on_login_success(self, username):
        print("Logged in as", username)
        self.current_user = username
        
        self.build_ui()
        self.update_list()
        self.status_label.config(text=f"Connected as: {username}")
        
        self.root.deiconify()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        self.listbox = tk.Listbox(frame, width=70, height=12)
        self.listbox.grid(row=0, column=0, columnspan=3, pady=(0,10))

        tk.Label(frame, text="Qty:").grid(row=1, column=0, sticky='e')
        self.qty_entry = tk.Entry(frame, width=8)
        self.qty_entry.grid(row=1, column=1, sticky='w')
        self.qty_entry.insert(0, "1")

        tk.Button(frame, text="Add to cart", command=self.add_to_cart, width=18).grid(row=2, column=0, pady=6)
        tk.Button(frame, text="Check your cart", command=self.view_cart, width=18).grid(row=2, column=1, pady=6)
        tk.Button(frame, text="Purchase", command=self.checkout, width=18).grid(row=2, column=2, pady=6)
        tk.Button(frame, text="Purchase History", command=self.view_history, width=18).grid(row=3, column=1, pady=0)

        self.status_label = tk.Label(self.root, text="", anchor='w')
        self.status_label.pack(fill='x', padx=10, pady=(6,0))

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for p in StoreAPI.get_all_products():
            self.listbox.insert(tk.END, f"{p['id']} | {p['name']} | Price: {p['price']:.2f}€ | In stock: {p['stock']}")

    def add_to_cart(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Choose a product")
            return
            
        idx = sel[0]
        line = self.listbox.get(idx)
        product_id = line.split('|')[0].strip()
        
        try: 
            qty = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Type qty in numbers")
            return
            
        prod = StoreAPI.get_product(product_id)
        if not prod:
            messagebox.showerror("Error", "Product not found")
            return
            
        if qty > prod['stock']:
            messagebox.showerror("Error", "Not enough in storage")
            return
            
        try: 
            self.cart.add(product_id, qty)
            self.status_label.config(text=f"Added: {prod['name']} x{qty}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_cart(self):
        if not self.cart.items:
            messagebox.showinfo("Cart", "Cart is empty")
            return
            
        lines = []
        total_price = 0
        
        for pid, qty in self.cart.items.items():
            p = StoreAPI.get_product(pid)
            if p:
                cost = p['price'] * qty
                total_price += cost
                lines.append(f"{p['name']} x{qty} = {cost:.2f}€")
                
        lines.append(f"In total: {total_price:.2f}€")
        messagebox.showinfo("Cart", "\n".join(lines))
    
    def checkout(self):
        if not self.cart.items:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        try:
            for pid, qty in list(self.cart.items.items()):
                prod = StoreAPI.get_product(pid)
                if prod:
                    StoreAPI.reduce_stock(pid, qty)
                    total_price = prod['price'] * qty
                    StoreAPI.log_purchase(self.current_user, prod['name'], qty, total_price)
                
            self.cart.clear()
            self.update_list()
            self.status_label.config(text="Purchased successfully")
            messagebox.showinfo("Success", "Purchased successfully and DB updated")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unknown error: {e}")

    def view_history(self):
        history = StoreAPI.get_user_history(self.current_user)
        if not history:
            messagebox.showinfo("History", "You haven't purchased anything yet.")
            return
            
        lines = [f"History for {self.current_user}:", "-" * 30]
        for item in history:
            date = item['timestamp'].split('.')[0] 
            lines.append(f"[{date}] {item['product_name']} (x{item['qty']}) - {item['total_price']:.2f}€")
            
        messagebox.showinfo("Purchase History", "\n".join(lines))

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
