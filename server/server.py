# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.

HOST = '127.0.0.1'
PORT = 40000

import socket
import sys
import threading
import yaml


class ThreadClient(threading.Thread):
    # objet thread pour gérer la connexion avec un client
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        # Dialogue avec le client :
        nom = self.getName()  # Chaque thread possède un nom
        while 1:
            receivedmessage = yaml.safe_dump(self.connexion.recv(1024).decode("UTF-8"))
            receiveddoc = yaml.safe_load(receivedmessage)
            if receivedmessage.upper() == "FIN" or receivedmessage == "":
                break
            message = "%s> %s" % (nom, receivedmessage)
            print(receiveddoc)
            receiveddoc

        # Fermeture de la connexion :
        self.connexion.close()  # couper la connexion côté serveur
        del conn_client[nom]  # supprimer son entrée dans le dictionnaire
        print("Client %s déconnecté." % nom)
        # Le thread se termine ici


# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
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
    th.start()
    # Mémoriser la connexion dans le dictionnaire :
    it = th.getName()  # identifiant du thread
    conn_client[it] = connexion
    print("Client %s connecté, adresse IP %s, port %s." % \
          (it, adresse[0], adresse[1]))
    # Dialogue avec le client :
    connexion.send("Vous êtes connecté. Envoyez vos messages.".encode("utf-8"))
