import json
from commands.utils import has_permission
from commands.utils import is_owner
from commands.utils import is_admin


def file_to_string(filename, fileproperties, user):
    if is_owner(fileproperties, user):
        return "cldro " + filename
    if is_admin(user):
        return "-l-r- | " + filename
    txt = ""
    permissions = fileproperties.get("permissions").get(user)
    for pname, pvalue in permissions.items():
        if pvalue:
            txt += pname
        else:
            txt += "-"
    return txt + " | " + filename


def get_files_from_parent(files, parent, user):
    show_files = ""
    for filename, fileproperties in files.items():
        if fileproperties.get('parent') == parent and (
                has_permission(fileproperties, user, "l") or has_permission(files.get(parent), user, "l")):
            show_files += file_to_string(filename, fileproperties, user) + "\n"
    return show_files


def ls(data):
    with open("files/files.json", "r") as read_files:
        files = json.load(read_files)
    args = data.get('args')
    user = data.get('user')

    if len(args) > 2:
        return "Error: Incorrect syntax.\nUsage: ls [directory|file]"

    if len(args) == 1:
        return get_files_from_parent(files, user, user)

    f = files.get(args[1])
    if not f:
        return "Error: Error: No such file or directory."

    if f.get('parent') == "":
        return get_files_from_parent(files, f.get('parent'), user)

    if has_permission(f, user, "l"):
        return file_to_string(args[1], f, user)

    return "Error: Permission denied."
