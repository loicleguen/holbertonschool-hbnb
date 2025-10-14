from .BaseModel import BaseModel, datetime
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    def __init__(self, id: str, first_name: str, last_name: str, email: str, is_admin: bool, created_at: datetime, updated_at: datetime):
        super().__init__()
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.created_at = created_at
        self.updated_at = updated_at
        self.user = []  # List to store related places


    @property
    def validate(self):
        if not isinstance(self.id, str):
            raise TypeError("id must be a string")
        if len(self.id) < 1:
            raise ValueError("id must be > 0")
        if not isinstance(self.first_name, str):
            raise TypeError("first_name must be a string")
        if len(self.first_name) < 1:
            raise ValueError("first_name mustn't empty")
        if len(self.first_name) > 50:
            raise ValueError("first_name must be less than 50 characters")
        if not isinstance(self.last_name, str):
            raise TypeError("first_name must be a string")
        if len(self.last_name) < 1:
            raise ValueError("last_name mustn't empty")
        if len(self.last_name) > 50:
            raise ValueError("first_name must be less than 50 characters")
        if not isinstance(self.is_admin, bool):
            raise TypeError("is_admin must be a boolean")
        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")
        if not isinstance(self.updated_at, datetime):
            raise TypeError("updated_at must be a datetime")

        self.email = email
        try:
            emailinfo = validate_email(self.email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            print(str(e))
