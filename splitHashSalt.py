import hashlib
import numpy
import pandas
import math

class splitHashSalt:
    def __init__(self, client_id, salt='salt'):
        """
        Randomly assign an entity/list of entities to multiple groups,
        the same way every single time. (AB testing or ABN testing)
        
        For a list of entities, the assignemnt is dependent on the order of the list.
        If the list is shuffled, then the group assignments (A or B or .. N) can change.

        Args:
            client_id: (int, float, str, pandas series, numpy array)
                entity or list of entities that needs to be pseudo randomly assigned
            salt: unique salt value for hashing
        """
        self.salt = salt
        self.client_id = client_id
        
        # Create the list of hash values based on salt specified.
        if isinstance(self.client_id, (str, int, float)):
            client_id_salt_str = str(self.client_id) + self.salt
            tmp_hash = hashlib.md5(client_id_salt_str.encode('ascii')).hexdigest()
            self.hash_value = int(tmp_hash[:4], 16)/0xFFFF
        elif isinstance(self.client_id, (list, numpy.ndarray, pandas.core.series.Series)):
            self.hash_value = []
            for i in self.client_id:
                client_id_salt_str = str(i) + self.salt
                tmp_hash = hashlib.md5(client_id_salt_str.encode('ascii')).hexdigest()
                self.hash_value.append(int(tmp_hash[:4], 16))
    def get_group_assignments(self, splits=2):
        """
        Get the group assignments for the unique identifiers based on the hash value created

        Args:
            splits (int): Number of splits needed - e.g. AB tests has 2 splits.
        """
        if isinstance(self.client_id, (str, int, float)):
            return math.ceil((self.hash_value + 1)/((0xFFFF + 1)/splits))
        elif isinstance(self.client_id, (list, numpy.ndarray, pandas.core.series.Series)):
            self.group_assignments = []
            for i in self.hash_value:
                self.group_assignments.append(math.ceil((i + 1)/((0xFFFF + 1)/splits)))
            return self.group_assignments