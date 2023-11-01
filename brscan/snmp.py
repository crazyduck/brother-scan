"""

 Register Host IP to Brother scanner

"""

import time
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902


def add_menu_entry(args):
    """ Announce each menuitem to scanner """
    cmd = ('TYPE=BR;' +
           f'BUTTON={args['button']};' +
           f'USER="{args['user']}";' +
           f'FUNC={args['func']};' +
           f'HOST={args['host']};' +
           f'APPNUM={args['appnum']};' +
           f'DURATION={args['duration']};' +
           f'BRID={args['brid']};')

    # print('Registering:', cmd)
    err_indication, err_status, err_index, var_binds = args['cmd_gen'].setCmd(
        args['authdata'], args['transport_target'],
        ('1.3.6.1.4.1.2435.2.3.9.2.11.1.1.0', rfc1902.OctetString(cmd))
    )
    # See http://www.oidview.com/mibs/2435/BROTHER-MIB.html

    # Check for errors and print out results
    if err_indication:
        print(err_indication)
    else:
        if err_status:
            print(f'{err_status.prettyPrint()} at ' +
                  f'{err_index and var_binds[int(err_index)-1] or '?'}')


def launch(args, config):
    """ main function of submodule snmp, called by brscand """

    menuargs = {}
    menuargs['cmd_gen'] = cmdgen.CommandGenerator()
    menuargs['authdata'] = cmdgen.CommunityData('internal', mpModel=0)
    # SNMP Port 161
    menuargs['transport_target'] = cmdgen.UdpTransportTarget(
                                    (args.scanner_addr, 161))

    adv_addr = (args.advertise_addr, args.advertise_port)

    print(f'Advertising {adv_addr[0]}:{adv_addr[1]} to {args.scanner_addr}')
    for func, users in config['menu'].items():
        for user, entry in users.items():
            print('Entry:', func.upper(), user, entry)
    while 1:
        # Repeat advertising step each 60 seconds
        print('Advertising to scanner')
        appnum = 1
        for func, users in config['menu'].items():
            for user, entry in users.items():
                menuargs['button'] = 'SCAN'
                menuargs['func'] = func.upper()
                menuargs['user'] = user
                menuargs['host'] = f'{adv_addr[0]}:{adv_addr[1]}'
                menuargs['appnum'] = appnum
                menuargs['duration'] = 360
                menuargs['brid'] = ''

                add_menu_entry(menuargs)

                appnum += 1

        time.sleep(60)
