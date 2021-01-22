import socket

from .scanto import scanto


def launch(args, config):
    addr = (args.bind_addr, args.bind_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(addr)
    print("Listening on %s:%d" % (addr))

    while(1):
        data, addr = server_socket.recvfrom(2048)
        print("Got UDP packet: %d bytes from %s:%s" % (
            len(data), addr[0], addr[1]))
        if len(data) < 4 or data[0] != 2 or data[1] != 0 or data[3] != 0x30:
            print('Error: dropping unknown UDP data: %d bytes' % (len(data)))
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
