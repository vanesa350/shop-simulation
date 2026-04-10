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
from auth_service import AuthService
from user_repository import UserRepository

class LoginWindow:
    def __init__(self, on_success=None, master=None):
        self.repo = UserRepository()
        self.auth = AuthService(self.repo)
        self.on_success = on_success

        if master is None:
            self.root = tk.Toplevel()
        else:
            self.root = tk.Toplevel(master)
        self.root.title("Login")
        self.root.geometry("320x180")
        tk.Label(self.root, text="Username").pack(pady=(10,0))
        self.username = tk.Entry(self.root)
        self.username.pack(fill="x", padx=20)
        tk.Label(self.root, text="Password").pack(pady=(10,0))
        self.password = tk.Entry(self.root, show="*")
        self.password.pack(fill="x", padx=20)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=(12,0))
        tk.Button(btn_frame, text="Login", width=12, command=self.try_login).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Register", width=12, command=self.try_register).grid(row=0, column=1, padx=6)

    def try_login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            messagebox.showwarning("Warning", "Enter username and password")
            return
        if self.auth.authenticate(u, p):
            messagebox.showinfo("OK", "Login successful")
            if self.on_success:
                self.on_success(u)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def try_register(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            messagebox.showwarning("Warning", "Enter username and password")
            return
        if self.auth.register(u, p):
            messagebox.showinfo("OK", "Registered and logged in")
            if self.on_success:
                self.on_success(u)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Registration failed (weak password or user exists)")

def show_login(on_success=None, master=None):
    LoginWindow(on_success=on_success, master=master)