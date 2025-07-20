def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
 
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
 
# Attempt to connect to WiFi network
do_connect('GNet', '212850677')
 
#import webrepl	# 
#webrepl.start()
#network config: ('192.168.1.87', '255.255.255.0', '192.168.1.254', '192.168.1.254')
#WebREPL server started on http://192.168.1.87:8266/
#Started webrepl in normal mode

import uftpd
#FTP server started on 192.168.1.87:21
