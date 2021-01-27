import yaml


def put(args):
    file = open(args[1])
    serialized_file = yaml.safe_dump(file).encode("UTF-8")

    server_instruction = "PUT" + serialized_file
    # faire le chiffrement du message ici :

    return
