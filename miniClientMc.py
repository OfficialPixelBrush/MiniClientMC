import socket
import struct

HOST = "127.0.0.1"
PORT = 25565

def toString16(text):
    response = b''
    text_length = len(text)
    length_bytes = struct.pack('>H', text_length)
    response += length_bytes

    for c in text:
        encoded_char = c.encode('utf-16')[2:]
        swapped_encoded_char = encoded_char[::-1]
        response += swapped_encoded_char
    return response

x = 0.5
y = 70.5
z = 0.5
stance = 1.7
pitch = 0.0
yaw = 0.0
onGround = False

speed = 1.0

def SendHandshake(username):
    response = b'\x02'
    response += toString16(username)
    s.sendall(response)
    return s.recv(1024)

def SendLoginRequest(protocol,username):
    response = b'\x01'
    response += struct.pack('>i', protocol)
    response += toString16(username)
    response += struct.pack('>l', 0)
    response += b'\x00'
    s.sendall(response)
    return s.recv(1024)

def SendPlayerPositionLook():
    global x
    global y
    global z
    global stance
    global pitch
    global yaw
    global onGround
    response = b'\x0D'
    response += struct.pack('>d', x)
    response += struct.pack('>d', y)
    response += struct.pack('>d', stance)
    response += struct.pack('>d', z)
    response += struct.pack('>f', yaw)
    response += struct.pack('>f', pitch)
    response += struct.pack('>?', onGround)
    s.sendall(response)
    return s.recv(1024)

def SendChatMessage(message):
    response = b'\x03'
    response += toString16(message)
    s.sendall(response)
    return s.recv(1024)

def SendDisconnect(message):
    response = b'\xFF'
    response += toString16(message)
    s.sendall(response)
    return s.recv(1024)

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    username = input("Username? ")
    # Connect to the server
    s.connect((HOST, PORT))

    # Receive the response from the server
    data = SendHandshake(username)
    data = SendLoginRequest(14,username)
    while True:
        user_input = input("Message? ")
        if (user_input == "exit"):
            SendDisconnect("Quitting")
            break
        SendChatMessage(user_input)
