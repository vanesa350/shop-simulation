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
import pytest
from models import Cart, Prod, Store
from password_validator import validate_password
from auth_service import AuthService
from models import User

@pytest.mark.parametrize("password, expected", [
    ("Shrt1", False),
    ("nouppercase1", False),
    ("NOLOWERCASE1", False),
    ("NoNumbersHere", False),
    ("ValidPass123", True),
    ("A1b2C3d4", True)
])
def test_validate_password(password, expected):
    assert validate_password(password) == expected

def test_cart_add_and_update():
    cart = Cart()
    cart.add("prod_1", 2)
    assert cart.items["prod_1"] == 2
    cart.add("prod_1", 3)
    assert cart.items["prod_1"] == 5
    cart.upd("prod_1", 10)
    assert cart.items["prod_1"] == 10

def test_cart_add_negative_qty():
    cart = Cart()
    with pytest.raises(ValueError, match="Quantity should be positive"):
        cart.add("prod_1", -1)

def test_cart_remove_and_clear():
    cart = Cart()
    cart.add("prod_1", 2)
    cart.add("prod_2", 1)
    cart.rem("prod_1")
    assert "prod_1" not in cart.items
    assert "prod_2" in cart.items
    cart.clear()
    assert len(cart.items) == 0

def test_cart_total():
    cart = Cart()
    cart.add("1", 2)
    cart.add("2", 1)
    products = {
        "1": Prod("1", "Coffee", 3.50, 10),
        "2": Prod("2", "Tea", 2.00, 30)
    }
    assert cart.total(products) == 9.00

class MockStorage:
    def read_json(self, filepath):
        return [{"id": "1", "name": "Coffee", "price": 3.50, "stock": 5}]
    def write_json(self, filepath, data):
        pass

def test_store_reduce_stock():
    products = {"1": Prod("1", "Coffee", 3.50, 5)}
    store = Store(products, MockStorage())
    store.reduce_stock("1", 2)
    assert store.get_product("1").stock == 3
    with pytest.raises(ValueError, match="Not enough in storage"):
        store.reduce_stock("1", 10)
    with pytest.raises(KeyError, match="Product not found"):
        store.reduce_stock("999", 1)

class MockUserRepository:
    def __init__(self):
        self._users = []
        
    def get_by_username(self, username):
        for u in self._users:
            if u.username == username:
                return u
        return None
        
    def create_user(self, username, password):
        user = User(username=username, password=password)
        self._users.append(user)
        return user

def test_auth_service_register_and_login():
    repo = MockUserRepository()
    auth = AuthService(repo)
    assert auth.register("janis", "StipraParole123") == True
    assert auth.register("peteris", "vaja") == False
    assert auth.register("janis", "CitaParole123") == False
    assert auth.authenticate("janis", "StipraParole123") == True
    assert auth.authenticate("janis", "NepareizaParole") == False
    assert auth.authenticate("nezinams", "StipraParole123") == False
