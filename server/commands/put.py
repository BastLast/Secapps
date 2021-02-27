def put(data):
    f = open("temp/" + data.get('file_name'), 'wb')
    f.write(data.get('serialized_file'))
    f.close()
    return "fichier recu et enregistré"