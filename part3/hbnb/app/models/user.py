from .BaseModel import BaseModel
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    # Defining class attributes here ensures they exist on the instance
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    
    def __init__(self, *args, **kwargs):
        """
        Initializes User object, leveraging BaseModel for ID/timestamps,
        and setting attributes from kwargs if provided (e.g., deserialization).
        """
        super().__init__(*args, **kwargs)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def validate(self):
        # Validation checks
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

        # Password validation removed

    def save(self):
        self.validate()
        
        # Password hashing logic removed
        
        # Mise à jour de updated_at
        super().save()
        
    # check_password method removed

    def update(self, data):
        # Update attributes directly
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.validate()
        super().save()