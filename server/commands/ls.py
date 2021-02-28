import json
import os

from commands.utils import has_permission
from commands.utils import is_owner
from commands.utils import is_admin


def file_to_string(filename, fileproperties, user):

    if is_owner(fileproperties, user):
        if ".directory.json" in filename:
            return "cldro | ./"
        return "cldro | " + filename
    if is_admin(user):
        if ".directory.json" in filename:
            return "-l-r- | ./"
        return "-l-r- | " + filename
    txt = ""
    permissions = fileproperties.get("permissions").get(user)
    for pname, pvalue in permissions.items():
        if pvalue:
            txt += pname
        else:
            txt += "-"
    if ".directory.json" in filename:
        return txt + " | ./"
    return txt + " | " + filename


def get_files_from_parent(parent, user):
    show_files = ""
    with open("files/" + parent + "/.directory.json") as pfile:
        parentproperties = json.load(pfile)
    for filename in os.listdir("files/" + parent):
        fn = parent + "/" + filename
        with open("files/" + fn) as file:
            fileproperties = json.load(file);
        if has_permission(fileproperties, user, "l") or has_permission(parentproperties, user, "l"):
            fileperm=file_to_string(filename, fileproperties, user)
            show_files += fileperm + "\n"
    return show_files


def ls(data,user):
    args = data.get('args')

    if len(args) > 2:
        return "Error: Incorrect syntax.\nUsage: ls [directory|file]"

    if len(args) == 1:
        return get_files_from_parent(user, user)

    with open("users.json", "r") as users_file:
        users = json.load(users_file)

    if ".directory.json" in args[1]:
        return "Error: No such file or directory."

    if users.get(args[1]):
        return get_files_from_parent(args[1], user)

    if "/" not in args[1]:
        args[1] = user + "/" + args[1]

    if not os.path.exists("files/" + args[1]):
        return "Error: Error: No such file or directory."

    with open("files/" + args[1]) as file:
        fileproperties = json.load(file)

    if has_permission(fileproperties, user, "l"):
        return file_to_string(args[1], fileproperties, user)

    return "Error: Permission denied."
