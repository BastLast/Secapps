import yaml


def put(args):
    server_instruction = ""
    with open(args[1], 'rb') as stream:
        try:
            data = {
                'args': args,
                'serialized_file': stream.read()
            }
            server_instruction = yaml.dump(data).encode("UTF-8")
        except yaml.YAMLError as exc:
            print("error : " + exc)

    # faire le chiffrement du message ici :

    return server_instruction
