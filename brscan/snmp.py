"""

 Register Host IP to Brother scanner

"""

import time
import functools
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

# activate flush option in print cmd to see it in docker logs
myprint = functools.partial(print, flush=True)


def add_menu_entry(args):
    """ Announce each menuitem to scanner """
    cmd = ('TYPE=BR;' +
           f'BUTTON={args["button"]};' +
           f'USER="{args["user"]}";' +
           f'FUNC={args["func"]};' +
           f'HOST={args["host"]};' +
           f'APPNUM={args["appnum"]};' +
           f'DURATION={args["duration"]};' +
           f'BRID={args["brid"]};')

    # myprint('Registering:', cmd)
    err_indication, err_status, err_index, var_binds = args['cmd_gen'].setCmd(
        args['authdata'], args['transport_target'],
        ('1.3.6.1.4.1.2435.2.3.9.2.11.1.1.0', rfc1902.OctetString(cmd))
    )
    # See http://www.oidview.com/mibs/2435/BROTHER-MIB.html

    # Check for errors and print out results
    if err_indication:
        myprint(err_indication)
    else:
        if err_status:
            myprint(f'{err_status.myprettyPrint()} at ' +
                    f'{err_index and var_binds[int(err_index)-1] or "?"}')


def launch_advertiser(args, config):
    """ main function of submodule snmp, called by brscand """

    menuargs = {}
    menuargs['cmd_gen'] = cmdgen.CommandGenerator()
    menuargs['authdata'] = cmdgen.CommunityData('internal', mpModel=0)
    # SNMP Port 161
    menuargs['transport_target'] = cmdgen.UdpTransportTarget(
        (args.scanner_addr, 161))

    # Get IP and port to advertise
    adv_addr = (args.advertise_addr, args.advertise_port)

    myprint(f'Advertising {adv_addr[0]}:{adv_addr[1]} to {args.scanner_addr}')

    for func, users in config['menu'].items():
        for user, entry in users.items():
            myprint('Entry:', func.upper(), user, entry)

    while 1:
        # Repeat advertising step each 60 seconds
        myprint('Advertising to scanner')
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
