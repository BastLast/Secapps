# TP Sécurité des applications

## Installation & exécution

### Installation

Il est nécessaire d'installer au préalable les librairies python suivantes :
*   daiquiri
*   PyYAML
*   crypto

### Exécution

Se placer dans le répertoire d'installation.
Lancer le serveur depuis le répertoire server
*   cd server
*   python3 server.py

Lancer une ou plusieurs instances du client depuis le répertoire client
*   cd client
*   python3 client.py

Aucun utilisateur n'existe lors du premier lancement. Celui-ci est créé avec le login et le mot de passe fournis au moment de la connexion au client.

## Document d’architecture 

### Contexte

Ce projet a pour objet la réalisation d’un logiciel de transfert. Pour cela, nous suivrons une architecture de type client serveur schématisée ci-après. L’objectif est que les utilisateurs puissent télécharger, charger, supprimer et partager des fichiers entre eux. L’ensemble des fonctionnalités sera utilisable via des commandes dans une CLI.

### Architecture

![](https://media.discordapp.net/attachments/802123360091635724/803631964883910716/TP_Securite_des_applications.png)

### Interface
Nous utiliserons yaml pour faire transiter les commandes sérialisées en tant que string entre client et serveur.

### Objets

Dossier

*   id propriétaire
*   liste user autorisés à créer
*   nom

Fichier

*   Nom de fichier (string) 
*   Users autorisés (dictionnaire de permissions à true/false pour chaque user)
*   User owner (user)
*   Chemin d’accès (unique)

User

*   Login
*   Mot de passe (Stocké hashé côté client et salé)
*   Id
*   Pseudo
*   Admin (boolean)
*   Clé public


### 


### Personae

**Admin:**



*   Afficher la liste de tous les dossiers utilisateurs
*   Afficher le contenu d’un dossier utilisateur
*   Afficher les permissions sur un dossier/fichier
*   Modifier les permissions sur un dossier/fichier

**Utilisateur :**
- **Propriétaire :**

    *   Gérer les permissions des fichiers de son dossier
    *   Faire la liste des fichiers dans son dossier
    *   Télécharger un fichier
    *   Envoyer un fichier
    *   Supprimer un fichier
    *   Ecraser un fichier
    *   Créer un fichier


- **Autre :**

    *   Télécharger un fichier (s’il en a l’autorisation)
    *   Envoyer un fichier (s’il en a l’autorisation)
    *   Supprimer un fichier (s’il en a l’autorisation)
    *   Écraser un fichier (s’il en a l’autorisation)
    *   Créer un fichier (s’il en a l’autorisation)


### Gestion des permissions

**Gestion des permissions pour un fichier**



*   Lister. Les fichiers que l’utilisateur a le droit de lister
*   Télécharger un fichier
*   Envoyer un fichier
*   Supprimer un fichier
*   Ecraser un fichier

**Gestion des permissions pour un dossier**



*   Créer un fichier. Le créateur détient les droits suivants : lister, télécharger, supprimer et écraser le fichier

Il est impossible de révoquer les droits d’un propriétaire.


### Ajout d'utilisateurs

Afin d'ajouter un nouvel utilisateur, il suffit de fournir un login qui n'existe pas lors de la connexion.
Le premier utilisateur créé sur le serveur sera par défaut administrateur, les autres seront utilisateurs simples.
Il n'est pas possible de donner ou retirer les droits d'administrateur.

### Sécurité

Pour accéder au serveur, il faut passer par un système d’authentification par login/mot de passe. Les mots de passe sont stockés par paire avec le login dans un fichier. Les mots de passe sont hashés côté client au préalable.

L’accès à un fichier de clientA par clientB n’est possible que si clientA a ajouté à sa liste d’autorisation clientB. Pour chaque fichier, un tableau de dictionnaires est attribué. Chaque dictionnaire contient le pseudo@id de l’utilisateur et un booléen pour chaque permission.

Chiffrement pour la communication entre client et serveur:



*   ClientA chiffre son fichier avec la clé public du serveur.
*   Le serveur déchiffre et stock le fichier.
*   Le serveur chiffre avec la clé public du destinataire pour envoyer un fichier.

Instaurer des logs. Les fichiers sont chiffrés pour ne pas être modifiés.

Tester la syntaxe des commandes. Autoriser simplement celles dont nous avons besoin.


### Multi threads

Dans un premier temps, le serveur ne gérera pas le multi-thread.

Si nous en avons le temps, le but est que chaque commande reçue par le serveur soit gérée dans un thread à part pour permettre le traitement en parallèle des commandes.

## Analyse de risques

<table>
  <tr>
   <td><strong>Menace</strong>
   </td>
   <td><strong>Impact</strong>
   </td>
   <td><strong>Probabilité d’occurrence</strong>
   </td>
   <td><strong>Criticité</strong>
   </td>
   <td><strong>Remédiation</strong>
   </td>
  </tr>
  <tr>
   <td>Intrusion serveur
   </td>
   <td>Catastrophique
   </td>
   <td> Rare
   </td>
   <td> Forte
   </td>
   <td>Avoir les autorisation admin sur la machine pour lire les fichiers sensibles
   </td>
  </tr>
  <tr>
   <td>Vol de login/mot de passe côté serveur
   </td>
   <td>Catastrophique
   </td>
   <td>Hautement improbable
   </td>
   <td> Forte
   </td>
   <td>Hash
   </td>
  </tr>
  <tr>
   <td>Modifications des droits sur les dossiers d’autrui
   </td>
   <td>Catastrophique
   </td>
   <td>Hautement improbable
   </td>
   <td> Forte
   </td>
   <td>Non traité
   </td>
  </tr>
  <tr>
   <td>Exécution d’un fichier malveillant sur le serveur
   </td>
   <td>Catastrophique
   </td>
   <td>Hautement improbable
   </td>
   <td> Forte
   </td>
   <td>Vérification des commandes envoyées
   </td>
  </tr>
  <tr>
   <td>Interception communication client - serveur
   </td>
   <td>Grave
   </td>µ
   <td>Probable
   </td>
   <td> Moyenne
   </td>
   <td>Chiffrement communication 
   </td>
  </tr>
  <tr>
   <td>L’admin se crée un compte user pour lui donner tous les droits
   </td>
   <td>Grave
   </td>
   <td>Probable
   </td>
   <td> Très forte
   </td>
   <td>Créer une double authentification par pièce d’identité ou autre identifiant unique
   </td>
  </tr>
</table>

**Légende**

Impact :

*   Insignifiant
*   Signifiant
*   Grave
*   Catastrophique

Probabilité d'occurrence

*   Fréquent
*   Probable
*   Occasionnel
*   Rare
*   Improbable
*   Hautement Improbable


## Coding rules / red (règles de l’équipe de dev) / tooling

**IDE:** PyCharm

**Versionning:** [https://gitlab.mines-ales.fr/BastLast/secapps](https://gitlab.mines-ales.fr/BastLast/secapps)

**Langage:** Python 3.9.1

**Librairie de log utilisée :** daiquiri

**Librairie de chiffrement et de hachage utilisée :** cryptodome

**Librairie de sérialisation de fichier utilisée :** yaml

**Suivre les recommandations PEP 8 :** [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

**Message de commit :** suivre le format “Type de modification - Méthode en question”  à raison d’un commit par méthode. Commit sur la branche de la méthode.

**Pour chaque méthode :** créer un header via commentaire pour indiquer sa fonction et éventuellement ses paramètres.

**Arborescence:**

*   **Serveur implémente le traitement**
    *   users
    *   config
    *   main
    *   commands
    *   classes
        *   user
        *   file
        *   folder
*   **Client implémente la CLI**
    *   main
    *   commands:
        *   delete
        *   upload
        *   download
        *   share


## Document d’utilisation

Utiliser les commandes dans le terminal qui contient le client lancé.

Liste des commandes disponibles pour tous les utilisateurs, s’ils disposent des permissions suffisantes :



*   _ls_ : Lister les fichiers dans le dossier de l'utilisateur et les permissions associées pour celui-ci
*   _ls &lt;user>_ : Lister les fichiers du dossier d'un autre utilisateur et le permissions pour l'utilisateur courant
*   _ls &lt;filename>_ : Lister le fichier et les permissions associées pour l'utilisateur courant
*   _put_ _&lt;filename>_ : Envoyer un fichier
    *   _filename_ : nom du fichier
*   _put_ _&lt;user> &lt;filename>_ : Envoyer un fichier dans le dossier d’un autre utilisateur
    *   _filename_ : nom du fichier
*   _get_ _&lt;filename>_ : Télécharger un fichier depuis son répertoire
    *   _filename_ : nom du fichier
*   _get &lt;user> &lt;filename>_ :Télécharger le fichier d’un autre utilisateur
    *   _user_ : nom de l’utilisateur propriétaire du fichier
    *   _filename_ : nom du fichier
*   _rm &lt;filepath>_ : Supprimer un fichier de son répertoire
    *   _filename_ : nom du fichier
*   _perm &lt;user> &lt;add|remove> &lt;c|l|d|r|o> &lt;directory|filename>_ : modifier les permissions sur un fichier ou un dossier pour un utilisateur. 
    *   _user_ : nom de l’utilisateur à qui modifier les permissions
    *   _add/remove_ : Ajouter ou retirer les permissions
    *   _c|l|d|r|o_ : Respectivement les permissions de créer un fichier dans un dossier, de lister un fichier/répertoire, de télécharger un fichier, d’effacer un fichier, et d’écraser un fichier. Il est possible d’en utiliser plusieurs à la fois. On ne peut modifier que les permissions dont on dispose.
    *   _directory|filename_ : nom du fichier ou du répertoire sur lequel appliquer ces permissions.

Le rôle “Utilisateur propriétaire” possède par défaut l’ensemble des permissions sur ses dossiers et fichiers.

Le rôle “Administrateur” possède par défaut les permissions de lister tous les fichiers et répertoires. De plus, il peut donner ou retirer n’importe quelle permission à n’importe quel utilisateur sur des ficiers ou répertoires dont il n'est pas le propriétaire, sauf aux administrateurs (dont lui-même). 
