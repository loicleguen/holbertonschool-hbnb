from app.models.BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
import bcrypt

class User(BaseModel):
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def validate(self):
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name must be a non-empty string")
        if len(self.first_name) > 50:
            raise ValueError("first_name must be less than 50 characters")

        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name must be a non-empty string")
        if len(self.last_name) > 50:
            raise ValueError("last_name must be less than 50 characters")

        try:
            emailinfo = validate_email(self.email, check_deliverability=False)
            self.email = emailinfo.normalized
        except EmailNotValidError as e:
            raise ValueError(str(e))

        if not isinstance(self.password, str):
            raise TypeError("password must be a string")
        if len(self.password) < 6:
            raise ValueError("password must be at least 6 characters long")

    def save(self):
        self.validate()
        if self.password and not self.password.startswith("$2b$"):
            self.password = bcrypt.hash(self.password)
        super().save()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate()
        super().save()
