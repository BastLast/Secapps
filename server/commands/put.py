import base64
import json


def put(data, login):
    defaultpermissions = {login: {
        "c": "false",
        "l": "true",
        "d": "true",
        "r": "false",
        "o": "false"
    }}
    file = {
        "content": base64.b64encode(data.get('serialized_file')).decode(),
        "parent": login,
        "owner": login,
        "permissions": defaultpermissions
    }
    print(file)
    with open("files/" + login + "/" + data.get('file_name') + ".json", "w") as outfile:
        json.dump(file, outfile)

    with open("files/" + login + "/" + data.get('file_name') + ".json", "r") as outfile:
        datade = json.load(outfile)

    f = open("files/" + login + "/" + data.get('file_name'), 'wb')
    f.write(base64.b64decode(datade.get("content").encode()))
    f.close()
    return "fichier recu et enregistré"
