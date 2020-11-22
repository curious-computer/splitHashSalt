import hashlib
import numpy
import pandas

class splitHashSalt:
    '''This module can be used to create hash values for a unique identifier based on a salt.
    
    This module is useful to randomly assign an entity/list of entities to multiple groups,
    the same way every single time. (AB testing or ABN testing)
    
    The salt value along with the unique identifier will make sure the split is pseudo randomized.
    This has advantages over setting a seed and splitting based on the list of random generated numbers.
    For a list of entities, the assignemnt is dependent on the order of the list.
    If the list is shuffled, then the group assignments (A or B or .. N) can change.
    
    client = splitHashSalt(client_id=unique_identifier, salt='salt')
    client.create_hashed_value()
    
    client_id: object of type int, float, str, list, pandas Series, numpy array
    salt: string that make the split of a list of clients unique
    '''
    def __init__(self, client_id, salt='salt'):
        self.salt = salt
        self.client_id = client_id
        self.hash_value = None

    def create_hashed_value(self):
        if isinstance(self.client_id, (str, int, float)):
            client_id_salt_str = str(self.client_id) + self.salt
            tmp_hash = hashlib.md5(client_id_salt_str.encode('ascii')).hexdigest()
            self.hash_value = int(tmp_hash[:6], 16)/0xFFFFFF
        elif isinstance(self.client_id, (list, numpy.ndarray, pandas.core.series.Series)):
            self.hash_value = []
            for i in self.client_id:
                client_id_salt_str = str(i) + self.salt
                tmp_hash = hashlib.md5(client_id_salt_str.encode('ascii')).hexdigest()
                self.hash_value.append(int(tmp_hash[:6], 16)/0xFFFFFF)

    def get_group_assignments(self, splits=2):
        if isinstance(self.client_id, (str, int, float)):
            return int(self.hash_value/(1/splits)) + 1
        elif isinstance(self.client_id, (list, numpy.ndarray, pandas.core.series.Series)):
            self.group_assignments = []
            for i in self.hash_value:
                self.group_assignments.append(int(i/(1/splits)) + 1)
            return self.group_assignments