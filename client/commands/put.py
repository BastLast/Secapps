import yaml


def put(args):
    server_instruction = ""
    with open(args[1], 'rb') as stream:
        try:
            data = {
                'args': args,
                'serialized_file': stream.read(),
                'file_name': stream.name
            }
            server_instruction = yaml.safe_dump(data).encode("utf-8")
            #print(yaml.safe_load(server_instruction))
        except yaml.YAMLError as exc:
            print("error : " + exc)

    # faire le chiffrement du message ici :

    return server_instruction
