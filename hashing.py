import bcrypt
#generation of the password hash
def generate_hash(psw):
    psw_byte=psw.encode("utf-8")
    salt=bcrypt.gensalt(rounds=10)
    hashed=bcrypt.hashpw(psw_byte,salt)
    return hashed.decode("utf-8")
#checking if password == to the hash stored
def is_valid_hash(psw,hashed):
    hash_=hashed.encode("utf-8")
    psw_bytes=psw.encode("utf-8")
    is_valid=bcrypt.checkpw(psw_bytes,hash_)
    return is_valid