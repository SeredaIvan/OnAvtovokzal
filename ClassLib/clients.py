class Clients:
    def __init__(self):
        self.id_client = None
        self.name = None
        self.phone = None
        self.email = None
        self.password = None
        self.role_client = None

    def to_dict(self):
        return {
            'id': self.id_client,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'role_client': self.role_client
        }

    @classmethod
    def from_dict(cls, user_dict):
        user = cls()
        user.id_client = user_dict.get('id_client', '')
        user.name = user_dict.get('name', '')
        user.email = user_dict.get('email', '')
        user.phone = user_dict.get('phone', '')
        user.password = user_dict.get('password', '')
        user.role_client = user_dict.get('role_client', '')
        return user