def put(data, login):
    f = open("files/" + login + "/" + data.get('file_name'), 'wb')
    f.write(data.get('serialized_file'))
    f.close()
    return "fichier recu et enregistré"
