import socket
import math
import re

HOST = "challenge01.root-me.org"
PORT = 52002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    data = s.recv(4096).decode()
    print(data)
    match = re.search(
        r"square root of\s+(\d+(?:\.\d+)?)\s+and multiply by\s+(\d+(?:\.\d+)?)",
        data,
        re.IGNORECASE
    )

    if not match:
        print("Could not parse calculation.")
        exit()

    number = float(match.group(1))
    multiplier = float(match.group(2))

    result = math.sqrt(number) * multiplier

    answer = f"{result:.2f}\n"

    print(answer)
    s.sendall(answer.encode())

    response = s.recv(4096).decode()
    print("Server:", response)
