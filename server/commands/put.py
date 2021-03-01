import base64
import json
from os import path

from commands.utils import has_permission

def put(data, login):
    parent = login
    if len(data.get("args")) > 2:
        parent = data.get("args")[2]
        if "../" in parent:
            return "Erreur, le dossier cible n'existe pas"
        if ".directory.json" in data.get("args")[1]:
            return "Erreur, le dossier cible n'existe pas"
        if not path.exists("files/" + parent):
            return "Erreur, le dossier cible n'existe pas"
        with open("files/" + parent + "/.directory.json") as pfile:
            parentproperties = json.load(pfile)
            if not has_permission(parentproperties, login, "c"):
                return "Vous n'avez pas la permission d'écrire ici !"

    if path.exists("files/" + parent + "/" + data.get('file_name')):
        with open("files/" + parent + "/" + data.get('file_name')) as file:
            fileproperties = json.load(file)
            if not has_permission(fileproperties, login, "o"):
                return "Vous n'avez pas la permission de réécrire ce fichier !"

    defaultpermissions = {login: {
        "c": "false",
        "l": "true",
        "d": "true",
        "r": "false",
        "o": "false"
    }}
    file = {
        "content": base64.b64encode(data.get('serialized_file')).decode(),
        "parent": parent,
        "owner": login,
        "permissions": defaultpermissions
    }
    with open("files/" + parent + "/" + data.get('file_name'), "w") as outfile:
        json.dump(file, outfile)

    return "Fichier reçu et enregistré."
