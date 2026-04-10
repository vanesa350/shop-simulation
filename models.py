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
from dataclasses import dataclass, asdict #imp dataclass un asdict 
from typing import Dict, Any #imp anotacijas Dict un Any

@dataclass #dataclass dekorators
class Prod: #saisinats Product nosauk
    id: str #prod id lauks
    name: str #prod nosauk
    price: float #prod cena
    stock: int #prod noliktavas daudzums

    @classmethod #klases metode dekorators
    def from_d(cls, d: Dict[str, Any]): #saisinata from_dict 
        return cls( #prod ins no dict
            id=str(d['id']), #id no dict konvertets uz string
            name=d['name'], #name no dict
            price=float(d['price']), #price no dict uz float
            stock=int(d['stock']) #stock no dict uz int
        )

    def to_d(self) -> Dict[str, Any]: #saisinata to_dict
        return asdict(self) #atgriez dataklases laukus dict

class Cart: #groza klase
    def __init__(self): #konstr
        #items (prod_id uz qty)
        self.items: Dict[str, int] = {} #inic items dict

    def add(self, prod_id: str, qty: int): #pievieno daudzumu grozam
        if qty <= 0: #ja daudzums nav pozitivs
            raise ValueError("Quantity should be positive") #izmet ValueError
        self.items[prod_id] = self.items.get(prod_id, 0) + qty #palielina vai pievieno ierakstu

    def rem(self, prod_id: str): #iznem produktu no groza
        if prod_id in self.items: #ja produkts ir groza
            del self.items[prod_id] #dzest ierakstu no dict

    def upd(self, prod_id: str, qty: int): #uzstada jaunu daudzumu vai iznem
        if qty <= 0: #ja daudzums nav pozitivs
            self.rem(prod_id) #iznem produktu no groza
        else:
            self.items[prod_id] = qty #uzstada noradito daudzumu

    def clear(self): #iztira grozu pilnigi
        self.items.clear() #izdzest visus ierakstus
    def total(self, products: Dict[str, Prod]) -> float: #aprekina groza kopsummu
        total = 0.0 #inic total mainigo
        for pid, qty in self.items.items(): #iziet cauri groza ierakstiem
            prod = products.get(pid) #iegust produktu no products dict
            if prod: #ja produkts eksiste
                total += prod.price * qty #pieskaita cena * daudzums
        return total #atgriez aprek summu

class Store: #veikala klase
    def __init__(self, prods: Dict[str, Prod], stor): #konstruktors ar produktiem un storage handler
        #prods (id uz Prod)
        self.products = prods #saglaba produktus
        self.stor = stor #saglaba storage handler objektu

    @classmethod #klases metode dekorators
    def load_from_file(cls, enc_filepath: str, stor): #nolasa produktus no faila
        raw = stor.read_json(enc_filepath) #nolasa json datus no faila ar stor
        products = {str(p['id']): Prod.from_d(p) for p in raw} #konstr Prod objektus no raw saraksta
        return cls(products, stor) #atgriez Store instanci ar produktiem un stor

    def save_file(self, enc_filepath: str): #saglaba produktus faila
        data = [p.to_d() for p in self.products.values()] #konv produktus uz dict sarakstu
        self.stor.write_json(enc_filepath, data) #ieraksta json faila ar stor

    def get_product(self, prod_id: str) -> Prod: #atgriez produktu pec id
        return self.products.get(prod_id) #atgriez produktu vai None ja nav

    def list_products(self): #atgriez visu produktu sarakstu
        return list(self.products.values()) #konv dict values uz listu

    def reduce_stock(self, prod_id: str, qty: int): #samazina produkta noliktavas daudzumu
        prod = self.get_product(prod_id) #iegust produktu
        if not prod: #ja produkts nav atrasts
            raise KeyError("Product not found") #izmet KeyError ar ziņu
        if qty > prod.stock: #ja qty lielaks par stock
            raise ValueError("Not enough in storage") #izmet ValueError ar ziņu
        prod.stock -= qty #samazina stock par qty

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
