from db import Database, LoginController
from PyQt6.QtCore import QDate
import globals
from PyQt6.QtCore import QTimer
from ui_CustomButton import Scroll_button


class MainController():
    def __init__(self, db,ui):
        self.db = db
        self.ui = ui
        self.LogController= LoginController(self.db)
        self.timer = QTimer()
        
    def create_act_day_by_type(self, idtype, date, nb_adult, nb_children):
        #make previous widgets disappear
        
        while self.ui.verticalLayout_16.count():
            child = self.ui.verticalLayout_16.takeAt(0)
            if child.widget():
                child.widget().deleteLater()





        globals.ACT_BY_DAY_BY_TYPE = self.db.recherche_activite(idtype, date, nb_adult, nb_children)
        if globals.ACT_BY_DAY_BY_TYPE == []:
            
            #créer un bandeau pour dire qu'il n'y a pas d'activité ce jour là
            ########### A FAIRE #############






            pass
        else:
            for act in globals.ACT_BY_DAY_BY_TYPE:
                print(act[0])
                #créer les bandeaux pour chaque activité du jour
                #Scroll_button(self.ui.scrollAreaWidgetContents_3, self.ui.verticalLayout_16,hdébut,hfin,adresse,PriceAdult,PriceChild,PlaceAvailableAdult,PlaceAvailableChild):

                button=Scroll_button(self.ui.scrollAreaWidgetContents_3,self.ui.verticalLayout_16,self.db.get_horaires_activite(act[0])[1],self.db.get_horaires_activite(act[0])[2],self.db.get_lieu_activite(act[0]), act[2], act[3], act[8], act[9], act[0])
                button.pushButton.hide()
                button.toolButton.clicked.connect(lambda: button.pushButton.show())
                button.pushButton.clicked.connect(lambda: (button.pushButton.hide(),self.register_for_act(act[0])))



    def create_act_by_ind_registered(self, id):

        #make previous widgets disappear
        while self.ui.verticalLayout_13.count():
            child = self.ui.verticalLayout_13.takeAt(0)
            if child.widget():
                child.widget().deleteLater()




        globals.ACT_BY_IND_REGISTERED = self.db.get_ind_act(id)
        if globals.ACT_BY_IND_REGISTERED == []:
            #créer un bandeau pour dire qu'il n'est pas inscrit à aucune activité
            ########### A FAIRE #############
            pass
        else:
            for act in self.db.get_ind_act(id):
                print(act[0])
                #créer les bandeaux pour chaque activité à laquelle il est inscrit
                
                #Scroll_button(self.ui.scrollAreaWidgetContents, self.ui.verticalLayout_13,hdébut,hfin,adresse,PriceAdult,PriceChild,PlaceAvailableAdult,PlaceAvailableChild):
                for info in act:
                    info = str(info)
                button=Scroll_button(self.ui.scrollAreaWidgetContents,self.ui.verticalLayout_13,self.db.get_horaires_activite(act[0])[1],self.db.get_horaires_activite(act[0])[2],self.db.get_lieu_activite(act[0]), act[2], act[3], act[8], act[9], act[0])
                button.pushButton.hide()

    def register_for_act(self, id_act):
        #enregistrer l'utilisateur à l'activité
        self.db.reservation(id_act, globals.ID_USER, self.ui.spinbox_adultes.value(), self.ui.spinbox_enfants.value())
        self.create_act_day_by_type(globals.ID_TYPE_SELECTED, self.ui.calendrieract.selectedDate().toPyDate(), self.ui.spinbox_adultes.value(), self.ui.spinbox_enfants.value())






    def refresh(self):
        #refresh les bandeaux

        



        ########### A FAIRE #############                  
        pass

    def go_home(self):
        self.ui.LIVRE.setCurrentIndex(2)
        print(globals.ID_USER)
        self.create_act_by_ind_registered(globals.ID_USER)
        print(globals.MAILS)
        
    def try_login(self):
        username = str(self.ui.emaillog_2.text())
        password = str(self.ui.mdplog_2.text())
        answer = self.LogController.login(username, password)
        print(answer)
        if answer == None:
            self.ui.label_2.setText("Wrong Password or Email ! ")
            self.timer.singleShot(2000, lambda: self.ui.label_2.setText(""))
        else:
            
            RESULT=self.db.get_client_info(answer)
            self.setup_data(RESULT)
            
            self.ui.nomprenomlabel.setText(f"{globals.PRENOM_USER} {globals.NOM_USER}")
            self.ui.nomprenomlabel_2.setText(f"{globals.PRENOM_USER} {globals.NOM_USER}")
            self.ui.nomprenomlabel_3.setText(f"{globals.PRENOM_USER} {globals.NOM_USER}")
            self.go_activities()
    def go_activities(self):
        self.ui.LIVRE.setCurrentIndex(3)
    
    def go_login(self):
        self.ui.LIVRE.setCurrentIndex(1)
        self.ui.emaillog_2.setText("")
        self.ui.mdplog_2.setText("")
        self.ui.prenom_2.setText("")
        self.ui.nom_2.setText("")
        self.ui.emailsu_2.setText("")
        self.ui.mdpsu_2.setText("")
        self.ui.textevert.setText("")
        self.reset_data()

    def go_planning(self):
        self.ui.LIVRE.setCurrentIndex(4)



    def signup(self):
        globals.MAILS=self.db.get_mails()
        print(globals.MAILS)
        PRENOM=str(self.ui.prenom_2.text())
        NOM=str(self.ui.nom_2.text())
        MAIL=str(self.ui.emailsu_2.text())
        MDP=str(self.ui.mdpsu_2.text())
        RESULT = self.LogController.inscription(PRENOM,NOM,MAIL,MDP)
        if RESULT=='Error':
            self.ui.prenom_2.setText("")
            self.ui.nom_2.setText("")
            self.ui.emailsu_2.setText("")
            self.ui.mdpsu_2.setText("")
            self.ui.textevert.setStyleSheet("color:red;background-color: none;")
            self.ui.textevert.setText("Mail already used !")
            self.timer.singleShot(2000, lambda: self.ui.textevert.setText(""))
        else:
            self.ui.prenom_2.setText("")
            self.ui.nom_2.setText("")
            self.ui.emailsu_2.setText("")
            self.ui.mdpsu_2.setText("")
            self.ui.textevert.setStyleSheet("color:rgb(0, 255, 127);background-color: none;")
            self.ui.textevert.setText("You can now log in !")
            self.timer.singleShot(2000, lambda: self.ui.textevert.setText(""))

    def setup_data(self,RESULT):
        globals.TYPE_TABLE=self.db.get_type_table()
        globals.MAILS=self.db.get_mails()
        globals.PRENOM_USER=RESULT[2]
        globals.NOM_USER=RESULT[1]
        globals.ID_USER=RESULT[0]

    def reset_data(self):
        globals.TYPE_TABLE=[]
        globals.MAILS=[]
        globals.PRENOM_USER=""
        globals.NOM_USER=""
        globals.ID_USER=0

    def setup_planning(self, id):
        globals.ID_TYPE_SELECTED = id
        self.ui.TITREACT_label.setText(f"{ globals.TYPE_TABLE[globals.ID_TYPE_SELECTED-1][1]}")
        self.create_act_day_by_type(globals.ID_TYPE_SELECTED, QDate.currentDate().toPyDate(), 1, 0)
        self.go_planning()

    def recherche(self):
        Qdate = self.ui.calendrieract.selectedDate()
        DATE = Qdate.toPyDate()
        NB_ADULT = self.ui.spinbox_adultes.value()
        NB_CHILDREN = self.ui.spinbox_enfants.value()
        #self.refresh()                     #TODO
        self.create_act_day_by_type(globals.ID_TYPE_SELECTED, DATE, NB_ADULT, NB_CHILDREN)



    def close(self):
        self.ui.LIVRE.setCurrentIndex(0)