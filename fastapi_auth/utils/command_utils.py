import secrets
from fastapi_auth.consts import CommandConsts


def generate_code():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(secrets.choice(chars) for _ in range(22))


def parse_sub_commands(sub_commands: list[str], command: str) -> list[str]:
    result = []
    for sub_command in sub_commands:
        if "--" in sub_command and sub_command not in CommandConsts.COMMANDS[command]:
            raise ValueError(f"Command {sub_command} does not exists")
        result.append(sub_command)
    return result


def execute_from_line(args: list):
    if len(args) < 2:
        raise ValueError("Too few arguments.")
    command = args[1]
    if command not in CommandConsts.COMMANDS.keys():
        raise ValueError(f"Command {command} does not exists")
    sub_commands = parse_sub_commands(args[2:], command)
    if command == "--generate-key":
        if len(sub_commands) > 0:
            if sub_commands[0] == "--help":
                print("Function will return secret key to be used as a SECRET_KEY settings.py value.")
            else:
                raise ValueError(f"Unknown sub-commands {sub_commands}")
        else:
            print(generate_code())
