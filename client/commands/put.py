import yaml


def put(args):
    file = open(args[1], "rb")
    serialized_file = yaml.safe_dump(file)

    data = {
        'args': args,
        'serialized_file': serialized_file
    }

    server_instruction = yaml.safe_dump(data).encode("UTF-8")
    # faire le chiffrement du message ici :

    return server_instruction
