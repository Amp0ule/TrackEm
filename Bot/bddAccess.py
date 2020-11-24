import mysql.connector as mc



def getListConnected(cursor): #
    """ Cette fonction renvoie la liste des personnes connectées """
    cursor.execute("SELECT Name, Adresse_Mac FROM utilisateurs JOIN informations ON id_utilisateur = id WHERE is_connected = 1")
    rows = cursor.fetchall()
    listOfConnected = []       # initiation de la liste des utilisateurs connectés
    for row in rows:
        listOfConnected.append([row[0], row[1]])      # les indices sont spécifiques à l'ordre des colonnes de notre bdd. [0] = nom, [1] = adresse mac
    return listOfConnected



def getListOfUnknownConnected(cursor):
    """ Cette fonction renvoie la liste des personnes inconnues connectées """
    cursor.execute("SELECT Name, Adresse_Mac FROM utilisateurs WHERE Name = {}".format("Unknown"))
    rows = cursor.fetchall()
    listOfUnknownConnected = []
    for row in rows:
        if(row[1] == "Unknown"):
            listOfUnknownConnected.append([row[0], row[1]])
    return listOfUnknownConnected



def isConnected(cursor, name):
    """ Cette fonction renvoie un booléen True/False en fonction de si la personne en entrée est connectée ou non """
    cursor.execute("SELECT utilisateurs.Name, informations.is_connected FROM utilisateurs JOIN informations ON utilisateurs.id = informations.id_utilisateur WHERE is_connected = 1")
    rows = cursor.fetchall()
    isConnected = 0
    for row in rows:
        if row[0] == name:          # [0] = id du nom ici
            isConnected = row[1]    # 

    if isConnected == 0:
    	isConnected = False
    else:
    	isConnected = True

    return isConnected



def getNumberOfConnected(cursor):
    """ Cette fonction renvoie le nombre de personnes connectée """
    cursor.execute("SELECT SUM(id_utilisateur) FROM informations WHERE is_connected = 1")
    rows = cursor.fetchall()
    numberOfConnected = 0;

    if rows[0][0] != None:
    	numberOfConnected = rows[0][0]

    return numberOfConnected



def whoIsDisconnected(cursor):
    """ Cette fonction renvoie la liste des personnes qui ne sont pas connectées """
    cursor.execute("SELECT utilisateurs.Name FROM utilisateurs JOIN informations ON utilisateurs.id = informations.id_utilisateur WHERE is_connected = 0")
    rows = cursor.fetchall()
    disconnected = []           #initialisation de la liste des déconnectés.
    for row in rows:
        disconnected.append(row[0])

    return disconnected



def getNumberOfDisconnected(cursor):
    """ Cette fonction renvoie le nombre de personne qui ne sont pas connectées """
    cursor.execute('SELECT SUM(id_utilisateur) FROM informations  WHERE is_connected = 0')
    rows = cursor.fetchall()
    numberOfDisconnected = 0;
    
    if rows[0][0] != None:
    	numberOfDisconnected = rows[0][0]

    return numberOfDisconnected



def getNumberOfPeopleSave(cursor):
    """ Cette fonction renvoie le nombre de personnes sauvegardées """
    cursor.execute("SELECT SUM(id) FROM utilisateurs")
    rows = cursor.fetchall() # renvoie une matrice contenant tous les éléments de la bdd obtenue après l'exécution le requête effectuée plus haut.

    return rows[0][0]



#conn = mc.connect(host="localhost", user="root", password="", database= "trackem")
#cursor = conn.cursor()  #fonction dans la librairy dans la mysql elle permet d'exécuter des requêtes SQL
# CODE 
# cursor.close()
# conn.close()