"""
Overview of brscan package


Package brscan:
    - Module brscand:
        Main module contains the public callable function (main())
        creates Threads for listen.launch() and snmp.launch()
          brscand arguments:
            bind_addr', metavar='BIND_ADDR',
                        type=str,
                        help='IP/host to bind UDP socket to'
            -p', '--bind-port', metavar='PORT',
                        type=int, default=54925,
                        help='UDP port number to bind UDP socket to'
            -A', '--advertise-addr', metavar='ADDR',
                        type=str, default=None,
                        help='IP/host to advertise to scanner'
            -P', '--advertise-port', metavar='PORT',
                        type=int, default=None,
                        help='UDP port number to advertise to scanner'
            scanner_addr', metavar='SCANNER_ADDR',
                        type=str,
                        help='IP address of scanner'
            -c', '--config', metavar='FILE',
                        type=str, default='brother-scan.yaml',
                        help='Configuration file'
    - listen:
        Open listen Port and wait for scanner to trigger a scan.
        If a scan request is received submodule scanto is triggered.
    - snmp:
        Transmit the given configuration to scanner and advertise Host IP
    - scanto:
        Waits for requests from listen submodule
"""
