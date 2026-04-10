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
from cryptography.fernet import Fernet #atslega imports
import json #json imports
from typing import Any #tipu anotacija
import os #os imports

class StorageHandler: #klase kas apstrada atslegu un failus
    def __init__(self, keyfile: str): #konstruktors ar atslegas faila celu
        self.keyfile = keyfile #saglaba atslegas faila celu
        self.key = self._load_or_create_key() #ielade vai izveido atslegu

    def _load_or_create_key(self) -> bytes: #ielade vai izveide atslegas baitiem
        #atslega eksiste-nolasa, neeksiste-izveido jaunu
        if os.path.exists(self.keyfile): #parbauda vai atslegas fails eksiste
            with open(self.keyfile, 'rb') as f: #atver failu lasisanai binari
                return f.read() #nolasa atslegas baitus un atgriez
        else: #ja fails neeksiste
            key = Fernet.generate_key() #generē jaunu fernet atslegu
            #lai mape eksiste
            os.makedirs(os.path.dirname(self.keyfile), exist_ok=True) #izveido mapes celu ja vajadzigs
            with open(self.keyfile, 'wb') as f: #atver failu rakstisanai binari
                f.write(key) #ieraksta genereto atslegu faila
            return key #atgriez jauno atslegu

    def read_json(self, enc_filepath: str): #nolasa sifretu json failu un atgriez objektu
        fernet = Fernet(self.key) #izveido fernet objektu ar atslegu
        with open(enc_filepath, 'rb') as f: #atver sifreto failu lasisanai binari
            encrypted = f.read() #nolasa sifretos baitus
        decrypted = fernet.decrypt(encrypted) #atsifre datus ar fernet
        return json.loads(decrypted.decode('utf-8')) #dekode utf-8 un parse json

    def write_json(self, enc_filepath: str, data: Any): #sifre un ieraksta json faila
        fernet = Fernet(self.key) #izveido fernet objektu ar atslegu
        raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8') #serialize datus uz utf-8 baitiem
        encrypted = fernet.encrypt(raw) #sifre serialize baitu saturu
        os.makedirs(os.path.dirname(enc_filepath), exist_ok=True) #izveido mapes celu ja vajadzigs
        with open(enc_filepath, 'wb') as f: #atver failu rakstisanai binari
            f.write(encrypted) #ieraksta sifreto faila