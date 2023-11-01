"""
Submodule of brscand
handles the listen process which will be called from scanner
"""
import socket
# import subprocess

from .scanto import scanto


def launch(args, config):
    """ Endless listen function """
    addr = (args.bind_addr, args.bind_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(addr)
    print(f'Listening on {addr[0]}:{addr[1]}')

    while 1:
        data, addr = server_socket.recvfrom(2048)
        print(f'Got UDP packet: {len(data)} bytes from {addr[0]}:{addr[1]}')

        if len(data) < 4 or data[0] != 2 or data[1] != 0 or data[3] != 0x30:
            print(f'Error: dropping unknown UDP data: {len(data)} bytes')
            continue

        msg = data[4:].decode('utf-8')
        print('Received:', msg)
        msgd = {}
        for item in msg.split(';'):
            if not item:
                continue
            name, value = item.split('=')
            if name == 'USER':
                value = value[1:-1]
            msgd[name] = value
        for menu_func, menu_users in config['menu'].items():
            for menu_user, menu_entry in menu_users.items():
                menu_func = menu_func.upper()
                if msgd['FUNC'] == menu_func and msgd['USER'] == menu_user:
                    scanto(msgd['FUNC'], menu_entry)
                    break
        server_socket.recvfrom(len(data))
