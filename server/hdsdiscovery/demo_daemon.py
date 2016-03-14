import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 8889))
serversocket.listen(5) # become a server socket, maximum 5 connections

print("Listening...")

while True:
    conn, address = serversocket.accept()
    print 'Connected with ', address
    buf = conn.recv(1024)
    if len(buf) > 0:
        print buf
        
        #TODO: configure cobbler according to the server info in buff.
        conn.send("reboot")
        continue
