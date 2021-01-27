class Folder():
    id = 0
    nom = ""
    list_user = []

    '''Init principal'''
    def __init__(self, id, nom, list):
        self.id = id
        self.nom = nom
        self.list_user = list

    def add_user_to_list(self, user):
        self.list_user.append(user)