#Functions used by multiple commands
import json

def is_owner(file,user):
    return file.get("owner") == user

def is_admin(user):
    with open("users.json", "r") as users_file:
        users = json.load(users_file)
    return users.get(user).get("admin")

def has_permission(file,user,permission):
    if is_owner(file,user):
        return True
    if is_admin(user) and permission == 'l':
        return True
    user_perm=file.get('permissions').get(user)
    if not user_perm:
        return False
    return user_perm.get(permission)