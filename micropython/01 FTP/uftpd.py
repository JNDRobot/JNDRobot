import socket
import network
import uos
import gc

ftpsocket = None
datasocket = None
last_client_socket = None
DATA_PORT = 13333
PASV_seen = False

cwd = '/'
msg_250_OK = '250 OK\r\n'
msg_550_fail = '550 Failed\r\n'
fromname = None

from time import localtime

month_name = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def send_list_data(path, dataclient, full):
    try: # whether path is a directory name
        for fname in sorted(uos.listdir(path), key = str.lower):
            dataclient.sendall(make_description(path, fname, full))
    except: # path may be a file name or pattern
        pattern = path.split("/")[-1]
        path = path[:-(len(pattern) + 1)]
        if path == "": path = "/"
        for fname in sorted(uos.listdir(path), key = str.lower):
            if fncmp(fname, pattern) == True:
                dataclient.sendall(make_description(path, fname, full))
                
def make_description(path, fname, full):
    global month_name
    if full:
        stat = uos.stat(get_absolute_path(path,fname))
        file_permissions = "drwxr-xr-x" if (stat[0] & 0o170000 == 0o040000) else "-rw-r--r--"
        file_size = stat[6]
        tm = localtime(stat[7])
        if tm[0] != localtime()[0]:
            description = "{}    1 owner group {:>10} {} {:2} {:>5} {}\r\n".format(
                file_permissions, file_size, month_name[tm[1]], tm[2], tm[0], fname)
        else:
            description = "{}    1 owner group {:>10} {} {:2} {:02}:{:02} {}\r\n".format(
                file_permissions, file_size, month_name[tm[1]], tm[2], tm[3], tm[4], fname)
    else:
        description = fname + "\r\n"
    return description
    
def send_file_data(path, dataclient):
    with open(path, "r") as file:
        chunk = file.read(512)
        while len(chunk) > 0:
            dataclient.sendall(chunk)
            chunk = file.read(512)

def save_file_data(path, dataclient, mode):
    with open(path, mode) as file:
        chunk = dataclient.read(512)
        while len(chunk) > 0:
            file.write(chunk)
            chunk = dataclient.read(512)

def get_absolute_path(cwd, payload):
    # Just a few special cases "..", "." and ""
    # If payload start's with /, set cwd to / 
    # and consider the remainder a relative path
    if payload.startswith('/'):
        cwd = "/"
    for token in payload.split("/"):
        if token == '..':
            if cwd != '/':
                cwd = '/'.join(cwd.split('/')[:-1])
                if cwd == '': 
                    cwd = '/'
        elif token != '.' and token != '':
            if cwd == '/':
                cwd += token
            else:
                cwd = cwd + '/' + token
    return cwd

# compare fname against pattern. Pattern may contain
# wildcards ? and *.
def fncmp(fname, pattern):
    pi = 0
    si = 0
    while pi < len(pattern) and si < len(fname):
        if (fname[si] == pattern[pi]) or (pattern[pi] == '?'):
            si += 1
            pi += 1
        else:
            if pattern[pi] == '*': # recurse
                if (pi + 1) == len(pattern):
                    return True
                while si < len(fname):
                    if fncmp(fname[si:], pattern[pi+1:]) == True:
                        return True
                    else:
                        si += 1
                return False
            else:
                return False
    if pi == len(pattern.rstrip("*"))  and si == len(fname):
        return True
    else:
        return False

def accept_ftp_connect(ftpsocket):

    global last_client_socket
    global cwd, fromname
    
    if last_client_socket:
        # close any previous clients
        last_client_socket.close()
    
    last_client_socket, remote_addr = ftpsocket.accept()
    last_client_socket.settimeout(300)
    print("FTP connection from:", remote_addr)
    cwd = '/'
    fromname = None
    last_client_socket.setblocking(False)
    last_client_socket.setsockopt(socket.SOL_SOCKET, 20, exec_ftp_command)
    last_client_socket.sendall("220 Hello, this is the ESP8266.\r\n")
        
def exec_ftp_command(cl):
    global last_client_socket
    global cwd, fromname
    global ftpsocket, datasocket
    global DATA_PORT, PASV_seen
    
    dataclient = None

    try:
        gc.collect()
        data = cl.readline().decode("utf-8").rstrip("\r\n")
        if len(data) <= 0:
            # print("Client disappeared")
            return
        
        command = data.split(" ")[0].upper()
        payload = data[len(command):].lstrip()
        path = get_absolute_path(cwd, payload)
        print("Command={}, Payload={}, Path={}, PASV={}".format(command, payload, path, PASV_seen))
        
        if command == "USER":
            cl.sendall("230 Logged in.\r\n")
        elif command == "SYST":
            cl.sendall("215 UNIX Type: L8\r\n")
        elif command == "NOOP":
            cl.sendall("200 OK\r\n")
        elif command == "FEAT":
            cl.sendall("211 no-features\r\n")
        elif command == "PWD":
            cl.sendall('257 "{}"\r\n'.format(cwd))
        elif command == "CWD":
            try:
                files = uos.listdir(path)
                cwd = path
                cl.sendall(msg_250_OK)
            except:
                cl.sendall(msg_550_fail)
        elif command == "CDUP":
            cwd = get_absolute_path(cwd, "..")
            cl.sendall(msg_250_OK)
        elif command == "TYPE":
            # probably should switch between binary and not
            cl.sendall('200 Transfer mode set\r\n')
        elif command == "SIZE":
            try:
                size = uos.stat(path)[6]
                cl.sendall('213 {}\r\n'.format(size))
            except:
                cl.sendall(msg_550_fail)
        elif command == "QUIT":
            cl.sendall('221 Bye.\r\n')
            cl.close()
            cl = None
            ftpsocket.setsockopt(socket.SOL_SOCKET, 20, accept_ftp_connect)
        elif command == "PASV":
            addr = network.WLAN().ifconfig()[0]
            cl.sendall('227 Entering Passive Mode ({},{},{}).\r\n'.format(
                addr.replace('.',','), DATA_PORT>>8, DATA_PORT%256))
            PASV_seen = True
#            dataclient, data_addr = datasocket.accept()
#            print("FTP Data connection from:", data_addr)
        elif command == "LIST" or command == "NLST":
            dataclient, data_addr = datasocket.accept()
            if not payload.startswith("-"):
                place = path
            else: 
                place = cwd
            try:
                send_list_data(place, dataclient, command == "LIST" or payload == "-l")
                cl.sendall("150 Here comes the directory listing.\r\n")
                cl.sendall("226 Listed.\r\n")
            except:
                cl.sendall(msg_550_fail)
            dataclient.close()
            PASV_seen = False
        elif command == "RETR":
            dataclient, data_addr = datasocket.accept()
            try:
                send_file_data(path, dataclient)
                cl.sendall("150 Opening data connection.\r\n")
                cl.sendall("226 Transfer complete.\r\n")
            except:
                cl.sendall(msg_550_fail)
            dataclient.close()
            PASV_seen = False
        elif command == "STOR":
            dataclient, data_addr = datasocket.accept()
            try:
                cl.sendall("150 Ok to send data.\r\n")
                save_file_data(path, dataclient, "w")
                cl.sendall("226 Transfer complete.\r\n")
            except:
                cl.sendall(msg_550_fail)
            dataclient.close()
            PASV_seen = False
        elif command == "APPE":
            dataclient, data_addr = datasocket.accept()
            try:
                cl.sendall("150 Ok to send data.\r\n")
                save_file_data(path, dataclient, "a")
                cl.sendall("226 Transfer complete.\r\n")
            except:
                cl.sendall(msg_550_fail)
            dataclient.close()
            PASV_seen = False
        elif command == "DELE":
            try:
                uos.remove(path)
                cl.sendall(msg_250_OK)
            except:
                cl.sendall(msg_550_fail)
        elif command == "RMD":
            try:
                uos.rmdir(path)
                cl.sendall(msg_250_OK)
            except:
                cl.sendall(msg_550_fail)
        elif command == "MKD":
            try:
                uos.mkdir(path)
                cl.sendall(msg_250_OK)
            except:
                cl.sendall(msg_550_fail)
        elif command == "RNFR":
                fromname = path
                cl.sendall("350 Rename from\r\n")
        elif command == "RNTO":
                if fromname is not None: 
                    try:
                        uos.rename(fromname, path)
                        cl.sendall(msg_250_OK)
                    except:
                        cl.sendall(msg_550_fail)
                else:
                    cl.sendall(msg_550_fail)
                fromname = None
        else:
            cl.sendall("502 Unsupported command.\r\n")
            # print("Unsupported command {} with payload {}".format(command, payload))
    except Exception as err:
        print(err)  
        cl.close()
        cl = None
        ftpsocket.setsockopt(socket.SOL_SOCKET, 20, accept_ftp_connect)
        if dataclient is not None:
            dataclient.close()

def stop():
    global ftpsocket, datasocket, dataclient

    if ftpsocket is not None:
        ftpsocket.close()
    if datasocket is not None:
        datasocket.close()

# start listening for telnet connections on port 23
def start(port=21):
    global ftpsocket, datasocket
    global DATA_PORT

    ftpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ftpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    datasocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ftpsocket.bind(socket.getaddrinfo("0.0.0.0", 21)[0][4])
    datasocket.bind(socket.getaddrinfo("0.0.0.0", DATA_PORT)[0][4])

    ftpsocket.listen(1)
    datasocket.listen(1)
    datasocket.settimeout(10)
    ftpsocket.setsockopt(socket.SOL_SOCKET, 20, accept_ftp_connect)
    
    for i in (network.AP_IF, network.STA_IF):
        wlan = network.WLAN(i)
        if wlan.active():
            print("FTP server started on {}:{}".format(wlan.ifconfig()[0], port))

start()
