import yaml


def rm(args):
    data = {
        'args': args
    }

    server_instruction = yaml.safe_dump(data).encode("UTF-8")

    return server_instruction
