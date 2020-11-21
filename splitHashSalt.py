import hashlib

class splitHashSalt:
    def __init__(self, client_id, salt='salt'):
        self.salt = salt
        self.client_id = client_id
        self.hash_value = None
    def create_hashed_value(self):
        client_id_salt_str = str(self.client_id) + self.salt
        tmp_hash = hashlib.md5(client_id_salt_str.encode('ascii')).hexdigest()
        self.hash_value = int(tmp_hash[:6], 16)/0xFFFFFF