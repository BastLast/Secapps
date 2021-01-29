# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).
import hashlib
import json
import os
import socket
import sys
import threading
from time import sleep

import yaml
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes

from commands.get import get
from commands.put import put
from commands.ls import ls
from commands.perm import perm
from commands.rm import rm
from Crypto.PublicKey import RSA

host = '127.0.0.1'
port = 40000
secret_code = "JackJack"


class ThreadReception(threading.Thread):
    # objet thread gérant la réception des messages du serveur
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

    # Thread envoyant les commandes

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn  # réf. du socket de connexion

    def parseargs(self, message):
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
        return m_parsed

    def nf(self, args):
        return "Unrecognized command."

    def exec_command(self, args):
        return {
            'get': get,
            'put': put,
            'ls': ls,
            'rm': rm,
            'perm': perm
        }.get(args[0], self.nf)(args)

    # parse arguments from message
    # message : string

    def run(self):
        while 1:
            result = self.exec_command(self.parseargs(input()))
            self.connexion.send("DEBUT".encode("utf-8"))
            f = open("server_instruction", 'wb')
            f.write(result)
            f.close()
            f = open("server_instruction", 'rb')
            senddata = f.read(1024)
            while senddata:
                self.connexion.send(senddata)
                senddata = f.read(1024)
                print(senddata)
            sleep(1)
            self.connexion.send("FIN".encode("utf-8"))
            f.close()
            # A tester: recupère la clé public du serv et s'en sert pour chiffrer avant d'envoyer
            # with open("publicclient.json", "r") as publicclient:
            #     public_key = RSA.import_key(json.load(publicclient)["server"].encode('utf-8'), passphrase=secret_code)
            #     session_key = get_random_bytes(16)
            #
            #     # Encrypt the session key with the public RSA key
            #     cipher_rsa = PKCS1_OAEP.new(public_key)
            #     enc_session_key = cipher_rsa.encrypt(session_key)
            #
            #     # Encrypt the data with the AES session key
            #     cipher_aes = AES.new(session_key, AES.MODE_EAX)
            #     ciphertext, tag = cipher_aes.encrypt_and_digest(result)
            #     result = open("result.bin", "wb")
            #     [result.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
            #     result.close()



# Programme principal - Établissement de la connexion :
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    response = client_socket.recv(2048)  # Demande login par serveur
    name = input(response.decode('utf-8'))
    if name == "server":
        name = input("Ce pseudo n'est pas autorisé, veuillez en choisir un nouveau svp :")
    client_socket.send(name.encode('utf-8'))  # Envoi login
    response = client_socket.recv(2048)  # Demande password par serveur
    salt = b'\xf0\xa4\x1f;\xcbZ\xf41\xb4k{T\xac\x8ea\x9a'
    password = hashlib.pbkdf2_hmac('sha256', input(response.decode('utf-8')).encode('utf-8'), salt, 100000).hex()
    client_socket.send(password.encode('utf-8'))  # Envoie password
    response = client_socket.recv(2048)  # Demande pubkey par serveur
    if response.decode('utf-8') == "pubkey":
        if os.path.getsize("privateclient.json") > 0 and os.path.getsize("publicclient.json") > 0:
            with open("privateclient.json", "r") as privateclient:
                dataprivate = json.load(privateclient)
                stopbug = False
                if (name in dataprivate.keys() and dataprivate[name] == "") or name not in dataprivate.keys():
                    secret_code = "JackJack"
                    key = RSA.generate(2048)
                    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
                    public_key = key.publickey().export_key()
                    dataprivate[name] = encrypted_key.decode('utf-8')
                    with open("publicclient.json", "r") as publicclient:
                        datapublic = json.load(publicclient)
                        datapublic[name] = public_key.decode('utf-8')
                    with open("publicclient.json", "w") as publicclient:
                        json.dump(datapublic, publicclient)
                else:
                    with open("publicclient.json", "r") as publicclient:
                        datapublic = json.load(publicclient)
                        public_key = datapublic[name].encode('utf-8')
            with open("privateclient.json", "w") as privateclient:
                json.dump(dataprivate, privateclient)
        else:
            key = RSA.generate(2048)
            encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
            public_key = key.publickey().export_key()
            with open("privateclient.json", "w") as privateclient:
                dataprivate = {name: encrypted_key.decode('utf-8')}
                json.dump(dataprivate, privateclient)
            with open("publicclient.json", "w") as publicclient:
                datapublic = {name: public_key.decode('utf-8')}
                json.dump(datapublic, publicclient)
        client_socket.send(public_key)
        pub_key_serv = client_socket.recv(2048)  # Reçoit clé public serveur
    with open("publicclient.json", "w") as publicclient:
        datapublic["server"] = pub_key_serv.decode('utf-8')
        json.dump(datapublic, publicclient)
    response = client_socket.recv(2048)  # Serveur indique si connecté ou non
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
