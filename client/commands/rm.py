import yaml


def rm(args):
    data = {
        'args': args
    }

    server_instruction = yaml.safe_dump(data).encode("UTF-8")
    # faire le chiffrement du message ici :

    return server_instruction
