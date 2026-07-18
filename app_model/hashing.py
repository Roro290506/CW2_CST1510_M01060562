import bcrypt
#generation of the password hash
def generate_hash(psw):
    psw_byte=psw.encode("utf-8")
    salt=bcrypt.gensalt(rounds=10)
    hashed=bcrypt.hashpw(psw_byte,salt)
    return hashed.decode("utf-8")
#checking if password == to the hash stored
def is_valid_hash(psw,hashed):
    try:
        #checking if its not falsy string
        if not psw or not hashed:
            return False
        hash_=hashed.encode("utf-8")
        psw_bytes=psw.encode("utf-8")
        return bcrypt.checkpw(psw_bytes,hash_)
    except Exception as e:
        return False