
import socket




def get_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if IPAddr[0:7] == "169.254":
        IPAddr = "no internet"

    return IPAddr