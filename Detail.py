#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os, sys
import numpy as np


from PyQt5.QtWidgets import (QComboBox, QDoubleSpinBox, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import  \
    FigureCanvasQTAgg as FigureCanvas,          \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

###################################
# Classe  DetailWidget
###################################

class DetailWidget(QWidget):
    ''' Widget de tracé des données brutes d'un fichier d'acquisition
        choisi par sélection des paramètres d'usinage.'''

    def __init__(self, mainWindow):
        '''Le constructeur de la classe DetailWidget reçoit une référence
           sur l'application principale, affectée à l'attribut 'mw'. Cette
           référence est utile pour accéder aux différents onglets de
           l'application et les données associées (listes,
           dictionnaires...).'''

        # exécuter le constructeur de la classe de base :
        QWidget.__init__(self, mainWindow)

        self.mw         = mainWindow
        self.filePath   = None   # le chemin du fichier choisi

        # Les objets utiles aux tracé des courbes :
        self.figure     = Figure()  # figure tracé
        self.axes       = []        # la liste des systèmes d'axes

        # La zone de dessin des tracés matplotlib :
        self.canvas     = FigureCanvas(self.figure)
        # La barre d'outils pour le tracé :
        self.toolbar    = NavigationToolbar(self.canvas, self)

    def AxesSuplot(self, n):
        '''Construit des systèmes d'axes pour <n> tracés les uns en dessous
           des autres.'''

        # Création automatique des n° des subplots :
        # add_subplot(nL,nC,no) où
        #     nL est le nombre de lignes de graphiques
        #     nC est le nombre de colonnes de graphiques
        #     no le numéro du graphique (de haut en bas et de gauche
        #                                à droite)
        self.axes = [self.figure.add_subplot(n,1,i+1) for i in range(n)]


###################################
# Classe  DetailTWidget
###################################

class DetailPWidget(DetailWidget):
    ''' Widget de tracé des données acquises sur une opération de perçage.'''

    def __init__(self, mainWindow):

        # exécuter le constructeur de la classe de base :
        DetailWidget.__init__(self, mainWindow)

        # Boîtes combo :
        self.geomOutils  = QComboBox(self)
        self.materiauxU  = QComboBox(self)
        self.Vc          = QComboBox(self)
        self.F           = QComboBox(self)

        # L'attribut materiau sert à la mémorisation du matériau choisi,
        # qui est indispensable car la liste des valeurs 'Vc' et 'f'
        # qui alimentant les combos dépend du matériau :
        self.materiau    = ""

        # Initialisation des systèmes d'axes de tracé :
        self.AxesSuplot(4)

        # Mise en place des widgets de l'interface GUI :
        self.__initUI()


    def __initUI(self):
        '''Mise en place des widgets de l'interface GUI.'''

        # Adaptation automatique de la largeur des QComboBox à leur contenu :
        self.geomOutils.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #### A FAIRE POUR TOUS LES COMBOS...
        self.materiauxU.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.Vc.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.F.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        # Toute modification du choix d'un QComboBox est associé à la
        # méthode privée <build_file_name> :
        self.materiauxU.addItems(self.mw.metadataTab.listMateriaux)
        self.geomOutils.addItems(self.mw.metadataTab.listGeomOutils)

        #self.geomOutils.activated.connect(self.FillComboBoxes)
        self.materiauxU.activated.connect(self.FillComboBoxes)
        #### A FAIRE POUR TOUS LES COMBOS...

        # Réglages Matplolib :
        self.figure.subplots_adjust(left=0.1,right=0.98,bottom=0.1,\
                                    top=0.95,hspace=0.5)
        # La zone des tracés doit s'adapter à la taille de la fenêtre :
        self.canvas.setSizePolicy(QSizePolicy.Expanding,\
                                  QSizePolicy.Expanding)

        # Le layout du Widget :
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Ligne 1 :
        hbox  = QHBoxLayout()

        label = QLabel("Materiau usiné", self)
        hbox.addWidget(label)
        hbox.addWidget(self.materiauxU)

        label = QLabel("Géométrie outil", self)
        hbox.addWidget(label)
        hbox.addWidget(self.geomOutils)

        label = QLabel("Vc", self)
        hbox.addWidget(label)
        hbox.addWidget(self.Vc)
        label = QLabel("m/mn", self)
        hbox.addWidget(label)

        label = QLabel("F", self)
        hbox.addWidget(label)
        hbox.addWidget(self.F)
        label = QLabel("mm/tour", self)
        hbox.addWidget(label)

        hbox.addStretch()
        vbox.addLayout(hbox)

        # ligne 2
        vbox.addWidget(self.canvas)

        #ligne 3
        vbox.addWidget(self.toolbar)
        vbox.addLayout(hbox)


    def __ForgerNomFichier(self):
        '''Construit le nom du fichier *.txt à visualiser.
           Si l'utilisateur a changé de matériau avec le combo materiaux,
           il faut mettre à jour les valeurs des combo Vc et F qui dépendent
           du matériau sélectionné...
           Une fois le nom du fichier construit (sans oublier le répertoire
           dossierUsin), il faut utiliser la méthode
           <ApplicationUsinage.Lirefichier> pour lire les données du
           fichier.
           LireFichier renvoie un objet SignalPercage qui sait donner les
           valeurs de Fx, Fy, Fz et C pour les tracer dans les 4 systèmes
           d'axes.'''

        ####################################################################
        ######## <Méthode ForgerNomFichier à écrire> #######################
        ####################################################################
        nom_geomOutils=str(self.geomOutils.currentText()) 
        print(nom_geomOutils)
        nom_materiau=str(self.materiauxU.currentText())  
        print(nom_materiau)
        nom_Vc=str(self.Vc.currentText())          
        print(nom_Vc)
        nom_F=str(self.F.currentText())
        print(nom_F)
        
        # Création nom fichier
        #nom_fichier=nom_geomOutils+'-'+nom_materiau+'-Vc'+nom_Vc+'-f'+nom_F+'BCDry.txt'
        nom_fichier=self.mw.metadataTab.BuildFileName(nom_geomOutils, nom_materiau, nom_Vc, nom_F)
        #print(nom_fichier)
        #Création du dossierUsin
        dossierUsin="usinage/P"
        print("test1")
        dossierUsin=self.mw.metadataTab.dossierUsin()
        print("test2")
        print(dossierUsin)
        #self.mw.metadataTab.dossierUsin()
        print(dossierUsin+'/'+'P-'+nom_fichier)
        # Lecture fichier
        print(self.mw.ApplicationUsinage.LireFichier())
        signal=self.mw.ApplicationUsinage.LireFichier(dossierUsin+'/'+nom_fichier,"perçage")
        print(signal)
        self.Fx=signal.Fx()
        self.Fy=signal.Fy()
        self.Fz=signal.Fz()
        self.C=signal.C()
        
        #self.Plot()




        ####################################################################



    def FillComboBoxes(self):
        '''Met à jour le contenu des boîtes combo en utilisant les listes et
           les dictionnaires de l'onglet mw.metadataTab.
           Ne pas oublier de nettoyer les boîtes combo (méthode clear de la
           classe QComboBox ) avant de les remplir avace une nouvelle liste
           de str (méthode addItem de la classe QComboBox).
           Petite difficulté : trier correctement les listes que vous injectez
           dans une boîte combo pour que celle-ci affiche ses items dans le
           bon ordre...
           Quand le travail est fait, on peut appeler la méthode
           ForgerNomFichier.'''

        ####################################################################
        ######## <Méthode ForgerNomFichier à écrire> #######################
        ####################################################################


        self.geomOutils.clear()
        self.Vc.clear()
        self.F.clear()
        self.Vc.addItems(self.mw.metadataTab.dicoMatVc[self.materiauxU.currentText()])
        self.F.addItems(self.mw.metadataTab.dicoMatF[self.materiauxU.currentText()])
        self.geomOutils.addItems(self.mw.metadataTab.listGeomOutils)
        
        self.materiauxU.activated.connect(self.__ForgerNomFichier)
        self.geomOutils.activated.connect(self.__ForgerNomFichier)
        self.Vc.activated.connect(self.__ForgerNomFichier)
        self.F.activated.connect(self.__ForgerNomFichier)
            #Petite difficulté : trier correctement les listes que vous injectez
           #dans une boîte combo pour que celle-ci affiche ses items dans le
           #bon ordre... Pas compris

        ####################################################################


    def Plot(self):
        '''Tracer les composantes Fx, Fy, Fz  de la force et le couple.
           - commencer par effacer les tracés (méthode clear utilisée avec
             les axes de la liste self.axes),
           - rafraîchir avec la méthode draw de self.canvas,
           - puis faire les tracés avec la méthode plot, qui fonctionne avec
             les axes comme avec matplotlib.pyplot.
           - ne pas oublier de faire afficher les nouveaux tracés avec la
             la méthode draw de self.canvas.'''

        ####################################################################
        ######## <Méthode Plot à écrire> #######################
        ####################################################################

        Datas = (self.Fx,self.Fy,self.Fz,self.C)
        Legende=("FX","FY","FZ","C")
        for (axes,Y,L) in zip(self.axes,Datas,Legende):
            axes.clear()
            axes.canvas.draw()
            axes.plot(T,Y)
            axes.label(L)
            




        ####################################################################




###################################
# Classe  DetailTWidget
###################################

class DetailTWidget(DetailWidget):
    ''' Widget de tracé des données acquises sur une opération de tournage.'''
    def __init__(self, mainWindow):

        # exécuter le constructeur de la classe de base :
        DetailWidget.__init__(self, mainWindow)

        # Boîtes combo :
        self.Outils      = QComboBox(self)
        self.materiauxU  = QComboBox(self)
        self.Vc          = QComboBox(self)
        self.F           = QComboBox(self)
        self.ap          = QComboBox(self)
        # L'attribut materiau sert à la mémorisation du matériau choisi,
        # qui est indispensable car la liste des valeurs 'Vc' et 'f'
        # qui alimentant les combos dépend du matériau :
        self.materiau    = ""

        # Initialisation des systèmes d'axes de tracé :
        self.AxesSuplot(4)

        # Mise en place des widgets de l'interface GUI :
        self.__initUI()


    def __initUI(self):
        '''Mise en place des widgets de l'interface GUI.'''

        # Adaptation automatique de la largeur des QComboBox à leur contenu :
        self.Outils.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #### A FAIRE POUR TOUS LES COMBOS...
        self.materiauxU.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.Vc.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.F.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.ap.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        # Toute modification du choix d'un QComboBox est associé à la
        # méthode privée <build_file_name> :
        self.materiauxU.addItems(self.mw.metadataTab.listMateriaux)
        self.Outils.addItems(self.mw.metadataTab.listOutils)

        #self.geomOutils.activated.connect(self.FillComboBoxes)
        self.Outils.activated.connect(self.FillComboBoxes)
        #### A FAIRE POUR TOUS LES COMBOS...

        # Réglages Matplolib :
        self.figure.subplots_adjust(left=0.1,right=0.98,bottom=0.1,\
                                    top=0.95,hspace=0.5)
        # La zone des tracés doit s'adapter à la taille de la fenêtre :
        self.canvas.setSizePolicy(QSizePolicy.Expanding,\
                                  QSizePolicy.Expanding)

        # Le layout du Widget :
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Ligne 1 :
        hbox  = QHBoxLayout()

        label = QLabel("Materiau usiné", self)
        hbox.addWidget(label)
        hbox.addWidget(self.materiauxU)

        label = QLabel("Outil utilisé", self)
        hbox.addWidget(label)
        hbox.addWidget(self.Outils)

        label = QLabel("Vc", self)
        hbox.addWidget(label)
        hbox.addWidget(self.Vc)
        label = QLabel("m/mn", self)
        hbox.addWidget(label)

        label = QLabel("F", self)
        hbox.addWidget(label)
        hbox.addWidget(self.F)
        label = QLabel("mm/tour", self)
        hbox.addWidget(label)

        label = QLabel("Ap", self)
        hbox.addWidget(label)
        hbox.addWidget(self.ap)
        label = QLabel("mm", self)
        hbox.addWidget(label)
        
        hbox.addStretch()
        vbox.addLayout(hbox)

        # ligne 2
        vbox.addWidget(self.canvas)

        #ligne 3
        vbox.addWidget(self.toolbar)
        vbox.addLayout(hbox)


    def __ForgerNomFichier(self):
        '''Construit le nom du fichier *.txt à visualiser.
           Si l'utilisateur a changé de matériau avec le combo materiaux,
           il faut mettre à jour les valeurs des combo Vc et F qui dépendent
           du matériau sélectionné...
           Une fois le nom du fichier construit (sans oublier le répertoire
           dossierUsin), il faut utiliser la méthode
           <ApplicationUsinage.Lirefichier> pour lire les données du
           fichier.
           LireFichier renvoie un objet SignalPercage qui sait donner les
           valeurs de Fx, Fy, Fz et C pour les tracer dans les 4 systèmes
           d'axes.'''

        ####################################################################
        ######## <Méthode ForgerNomFichier à écrire> #######################
        ####################################################################
        nom_geomOutils=str(self.Outils.currentText()) 
        print(nom_geomOutils)
        nom_materiau=str(self.materiauxU.currentText())  
        print(nom_materiau)
        nom_Vc=str(self.Vc.currentText())          
        print(nom_Vc)
        nom_F=str(self.F.currentText())
        print(nom_F)
        nom_ap=str(self.ap.currentText())
        # Création nom fichier
        #nom_fichier=nom_geomOutils+'-'+nom_materiau+'-Vc'+nom_Vc+'-f'+nom_F+'Dry.txt'
        nom_fichier=self.mw.metadataTab.BuildFileName(nom_geomOutils, nom_materiau, nom_Vc, nom_F, nom_ap)
        print(nom_fichier)
        #Création du dossierUsin
        dossierUsin="usinage/T"
        dossierUsin=self.mw.metadataTab.dossierUsin()
        
        #self.mw.metadataTab.dossierUsin()
        print(dossierUsin+'/'+'T-'+nom_fichier)
        # Lecture fichier
        print(self.mw.ApplicationUsinage.LireFichier())
        signal=self.mw.ApplicationUsinage.LireFichier(dossierUsin+'/'+nom_fichier,"tournage")
        print(signal)
        self.Fx=signal.Fx()
        self.Fy=signal.Fy()
        self.Fz=signal.Fz()
        self.C=signal.C()
        
        #self.Plot()




        ####################################################################



    def FillComboBoxes(self):
        '''Met à jour le contenu des boîtes combo en utilisant les listes et
           les dictionnaires de l'onglet mw.metadataTab.
           Ne pas oublier de nettoyer les boîtes combo (méthode clear de la
           classe QComboBox ) avant de les remplir avace une nouvelle liste
           de str (méthode addItem de la classe QComboBox).
           Petite difficulté : trier correctement les listes que vous injectez
           dans une boîte combo pour que celle-ci affiche ses items dans le
           bon ordre...
           Quand le travail est fait, on peut appeler la méthode
           ForgerNomFichier.'''

        ####################################################################
        ######## <Méthode ForgerNomFichier à écrire> #######################
        ####################################################################


        self.Vc.clear()
        self.F.clear()
        self.ap.clear()
        self.Vc.addItems(self.mw.metadataTab.dicoOutilVc[self.Outils.currentText()])
        self.F.addItems(self.mw.metadataTab.dicoOutilF[self.Outils.currentText()])
        self.ap.addItems(self.mw.metadataTab.dicoOutilAp[self.Outils.currentText()])
        #self.materiauxU.addItems(self.mw.metadataTab.listGeomOutils)
        
        self.materiauxU.activated.connect(self.__ForgerNomFichier)
        self.Outils.activated.connect(self.__ForgerNomFichier)
        self.Vc.activated.connect(self.__ForgerNomFichier)
        self.F.activated.connect(self.__ForgerNomFichier)
        self.ap.activated.connect(self.__ForgerNomFichier)
            #Petite difficulté : trier correctement les listes que vous injectez
           #dans une boîte combo pour que celle-ci affiche ses items dans le
           #bon ordre... Pas compris

        ####################################################################

        


    def Plot(self):
        '''Tracer les composantes Fx, Fy, Fz  de la force et le couple.
           - commencer par effacer les tracés (méthode clear utilisée avec
             les axes de la liste self.axes),
           - rafraîchir avec la méthode draw de self.canvas,
           - puis faire les tracés avec la méthode plot, qui fonctionne avec
             les axes comme avec matplotlib.pyplot.
           - ne pas oublier de faire afficher les nouveaux tracés avec la
             la méthode draw de self.canvas.'''

        ####################################################################
        ######## <Méthode Plot à écrire> #######################
        ####################################################################
#créer la lsite de temps
        Datas = (self.Fx,self.Fy,self.Fz,self.C)
        Legende=("FX","FY","FZ","C")
        for (axes,Y,L) in zip(self.axes,Datas,Legende):
            axes.clear()
            axes.canvas.draw()
            axes.plot(T,Y)
            axes.label(L)
            

        ####################################################################
        ######## classe à écrire par copier/coller/modifier
        ######## de la classe DetailPWidget.
        ####################################################################




