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
        with open("files/" + parent + "/" + data.get('file_name') + ".json", "r") as outfile:
            datade = json.load(outfile)

        # write the file in a file that will be sent
        try:
            result = yaml.safe_dump(datade).encode("utf-8")
        except yaml.YAMLError as exc:
            print("error : " + exc)
        return result
    except:
        print("Le fichier n'a pas été trouvé")
        return "error"
    return
