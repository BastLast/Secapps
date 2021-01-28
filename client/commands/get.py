import yaml


def get(args):

    data = {
        'args': args
    }

    """ print(receiveddoc)
    f = open("test.png", 'wb')
    f.write(receiveddoc.get('serialized_file'))
    f.close()
    """

    server_instruction = yaml.safe_dump(data).encode("UTF-8")
    # faire le chiffrement du message ici :

    return server_instruction
