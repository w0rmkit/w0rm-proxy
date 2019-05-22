import socket
import sys
import time
from termcolor import colored
from thread import *

def main():
    global listen_port, buffer_size, max_conn
    try:
        listen_port  = int(raw_input("Enter  a listening port: "))
    except KeyboardInterrupt:
        sys.exit()

    max_conn = 5
    buffer_size = 8192

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', listen_port))
        s.listen(max_conn)
	print("     . .  .  .  . . .")
	print("   .                  . ")
	print("   . What a nice day! .   ")
	print("    .  .  .  .      .`   ")
	print("                `..'  _\\\//")
	print("                     /@/@\  \"")
	print("                    ,\_\_/   |")
	print("                   { o    /   }")
	print("                    `-==-'   /    ")
	print("                      |>o<|  }@@@}        Developed by w0rm | @swagggs_")
	print("                     <(___<) }@@@@}")
	print("                     <(___<) }@@@@@}")
	print("                      <\___<) \_.?@@}")
	print("                        V`--V`__./@}")
	print("                      tx      ooo@}")
	print("")
	print("")
        print("[*] Intializing scoket... Done :-)")
	time.sleep(2)
        print("[*] Starting server on port: {}".format(listen_port))
	time.sleep(2)
	print("[*] Checking server connection ..."), colored('OK', 'green')
    except Exception as e:
        print(e)
        sys.exit(2)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Shutting server down...")
            sys.exit(1)

    s.close()


def conn_string(conn, data, addr):
    try:
        first_line = data.split("\n")[0]
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos  == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]
            
        port_pos = temp.find(":")

        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1

        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos -1])
            webserver = temp[:port_pos]
            
        print(webserver)
        proxy_server(webserver, port, conn, data, addr)
    except Exception as e:
        print(e)

def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)

        while True:
            reply = s.recv(buffer_size)

            if len(reply) > 0:
                conn.send(reply)

                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "{}.3s".format(dar)
                print("Request done: {} => {} <= {}".format(addr[0], dar, webserver))
            else:
                break
            
        s.close()
        conn.close()
    except socket.error, (value, msg):
        s.close()
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
