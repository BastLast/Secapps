import base64
import json
import yaml
from os import path

from commands.utils import has_permission


def get(data, login):
    parent = login

    # check permissions
    if len(data.get("args")) > 2:
        parent = data.get("args")[2]
        if not path.exists("files/" + parent):
            return "Erreur, le dossier cible n'existe pas"
        with open("files/" + parent + "/.directory.json") as pfile:
            parentproperties = json.load(pfile)
            if not has_permission(parentproperties, login, "r"):
                return "Vous n'avez pas la permission de lire ici !"

    # load the file
    try:
        with open("files/" + parent + "/" + data.get("args")[1], "r") as outfile:
            datade = json.load(outfile)
            content = base64.b64decode(datade["content"].encode())
            try:
                data3 = {
                    'content' : content,
                    'file_name': data.get("args")[1]
                }
                server_instruction = yaml.safe_dump(data3)
            except yaml.YAMLError as exc:
                print("error : " + exc)
    except:
        print("Le fichier n'a pas été trouvé")
        return "error"
    return server_instruction
