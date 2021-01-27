# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import hashlib
import os
import socket
import sys
import threading
import yaml

host = '127.0.0.1'
port = 40000


class ThreadReception(threading.Thread):
    # objet thread gérant la réception des messages
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion

    def run(self):
        while 1:
            message_recu = self.connexion.recv(1024).decode("utf-8")
            print("*" + message_recu + "*")
            if message_recu == '' or message_recu.upper() == "FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        th_E._Thread__stop()
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()


class ThreadEmission(threading.Thread):
    #objet thread gérant l'émission des messages

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion

    #parse arguments from message
    #message : string
    def parseargs(self,message):
        m_quotes = message.split("\"")
        m_parsed = []
        i = 0
        for m in m_quotes:
            if i:
                m_parsed.append(m)
            else:
                m_parsed += m.split(" ")
            i += 1
        m_parsed = [m for m in m_parsed if m != ""]
        return m_parsed;

    def get(self,args):
        return "get"
    def put(self,args):
        return "put"
    def ls(self,args):
        return "ls"
    def rm(self,args):
        return "rm"
    def perm(self,args):
        return "perm"

    def exec_command(self,args):
        return {
            'get':self.get(args),
            'put':self.put(args),
            'ls':self.ls(args),
            'rm':self.rm(args),
            'perm':self.perm(args)
        }.get(args[0],"Unrecognized command.")

    def run(self):
        while 1:
            result = self.exec_command(self.parseargs(input()))
            message_emis = yaml.safe_dump(result).encode("UTF-8")
            self.connexion.send(message_emis)

# Programme principal - Établissement de la connexion :
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    #salt = client_socket.recv(2048)
    response = client_socket.recv(2048)
    # Input UserName
    name = input(response.decode('utf-8'))
    client_socket.send(name.encode('utf-8'))
    response = client_socket.recv(2048)
    # Input Password
    salt = b'\xf0\xa4\x1f;\xcbZ\xf41\xb4k{T\xac\x8ea\x9a'
    password = hashlib.pbkdf2_hmac('sha256', input(response.decode('utf-8')).encode('utf-8'), salt, 100000).hex()
    client_socket.send(password.encode('utf-8'))
    response = client_socket.recv(2048)
    if response.decode('utf-8') == "Enregistrement réussi" or response.decode('utf-8') == "Connexion réussie":
        # Dialogue avec le serveur : on lance deux threads pour gérer
        # indépendamment l'émission et la réception des messages :
        print(response.decode('utf-8'))
        th_E = ThreadEmission(client_socket)
        th_R = ThreadReception(client_socket)
        th_E.start()
        th_R.start()
    else:
        print(response.decode('utf-8'))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()



