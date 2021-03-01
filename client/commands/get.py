import yaml


def get(args):

    data = {
        'args': args
    }

    server_instruction = yaml.safe_dump(data).encode("UTF-8")

    return server_instruction

"""    f = open("files/" + parent + "/" + data.get('file_name'), 'wb')
        f.write(base64.b64decode(datade.get("content").encode()))
        f.close()"""