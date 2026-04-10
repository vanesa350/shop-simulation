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
import userdata

class UserRepository:
    def __init__(self):
        try:
            self._users = userdata.load_users()
        except Exception:
            self._users = []

    def _persist(self):
        try:
            userdata.save_users(self._users)
        except Exception:
            pass

    def get_by_username(self, username: str):
        for u in self._users:
            if getattr(u, "username", None) == username:
                return u
        return None

    def create_user(self, username: str, password: str):
        from models import User
        user = User(username=username, password=password)
        self._users.append(user)
        self._persist()
        return user