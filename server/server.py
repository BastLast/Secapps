# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA

from classes.log import Log

HOST = '127.0.0.1'
PORT = 40000
secret_code = "Serveur"

import socket
import sys
import threading
import yaml
import json

from commands.get import get
from commands.ls import ls
from commands.perm import perm
from commands.put import put
from commands.rm import rm


class ThreadClient(threading.Thread):
    # objet thread pour gérer la connexion avec un client
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def nf(self, args):
        return "Unrecognized command."

    def exec_command(self, data):
        if data is None:
            return "none"
        else:
            return {
                'get': get,
                'put': put,
                'ls': ls,
                'rm': rm,
                'perm': perm
            }.get(data.get('args')[0], self.nf)(data)

    def run(self):
        can_connect = self.logincheck()
        receiveddata = b""
        mergemessages = False
        while can_connect:
            receivedmessage = self.decrypt(self.connexion.recv(1024)).decode('utf-8')
            # Test if the client was disconected
            if receivedmessage == '' or receivedmessage.upper() == "FIN":
                break

            if mergemessages and receivedmessage != "FIN":
                receiveddata = b"".join([receiveddata, receivedmessage])

            if receivedmessage == "DEBUT":
                receiveddata = b""
                mergemessages = True

            if receivedmessage == "FIN":
                mergemessages = False

            if not mergemessages:
                # traitement de la commande
                loadeddata = yaml.safe_load(receiveddata)
                result = self.exec_command(loadeddata)
                self.connexion.send(result.encode('utf-8'))



        # Fermeture de la connexion :
        self.connexion.close()  # couper la connexion côté serveur
        name = self.getName()
        if name in conn_client:
            del conn_client[name]  # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % name)
        # Le thread se termine ici

    # A tester quand server pourra envoyer à client.
    def encrypt(self, data, nameid):
        with open("users.json", "r") as publicclient:
            public_key = RSA.import_key(json.load(publicclient)[nameid].get("pub_key").encode('utf-8'))
            enc_data = PKCS1_OAEP.new(public_key).encrypt(data)
        return enc_data

    def decrypt(self, data):
        with open('prvkeyserv.pem','r') as f:
	        priv = f.read()
	        f.close()
        private_key = RSA.import_key(priv)
        dec_data = PKCS1_OAEP.new(private_key).decrypt(data)
        return dec_data

    def logincheck(self):
        self.connexion.send("Entrez votre login : ".encode('utf-8'))  # Demande login
        login = self.connexion.recv(2048).decode("utf-8")
        self.connexion.send('Entrez votre mot de passe : '.encode('utf-8'))  # Demande pw
        password = self.connexion.recv(2048).decode("utf-8")
        exist = False
        self.connexion.send("pubkey".encode('utf-8'))  # Demande pubkey client
        pubkey = self.connexion.recv(2048).decode("utf-8")
        self.connexion.send(RSA.import_key(open("pubkeyserv.pem").read()).export_key())  # Envoie sa clé public
        if os.path.isfile("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as read_users:
                data = json.load(read_users)
            for pseudoId, user in data.items():  # Test si le login envoyé correspond à un compte stocké
                if login == user.get("login"):
                    exist = True
                    pseudo_id = pseudoId
        # Cas nouvel utilisateur
        if not exist:
            data[login + "@" + str(len(data))] = {
                "login": login,
                "password": password,
                "id": str(len(data)),
                "pseudo": login,
                "admin": True,
                "pub_key": pubkey
            }
            with open("users.json", "w") as outfile:
                json.dump(data, outfile)
            can_connect = True
            self.connexion.send("Enregistrement réussi".encode('utf-8'))
        else:
            # Cas utilisateur existe déjà
            if data.get(pseudo_id).get("password") == password:
                self.connexion.send("Connexion réussie".encode('utf-8'))
                print('Connexion réussie : ')
                can_connect = True
                if data.get(pseudo_id).get("pub_key") == "":
                    with open("users.json", "w") as list_user:
                        data[pseudo_id]["pub_key"] = pubkey
                        json.dump(data, list_user)
            else:
                self.connexion.send("Connexion échouée".encode('utf-8'))
                print('Connexion échouée : ')
                can_connect = False
        return can_connect


# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log = Log().get_daiquiri()
try:
    mySocket.bind((HOST, PORT))
    log.error("ca run !!", somekey="test1", anotherkey="test")
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
f = open('prvkeyserv.pem', 'rb')
if "-----BEGIN RSA PRIVATE KEY-----" != f.readline().rstrip().decode("utf-8"):
    f.close()
    key = RSA.generate(2048)
    private_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")
    public_key = key.publickey().export_key()
    f = open('prvkeyserv.pem', 'wb')
    f.write(private_key)
    f2 = open('pubkeyserv.pem', 'wb')
    f2.write(public_key)
    f2.close()
f.close()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}  # dictionnaire des connexions clients
while 1:
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
    conn_client[th.getName()] = connexion
    th.start()
