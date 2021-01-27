class File:
    name = ""
    owner = ""
    path = ""
    list_user = []
    '''List must be filled with item type dictionary of key/value'''
    '''key of dictionary : pseudo@id, dl, send, delete, create, replace'''
    '''value of dictionary : string, bool, bool, bool, bool, bool'''

    '''Init principal'''
    def __init__(self, name, owner, path, list):
        self.name = name
        self.owner = owner
        self.path = path
        self.list_user = list

    def add_user_to_list(self, user):
        self.list_user.append(user)