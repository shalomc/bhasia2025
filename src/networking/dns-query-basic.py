import socket

domain = "google.com"
ip = socket.gethostbyname(domain)
print(f"IP address of {domain}: {ip}")

# f"IP address of {domain}: {ip}"