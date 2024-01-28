from fastapi_auth.utils import execute_from_line
import sys


def main():
    print(sys.argv, "args")
    execute_from_line(sys.argv)


main()
