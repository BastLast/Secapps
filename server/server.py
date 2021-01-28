# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.
import os

from classes.log import Log

HOST = '127.0.0.1'
PORT = 40000

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
        return {
            'get': get,
            'put': put,
            'ls': ls,
            'rm': rm,
            'perm': perm
        }.get(data.get('args')[0], self.nf)(data)

    def run(self):
        # Récupère le fichier json des utilisateurs
        with open("users.json", "r") as read_users:
            data = json.load(read_users)
        # Dialogue avec le client :
        # with open("config.json", "r") as read_config:
        # data2 = json.load(read_config)
        # print(data2.get("Salt"))
        # self.connexion.send(data2.get("Salt"))
        name = self.getName()  # Chaque thread possède un nom
        self.connexion.send("Entrez votre login : ".encode('utf-8'))
        login = self.connexion.recv(2048).decode("utf-8")
        self.connexion.send('Entrez votre mot de passe : '.encode('utf-8'))
        password = self.connexion.recv(2048).decode("utf-8")
        exist = False
        for pseudoId, user in data.items():
            if login == user.get("login"):
                exist = True
                pseudo_id = pseudoId
        # Cas nouvel utilisateur
        if not exist:
            self.connexion.send("Enregistrement et connexion réussi".encode('utf-8'))
            print("Enregistré : ", login)
            can_connect = True

        else:
            # Cas utilisateur existe déjà
            if data.get(pseudo_id).get("password") == password:
                self.connexion.send("Connexion réussie".encode('utf-8'))
                print('Connexion réussie : ', login)
                can_connect = True
            else:
                self.connexion.send("Connexion échouée".encode('utf-8'))
                print('Connexion échouée : ', login)
                can_connect = False
        while can_connect:
            receivedmessage = self.connexion.recv(1024).decode("UTF-8")
            data = yaml.safe_load(receivedmessage)
            print(self.exec_command(data))

        # Fermeture de la connexion :
        self.connexion.close()  # couper la connexion côté serveur
        if name in conn_client:
            del conn_client[name]  # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % name)
        # Le thread se termine ici


# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
log = Log().get_daiquiri()
try:
    mySocket.bind((HOST, PORT))
    log.error("ca run !!", somekey="test1", anotherkey="test")
except socket.error:
    print("La liaison du socket à l'adresse choisie a échoué.")
    sys.exit()
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
