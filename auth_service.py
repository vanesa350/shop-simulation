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
from user_repository import UserRepository
from password_validator import validate_password

class AuthService:
    def __init__(self, repo: UserRepository = None):
        self.repo = repo or UserRepository()

    def authenticate(self, username: str, password: str) -> bool:
        user = self.repo.get_by_username(username)
        if not user:
            return False
        return getattr(user, "password", None) == password

    def register(self, username: str, password: str) -> bool:
        if not validate_password(password):
            return False
        if self.repo.get_by_username(username):
            return False
        self.repo.create_user(username, password)
        return True