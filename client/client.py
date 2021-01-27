# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

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
    @staticmethod
    def parseargs(message):
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

    def run(self):
        while 1:
            docexemple = {'truc1': "yolo", 'truc2': "yolo2"}
            args = parseargs(input())
            message_emis = yaml.safe_dump(docexemple).encode("UTF-8")
            self.connexion.send(message_emis)

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()
