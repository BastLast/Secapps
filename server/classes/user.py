class User:
    login = ""
    password = ""
    id = 0
    pseudo = ""
    admin = False
    pub_key = ""
    pseudo_id = ""

    '''Init principal'''
    def __init__(self, login, password, id, pseudo, admin, pub_key):
        self.login = login
        self.password = password
        self.id = id
        self.pseudo = pseudo
        self.admin = admin
        self.pub_key = pub_key
        self.pair = self.pseudo + "@" + self.id
