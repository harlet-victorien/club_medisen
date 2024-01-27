import mysql.connector as mc
import hashlib
import webbrowser
import globals



###################################################################################################################################
###################################################################################################################################
##################################### Fonctions de récupération d'informations via la database ####################################
###################################################################################################################################
###################################################################################################################################


class Database ():
    """
    Classe utilisée pour la manipulation de la BDD
    """
    def __init__(self):
        self.conn = mc.connect(host="mysql-projetbalne.alwaysdata.net", user="344603", password="cacaprout", database="projetbalne_bdd")
        self.cursor = self.conn.cursor()

    
    
    def get_client_info(self,id):
        """
        Récupère les infos d'un client
        """
        self.cursor.execute("SELECT * FROM Clients WHERE IdClients=%s;", (int(id),))
        result = self.cursor.fetchall()
        if result == []:
            return None
        return result[0]
    


    def get_lieu_activite(self,id) :
        """
        Récupère le lieu de l'activité
        """
        self.cursor.execute("SELECT Lieu.Adresse FROM Lieu "
                       "INNER JOIN Activites ON Activites.IdLieu=Lieu.IdLieu "
                       "WHERE Activites.IdActivite=%s ", (int(id),))
        
        return self.cursor.fetchall()[0][0]
    


    def get_horaires_activite(self,id) :
        """
        Récupère la date, hdebut, hfin d'une activité en fonction de son id
        """
        self.cursor.execute("SELECT Date, Hdebut, Hfin FROM Activites "
                       "WHERE IdActivite=%s ;", (int(id),))
        resultat = self.cursor.fetchall()
        if resultat :
            datesql = resultat[0][0]
            Hdebut = resultat[0][1]
            Hfin = resultat[0][2]
            date_formatee = datesql.strftime('%d-%m-%Y')
            Hdebut_formatee = str(Hdebut)
            Hfin_formatee = str(Hfin)
            Hdebut_formatee = Hdebut_formatee[0:5]
            Hfin_formatee = Hfin_formatee[0:5]
            return date_formatee, Hdebut_formatee, Hfin_formatee
        else:
            return None


    
    def get_prix_activite(self,id) :
        """
        Récupère prix d'une activité
        """
        self.cursor.execute("SELECT PrixAdulte, PrixEnfant FROM Activites "
                       "WHERE Activites.IdActivite=%s ", (int(id),))
        return self.cursor.fetchall()[0]



    def get_ind_act(self,id):
        """
        Regarde les activités où le client est inscrit et les trie par date et heure de début
        """
        self.cursor.execute("SELECT * FROM Activites " 
                    "INNER JOIN Réservations ON Réservations.IdActivite=Activites.IdActivite "
                    "INNER JOIN Clients ON Réservations.IdClients=Clients.IdClients "
                    "WHERE Clients.IdClients=%s "
                    "ORDER BY Date, Hdebut;", (int(id),))
        RESULT=self.cursor.fetchall()
        if RESULT==[]:
            return []
        return RESULT



    def get_places_dispo(self,id):
        """
        Fonction qui regarde s'il reste des places disponibles
        """
        self.cursor.execute("SELECT NombreAdulte,NombreEnfant FROM Activites " 
                    "WHERE IdActivite=%s;", (int(id),))
        nb_adulte, nb_enfant = self.cursor.fetchall()[0]

        self.cursor.execute("SELECT Réservations.NombreAdultes,Réservations.NombreEnfant FROM Activites " 
                    "INNER JOIN Réservations ON Réservations.IdActivite=Activites.IdActivite "
                    "WHERE Réservations.IdActivite=%s;", (int(id),))
        nb_adulte_res, nb_enfant_res = self.cursor.fetchall()[0]

        adulte_dispo = int(nb_adulte) - int(nb_adulte_res)
        enfant_dispo = int(nb_enfant) - int(nb_enfant_res)

        return  (adulte_dispo, enfant_dispo)



    def get_act_day_by_type(self,id):
        """
        Récupère les activités du jour et les tries par heure de début
        """
        self.cursor.execute("SELECT * FROM Activites WHERE Date = CURDATE() AND IdType=%s ORDER BY HDebut;", (int(id),))
        RESULT=self.cursor.fetchall()
        if RESULT==[]:
            return None
        return RESULT
    


    def get_nbre(self,id):
        """
        Récupère le nombre d'adulte et le nombre d'enfant d'une reservation et calcule le prix total de la reservation
        """
        self.cursor.execute("SELECT NombreAdultes, NombreEnfant FROM Réservations WHERE IdActivite=%s;", (int(id),))
        resultat = self.cursor.fetchone()
        prix = self.get_prix_activite(id)
        if resultat and prix is not None and len(prix) == 2:
            nombre_adultes = resultat[0]
            nombre_enfant = resultat[1]

            prix_adulte = prix[0]
            prix_enfant = prix[1]

            total = nombre_adultes * prix_adulte + nombre_enfant * prix_enfant
            return resultat, total
        else:
            return None, 0
 
  

    def get_act_info(self,id):
        """
        Récupère toutes les informations des activités
        """
        self.cursor.execute("SELECT * FROM Activites WHERE IdActivite=%s;", (int(id),))
        result = self.cursor.fetchall()
        if result == []:
            return None
        return result[0]



    def get_type_table(self):
        """
        Récupère tous les types d'activités
        """
        self.cursor.execute("SELECT * FROM Type")
        result = self.cursor.fetchall()
        if result == []:
            return None
        return result


   
    def get_mails(self):
        """
        Récupères tous les mails
        """
        self.cursor.execute("SELECT Mail FROM Login")
        result = self.cursor.fetchall()
        if result == []:
            return None
        mails = []
        for mail in result:
            mails.append(mail[0])


        return mails
    


    def reservation(self, id_activite, id_client, nb_adulte, nb_enfant):
        """
        Fonction utilisée pour enregistrer une réservation dans la BDD
        """
        self.cursor.execute("SELECT NombreAdulte, NombreEnfant FROM Activites WHERE IdActivite=%s;", (int(id_activite),))
        result = self.cursor.fetchone()
        if result is None:
            return "Activité non trouvée"

        current_nb_adulte, current_nb_enfant = result

        # Vérifier si suffisamment de places sont disponibles
        if current_nb_adulte < nb_adulte or current_nb_enfant < nb_enfant:
            return "Pas assez de places disponibles"

        # Mettre à jour le nombre de places
        new_nb_adulte = current_nb_adulte - nb_adulte
        new_nb_enfant = current_nb_enfant - nb_enfant
        self.cursor.execute("UPDATE Activites SET NombreAdulte=%s, NombreEnfant=%s WHERE IdActivite=%s;", (new_nb_adulte, new_nb_enfant, int(id_activite)))

        # Insérer la réservation
        self.cursor.execute("INSERT INTO Réservations (IdActivite, IdClients, NombreAdulte, NombreEnfant) VALUES (%s, %s, %s, %s);", (id_activite, id_client, nb_adulte, nb_enfant))
        self.conn.commit()



    def recherche_activite(self,id_type, date, nb_adulte, nb_enfant):
        """
        Fonction utilisée pour rechercher une activité avec la date, le nombre de personne et le type d'activité
        """
        self.cursor.execute("""
        SELECT * FROM Activites 
        WHERE IdType = %s AND Date = %s AND NombreAdulte >= %s AND NombreEnfant >= %s;
        """, (id_type, date, nb_adulte, nb_enfant))

        activities = self.cursor.fetchall()

        if not activities:
            return []

        return activities



    def close(self):
        """
        Fonction utilisé pour fermer la connexion à la BDD
        """
        self.cursor.close()
        self.conn.close()



####################################################################################################################################
####################################################################################################################################
########################################### Controlleur de la page (Login et Signup) ###############################################
####################################################################################################################################
####################################################################################################################################


class LoginController():

    """
    Control de la page de login
    """

    def __init__(self,db):
        self.db = db



    def login(self, mail, motdepasse):
        """
        Fonction permettant de se connecter à l'application
        """
        self.db.cursor.execute("SELECT IdClients FROM Login WHERE Mail=%s AND MotDePasse=%s;", (mail,self.hashage(motdepasse)))
        RESULT=self.db.cursor.fetchall()
        if RESULT==[]:
            return None
        return RESULT[0][0]



    def hashage(self,motdepasse):
        """
        Fonction permettant de hasher le mot de passe
        """
        hacheur = hashlib.sha256()
        hacheur.update(motdepasse.encode('utf-8'))
        motdepassecrypte = hacheur.hexdigest()
        return motdepassecrypte



    def inscription(self, nom, prenom, mail, motdepasse):
        """
        Fonction permetant d'inscrire une personne dans la BDD
        """
        if mail in globals.MAILS:
            return 'Error'
        self.db.cursor.execute("INSERT INTO Clients (Nom, Prenom) VALUES (%s, %s);", (nom,prenom))
        self.db.cursor.execute("SELECT IdClients FROM Clients WHERE Nom=%s AND Prenom=%s;", (nom,prenom))
        id = self.db.cursor.fetchall()[0][0]
        self.db.cursor.execute("INSERT INTO Login (IdClients, Mail, MotDePasse) VALUES (%s, %s, %s);", (id,mail,self.hashage(motdepasse)))
        self.db.conn.commit()
        globals.MAILS.append(mail)
        return id

####################################################################################################################################
####################################################################################################################################
########################################### Controlleur des links webs #############################################################
####################################################################################################################################
####################################################################################################################################



class WebLink ():
    """
    Fonction pour les liens des icônes sur la page d'accueil
    """
    def __init__(self):
        pass



    def youtube(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)



    def instagram(self):
        url = "https://www.instagram.com/flxhlt/"
        webbrowser.open(url)

    
    
    def twitch(self):
        url = "https://www.twitch.tv/squeezie"
        webbrowser.open(url)   
    
    
    
    def linkedin(self):
        url = "https://www.linkedin.com/in/victorien-harlet-969b30267/"
        webbrowser.open(url)
        url = "https://www.linkedin.com/in/baptiste-bera/"
        webbrowser.open(url)