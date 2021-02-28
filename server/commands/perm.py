import json
import os
from commands.utils import has_permission
from commands.utils import is_owner
from commands.utils import is_admin


def setPermission(user, addrem, permissions, filename):
    with open("files/" + filename) as file:
        fileproperties = json.load(file)

    currentperm = fileproperties.get("permissions")
    if not currentperm.get(user):
        currentperm[user] = {
            "c": False,
            "l": False,
            "d": False,
            "r": False,
            "o": False
        }

    for p in permissions:
        currentperm[user][p] = addrem

    fileproperties["permissions"] = currentperm

    with open("files/" + filename, "w") as file:
        json.dump(fileproperties, file)

    return "Successfully set permissions."


def perm(data, user):
    args = data.get('args')

    if len(args) != 5:
        return "Error: Incorrect syntax.\nUsage: perm <user> <add|remove> <c|l|d|r|o> <directory|filename>"

    addrem = 0
    if args[2] == "add":
        addrem = True
    elif args[2] == "remove":
        addrem = False
    else:
        return "Error: Invalid argument."

    for p in args[3]:
        if p not in "cldro":
            return "Error: Invalid argument."

    if ".directory.json" in args[4]:
        return "Error: No such file or directory."

    with open("users.json", "r") as users_file:
        users = json.load(users_file)

    if not users.get(args[1]):
        return "Error: This user does not exist."

    if users.get(args[4]):
        with open("files/" + user + "/.directory.json") as parent:
            parentproperties = json.load(parent)
        if is_admin(user) and not is_owner(parentproperties, user) and is_admin(args[1]):
            return "Error: Cannot give permissions to an admin on a file you don't own."
        if not is_admin(user):
            for p in args[3]:

                if not has_permission(parentproperties, user, p):
                    return "Error: You can't change a permission you don't have."

        return setPermission(args[1], addrem, args[3], args[4] + "/.directory.json")

    if "/" not in args[4]:
        args[4] = user + "/" + args[4]

    if not os.path.exists("files/" + args[4]):
        return "Error: Error: No such file or directory."

    with open("files/" + args[4]) as file:
        fileproperties = json.load(file)
    if is_admin(user) and not is_owner(fileproperties, user) and is_admin(args[1]):
        return "Error: Cannot give permissions to an admin on a file you don't own."
    if not is_admin(user):
        for p in args[3]:
            if not has_permission(fileproperties, user, p):
                return "Error: You can't change a permission you don't have."

    return setPermission(args[1], addrem, args[3], args[4])
