import socket


# https://stackoverflow.com/a/25850698
def get_local_ip_address():
    # get the local IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]
