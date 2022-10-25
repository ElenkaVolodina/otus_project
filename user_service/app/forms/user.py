from typing import List

from fastapi import Request


class UserCreateForm:

    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.form = None

    async def load_data(self):
        self.form = await self.request.form()

    def is_valid(self):
        if self.form.get('password') and self.form.get('password') != self.form.get('password1'):
            self.errors.append("Password not equal")
        if not self.errors:
            return True
        return False
