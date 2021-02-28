import yaml
import os


def put(args):
    server_instruction = ""
    try:
        with open(args[1], 'rb') as stream:
            try:
                data = {
                    'args': args,
                    'serialized_file': stream.read(),
                    'file_name': os.path.basename(stream.name)
                }
                server_instruction = yaml.safe_dump(data).encode("utf-8")

            except yaml.YAMLError as exc:
                print("error : " + exc)
    except:
        print("Le fichier n'a pas été trouvé")
        return "error"

    return server_instruction
