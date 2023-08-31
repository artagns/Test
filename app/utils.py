from passlib.context import CryptContext

class Password :
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password) :
        return cls.pwd_context.hash(password)
    
    @classmethod
    def validate_password(cls, password, hashed_password) :
        # you can't do this, because bcrypt produces different hashes even for the 
        # same text each time 
        # return True if cls.get_password_hash(password)==hashed_password else False
        return cls.pwd_context.verify(password, hashed_password)