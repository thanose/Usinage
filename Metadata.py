#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)


###################################
# Classe  MetadataWidget
###################################

class MetadataWidget(QWidget):

    def __init__(self, mainWindow):

        # exécuter le constructeur de la classe de base :
        QWidget.__init__(self, mainWindow)

        '''Le constructeur de la classe MetadataWidget reçoit une référence
           sur l'application principale, affectée à l'attribut 'mw'. Cette
           référence est utile pour accéder aux différents onglets de l'appli-
           cation et les données associées (listes, dictionnaires...).'''

        self.mw              = mainWindow

        # Le tableau des noms de fichiers et des paramètres usinages déduits
        # des noms :
        self.table           = QTableWidget(self)
        self.__listMateriaux = []   # materiaux trouvés dans les noms fichiers

        # Le bouton pour lancer le scan du répertoire choisi:
        self.btn_scanFiles   = QPushButton("Scan Fichiers", self)

        # Les widgets pour choisir et afficher le répertoire à scanner :
        self.labelUsinage    = QLabel("Dossier usinage", self)
        self.dossierUsinage  = QLineEdit(self.mw.usinage_dir, self)
        self.choisirDossierU = QPushButton("...", self)

        # La liste des fichiers *.txt de perçage/tournage  trouvés dans le
        # répertoire renvoyé par 'dossierUsin' :
        self.listeFichiers   = []

        # connecter le clic des widgets aux méthodes de la classe :
        self.ConnectWidgetsToMethods()

    @property
    def listMateriaux(self) : return self.__listMateriaux.copy()

    def set_listMateriaux(self,new_list) :
        self.__listMateriaux = new_list

    @property
    def dossierUsin(self):
        '''Le répertoire dans lequel sont cherchés les fichiers de mesure
           *.txt'''
        return self.dossierUsinage.text()

    @dossierUsin.setter
    def dossierUsin(self, dir_name):
        self.dossierUsinage.setText(dir_name)

    def ChoixDossier(self, currDir, operation):
        '''Lance un navigateur pour choisir l\'emplacement du dossier
           contenant les fichiers d'acquisition *.txt.'''

        mess = 'Choix du dossier <usinage> ' + operation
        dir_name = QFileDialog.getExistingDirectory(None,
                                                    mess,
                                                    currDir)
        if dir_name != '' :
            # un répertoire valide a été choisi :
            self.dossierUsin = dir_name  # MAJ du label
            self.ClearTable()         # effacer le tableau


    def ListerTxt(self, dossierU):
        '''Affecte à l'attribut 'listeFichiers' la liste triée des
           fichiers *.txt contenus dans le répertoire dossierU passé en
           argument.'''
        ####################################################################
        ######## <Méthode ListerTxt à écrire> ##############################
        ####################################################################






        ####################################################################

    def ResizeTableColums(self):
        '''Met à jour la largeur des colonnes du tableau des fichiers en
           fonction des contenus des colonnes.'''
        for c in range(self.table.columnCount()):
            self.table.resizeColumnToContents(c)

    def ClearTable(self):
        '''Efface les données du tableau des fichiers.'''
        self.table.clearContents()

    def ListerFichiers(self):
        '''Scanne le répertoire choisi pour trouver les fichiers *.txt, efface
           le tableau et le remplit avec les nouvelles informations obtenues
           avec les noms des fichiers.'''
        self.ClearTable()
        self.ListerTxt(self.dossierUsin)
        self.RemplirTable()
        self.ResizeTableColums()

    def ConnectWidgetsToMethods(self):
        '''Connecte les actions des widgets (QPushButton, QTableWidget...)
           aux méthodes appropriées.'''

        mess  = 'Liste les fichiers *.txt de perçage'
        mess += 'contenus dans le dossier choisi.'
        self.btn_scanFiles.setToolTip(mess)
        self.btn_scanFiles.clicked.connect(self.ListerFichiers)

        mess  = 'Lance un navigateur pour choisir l\'emplacement du dossier'
        mess += ' de travail.'
        self.choisirDossierU.setToolTip(mess)
        self.choisirDossierU.clicked.connect(self.ChoixDossier)

        self.table.setSortingEnabled(True)


######################################
#   Classe dérivée  MetadataPWidget  #
######################################

class MetadataPWidget(MetadataWidget):
    '''Cette classe correspond à l'onglet d'analyse du répertoire contenant les
       fichiers *.txt de perçage.'''

    @staticmethod
    def BuildFileName (go, m, Vc, F):
        '''Construit un nom de fichier perçage avec les paramètres passés,
           conformément à la règle de nommage (cf document TP perçage) :
           "P-référence outil-matière usinée-Vcxxx-fx.xxxx-BCDry.txt".
           go : géométrie
           m  : matériau
           Vc : vitesse de coupe
           F  : avance par tour.
           Tous les arguments sont des chaînes de caractères.'''
        name = "P-{}-{}-Vc{}-f{}-BCDry.txt".format(go,m,Vc,F)
        return name

    def __init__(self, mainWindow):

        # exécuter le constructeur de la classe de base :
        MetadataWidget.__init__(self, mainWindow)

        self.__operation     = 'perçage'
        self.__nomColonnes   = ['Fichier', 'GéométrieOutil', 'Matériau usiné',
                              'Vc [m/min]', 'f [mm/tour]']

        self.__listGeomOutils= []  # géométries trouvées dans les noms fichiers
        self.__dicoMatVc     = {}  # dictionnaire des 'vitesse de coupe'
                                   # par matériau
        self.__dicoMatF      = {}  # dictionnaire des 'avance par tour' par
                                   # matériau

        # initialiser l'attribut dossierUsinage de la classe de Base :
        self.dossierUsin = self.mw.usinage_dir + '/P'

        # Mise en place des widgets de l'interface GUI :
        self.__initUI()

        ############# INITIALISATION FORCEE ###############################
        #
        #  Initialisation forcée des listes et dictionnaires des classes.
        #
        #  Permet aux autres classes de ne pas être bloquées et d'accéder
        #  aux listes et aux dictionnaires en attendant que cette classe
        #  soit totalement opérationnelle...
        #
        ###################################################################
        self.INIT_FORCEE()
        ###################################################################

    def INIT_FORCEE(self):
        self.set_listMateriaux(['2017AT4', '45NiCrMo16Recuit'])
        self.__listGeomOutils = ['Geometrie1Foret1', 'Geometrie2Foret1']
        self.__dicoMatVc      = {'2017AT4' : ['44','52'],
                               '45NiCrMo16Recuit': ['15','18']}
        self.__dicoMatF       = {'2017AT4' : ['0.04','0.05'],
                               '45NiCrMo16Recuit' : ['0.04','0.05']}


    @property
    def listGeomOutils(self): return self.__listGeomOutils.copy()

    @property
    def dicoMatVc(self): return self.__dicoMatVc.copy()

    @property
    def dicoMatF(self): return self.__dicoMatF.copy()

    def ChoixDossier(self):
            currDir = self.mw.usinage_dir + '/P'
            MetadataWidget.ChoixDossier(self, currDir, self.__operation)

    def __initUI(self):
        '''Mise en place des widgets de l'interface GUI.'''

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Ligne 1
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_scanFiles)
        hbox.addStretch()
        hbox.addWidget(self.labelUsinage)
        hbox.addWidget(self.dossierUsinage)
        hbox.addWidget(self.choisirDossierU)
        vbox.addLayout(hbox)
        # Ligne 2
        hbox = QHBoxLayout()
        hbox.addWidget(self.table)
        vbox.addLayout(hbox)

        # Fixe le nombre de colonnes du tableau :
        self.table.setColumnCount(len(self.__nomColonnes))
        # Labels des colonnes du tableau :
        self.table.setHorizontalHeaderLabels(self.__nomColonnes)
        # Valider le tri colonne quand on clique dans l'en-tête de la
        # colonne :
        self.table.setSortingEnabled(True)
        # Retailler la largeur des colonnes (avec les entêtes) :
        self.ResizeTableColums()


    def RemplirTable(self):
        '''Le but de cette méthode est, pour chaque de nom de fichier *.txt
           dans la listeFichier, d'extraire les valeurs des métadonnées de
           perçage codées dans le nom du fichier.

           Le modèle des noms des fichiers *.txt en perçage est :
                   "P-GeometrieOutil_materiau_Vcxxx_fx.xxBCDry.txt"

           La méthode remplit le tableau avec les noms des fichiers de
           perçage et les paramètres de l'essais, qui sont ventilés dans les
           colonnes du tableau.

           Les valeurs des paramètres GeometrieOutil, materiau, Vc et f sont
           stockées respectivement dans les attributs listGeomOutils,
           listMateriaux, dicoMatVc et dicoMatF :
           - dicoMatVc est un dictionnaire dont la clef est un nom matériau
               et la valeur associée est la liste des valeurs Vc (vitesse de
               coupe) associées à ce matériau,
           - dicoMatF est un dictionnaire dont la clef est un nom matériau
               et la valeur associée est la liste des valeurs F (avance par
               tour) associées à ce matériau    .'''

        # dimensionnement le nombre de lignes du tableau :
        self.table.setRowCount(len(self.listeFichiers))

        ####################################################################
        ######## <Méthode RemplirTable à écrire> ###########################
        ####################################################################







        # ajuster automatiquement la largeur des colonnes à leur contenu :
        self.ResizeTableColums()


######################################
#   Classe dérivée  MetadataTWidget  #
######################################

class MetadataTWidget(MetadataWidget):
    '''Cette classe correspond à l'onglet d'analyse du répertoire contenant
       les fichiers *.txt de tournage.'''

    @staticmethod
    def BuildFileName (o, m, Vc, F, ap):
        '''Construit un nom de fichier tournage avec les paramètres passés,
           conformément à la règle de nommage (cf document TP tournage):
           "T-référence plaquette-matière usinée-Vcxxx-fx.xx-apx.xx-Dry.txt".
           o  : outil
           m  : matériau
           Vc : vitesse de coupe
           F  : avance par tour
           ap : profondeur de passe.
           Tous les arguments sont des chaînes de caractères
           '''
        name = "T-{}-{}-Vc{}-f{}-ap{}-Dry.txt".format(o,m,Vc,F,ap)
        return name

    def __init__(self, mainWindow):

        # exécuter le constructeur de la classe de base :
        MetadataWidget.__init__(self, mainWindow)

        self.__operation    = 'tournage'
        self.__nomColonnes  = ['Fichier','Outil','Matériau usiné',
                            'Vc [m/min]','f [mm/tour]', 'ap [mm]']

        self.__listOutils    = []  # nom  plaquettes trouvées

        self.__dicoOutilVc = {}  # dictionnaire des 'vitesse de coupe'
                                 # par outil
        self.__dicoOutilF  = {}  # dictionnaire des 'avance par tour' par
                                 # outil
        self.__dicoOutilAp = {}  # dictionnaire des 'profondeur passe' par
                                 # outil

        # initialiser l'attribut dossierUsinage de la classe de Base :
        self.dossierUsin = self.mw.usinage_dir + '/T'

        # Mise en place des widgets de l'interface GUI :
        self.__initUI()

        ############# INITIALISATION FORCEE ###############################
        #
        #  Initilisation forcée des listes et dictionnaires des classes.
        #
        #  Permet aux autres classes de ne pas être bloquées et d'accéder
        #  aux listes et aux dictionnaires en attendant que cette classe
        #  soit totalement opérationnelle...
        #
        ###################################################################
        self.INIT_FORCEE()
        ###################################################################

    def INIT_FORCEE(self):
        self.set_listMateriaux(['2017AT4', '45NiCrMo16Recuit'])
        self.__listOutils     = ['TCGX16T304ALH10', 'CNMG120404SM1105']
        self.__dicoOutilVc    = {'TCGX16T304ALH10' : ['300'],
                                 'CNMG120404SM1105': ['300']}
        self.__dicoOutilAp    = {'TCGX16T304ALH10': ['0.5','1.5'],
                                 'CNMG120404SM1105' : ['0.5','1']}
        self.__dicoOutilF     = {'TCGX16T304ALH10' : ['0.04','0.05'],
                                 'CNMG120404SM1105' : ['0.04','0.05']}
    @property
    def listOutils(self): return self.__listOutils

    @property
    def dicoOutilVc(self): return self.__dicoOutilVc

    @property
    def dicoOutilF(self): return self.__dicoOutilF

    @property
    def dicoOutilAp(self): return self.__dicoOutilAp

    def ChoixDossier(self):
            currDir = self.mw.usinage_dir + '/T'
            MetadataWidget.ChoixDossier(self, currDir, self.__operation)

    def __initUI(self):
        '''Mise en place des widgets de l'interface GUI.'''

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Ligne 1
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_scanFiles)
        hbox.addStretch()
        hbox.addWidget(self.labelUsinage)
        hbox.addWidget(self.dossierUsinage)
        hbox.addWidget(self.choisirDossierU)
        vbox.addLayout(hbox)
        # Ligne 2
        hbox = QHBoxLayout()
        hbox.addWidget(self.table)
        vbox.addLayout(hbox)

        # Fixe le nombre de colonnes du tableau :
        self.table.setColumnCount(len(self.__nomColonnes))
        # Labels des colonnes du tableau :
        self.table.setHorizontalHeaderLabels(self.__nomColonnes)
        # Valider le tri colonne quand on clique dans l'en-tête de la
        # colonne :
        self.table.setSortingEnabled(True)
        # Retailler la largeur des colonnes (avec les entêtes) :
        self.ResizeTableColums()


    def RemplirTable(self):
        '''Le but de cette méthode est, pour chaque de nom de fichier *.txt
           dans la listeFichier, d'extraire les valeurs des métadonnées de
           tournage codées dans le nom du fichier.

           Le modèle des noms des fichiers *.txt en tournage est :
                   "T-plaquette_materiauU-Vcxxx-fx.xx-apx.xxDry.txt"

           La méthode remplit le tableau avec les noms des fichiers de
           tournage et les paramètres de l'essais, qui sont ventilés dans
           les colonnes du tableau.

           Les valeurs des paramètres plaquette, materiau, Vc, ap et f sont
           stockées respectivement dans les attributs listOutils,
           listMateriaux, dicoOutilVc, dicoOutilAp et dicoOutilF :
           - dicoOutilVc est un dictionnaire dont la clef est un nom d'outil
               et la valeur associée est la liste des valeurs Vc (vitesse de
               coupe) associées à cet outil.
           - dicoOutilAp est un dictionnaire dont la clef est un nom d'outil
               et la valeur associée est la liste des valeurs Ap (profondeur
               de passe) associées à cet outil,
           - dicoOutilF est un dictionnaire dont la clef est un nom d'outil
               et la valeur associée est la liste des valeurs F (avance par
               tour) associées à cet outil.'''

        # dimensionnement le nombre de lignes du tableau :
        self.table.setRowCount(len(self.listeFichiers))

        ####################################################################
        ######## <Méthode RemplirTable à écrire> ###########################
        ####################################################################








        # ajuster automatiquement la largeur des colonnes à leur contenu :
        self.ResizeTableColums()


