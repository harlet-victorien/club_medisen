from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QResource
from functions import MainController
from db import Database
from ui_main import UiMainWindow
from db import WebLink

import sys

###################################################################################################################################
###################################################################################################################################
##################################### Fenêtre de l'application avec les intéractions ##############################################
###################################################################################################################################
###################################################################################################################################


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """
        Initialisation de l'ensemble des intéractions, ex: boutons, labels, etc...
        """
        super().__init__()
        self.db = Database()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.resize(1000, 900)
                

        
        self.controller = MainController(self.db,self.ui)
        self.weblink=WebLink()
        QResource.registerResource('resources.rcc')
        self.ui.LIVRE.setCurrentIndex(0)
        #self.controller.LogController.inscription("har","vic","vichar","vichar")
        self.ui.Login_2.clicked.connect(self.controller.try_login)
        self.ui.label_2.setText("")
        

        self.ui.Signup_2.clicked.connect(self.controller.signup)


        self.ui.HomeBtn.clicked.connect(self.controller.go_home)
        self.ui.HomeBtn_2.clicked.connect(self.controller.go_home)
        self.ui.HomeBtn_3.clicked.connect(self.controller.go_home)
        
        self.ui.Quitter_2.clicked.connect(self.controller.close)

        self.ui.ActivitiesBtn.clicked.connect(self.controller.go_activities)
        self.ui.ActivitiesBtn_2.clicked.connect(self.controller.go_activities)
        self.ui.ActivitiesBtn_3.clicked.connect(self.controller.go_activities)

        self.ui.DisconnectBtn.clicked.connect(self.controller.go_login)
        self.ui.DisconnectBtn_2.clicked.connect(self.controller.go_login)
        self.ui.DisconnectBtn_3.clicked.connect(self.controller.go_login)

        self.ui.pushButton.clicked.connect(self.controller.go_login)


        self.ui.TennisBtn.clicked.connect(lambda: (self.controller.setup_planning(1))) 
        self.ui.BasketBtn.clicked.connect(lambda:(self.controller.setup_planning(2)))
        self.ui.HammamBtn.clicked.connect(lambda:(self.controller.setup_planning(3)))
        self.ui.GolfBtn.clicked.connect(lambda:(self.controller.setup_planning(4)))
        self.ui.KayakBtn.clicked.connect(lambda:(self.controller.setup_planning(5)))
        self.ui.JetskiBtn.clicked.connect(lambda:(self.controller.setup_planning(6)))
        self.ui.HikingBtn.clicked.connect(lambda:(self.controller.setup_planning(7)))
        self.ui.MassageBtn.clicked.connect(lambda:(self.controller.setup_planning(8)))

        self.ui.rechercheBtn.clicked.connect(self.controller.recherche)

        self.ui.YoutubeBtn.clicked.connect(lambda:(self.weblink.youtube()))
        self.ui.InstagramBtn.clicked.connect(lambda:(self.weblink.instagram()))
        self.ui.pushButton_4.clicked.connect(lambda:(self.weblink.linkedin()))
        self.ui.twitchBtn.clicked.connect(lambda:(self.weblink.twitch()))



if __name__ == "__main__":
    """
    Lancement de l'application
    """
    app = QtWidgets.QApplication(sys.argv)  
    main_window = MainWindow()  # Créez MyMainWindow
    main_window.show()
    sys.exit(app.exec())  