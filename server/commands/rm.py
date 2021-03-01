import json
import os
from commands.utils import has_permission

def rm(data,user):
    args = data.get('args')

    if len(args) != 2:
        return "Error: Incorrect syntax.\nUsage: rm <file>"
    #os.path.basename(args[1])
    if ".directory.json" in args[1]:
        return "Error: No such file."

    if "/" not in args[1]:
        args[1] = user + "/" + args[1]

    if "../" in args[1]:
        return "Error: Error: No such file."

    if not os.path.exists("files/" + args[1]):
        return "Error: Error: No such file."

    with open("files/"+args[1]) as file:
        fileprop=json.load(file)

    if not has_permission(fileprop, user, "r"):
        return "Error: Permission denied."

    os.remove("files/"+args[1])
    return "Successfully removed "+args[1]