class User:
    def __init__(self, id, name, lastname, rol, nick, password):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.rol = rol
        self.nick = nick
        self.password = password

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_lastname(self):
        return self.lastname

    def get_rol(self):
        return self.rol

    def get_nick(self):
        return self.nick

    def get_password(self):
        return self.password
