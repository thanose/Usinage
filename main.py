#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os, sys
import numpy as np

from PyQt5.QtWidgets import (QApplication, QDesktopWidget,
                             QMainWindow, QMessageBox, QTabWidget)
from Metadata import MetadataPWidget, MetadataTWidget
from SyntheseP import SynthesePWidget
from SyntheseT import SyntheseTWidget
from Detail import DetailPWidget, DetailTWidget
from SignauxUsinage import SignauxPercage, SignauxTournage
if __name__ == "__main__" :
    from FaireSyntheseP import SynthesePData
    from FaireSyntheseT import SyntheseTData
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class ApplicationUsinage(QMainWindow):

    '''Classe principale de l'application.
       Lance une fenêtre de dialogue qui permet de choisir de traiter des
       fichiers d'acquisition de type perçage ou tournage.'''

    icone_dir   = "icones"  # répertoire des icones des boutons
    # répertoire de travail :
    cur_dir     = os.getcwd().replace("\\","/")+"/"
    # répertoire des fichiers d'acquisition
    usinage_dir = os.getcwd().replace("\\","/")+"/usinage"

    def __init__(self):

        # Appel du constructeur de la classe de base :
        QMainWindow.__init__(self)

        # *** Bonnes pratiques  ***
        #   Définir dans le constructeur les données persistantes en tant
        #   qu'attributs ; si on ne connaît pas leur valeur à cet endroit
        #   on peut utiliser None:

        # objet QTabWidget qui gère les onglets de l'application :
        self.tabs        = QTabWidget()

        self.metadataTab = None # l'onglet des métadonnées
        self.syntheseTab = None # l'onglet de présentation synthétique
        self.detailTab   = None # l'onglet de visualisation détails

        self.toolBar     = self.addToolBar('toolBar')
        self.statusBar   = self.statusBar()  # Barre de statut

        # Initialisation de l'interface utilisateur :
        self.__initUI()


    def Center(self):
        '''Centrer la fenêtre principâle dans l'écran.'''

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

    def __initUI(self):
        '''Mettre en place les widgets et le layout de l'interface de
           l'application.'''

        self.resize(1200, 800)
        self.Center()
        titre = 'Application de traitement des données d\'usinage'+\
                ' (perçage/tournage)'
        self.setWindowTitle(titre)

        # Lancement d'une boîte de dialogue pour déterminer le type de
        # fichiers à traiter :
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle('Choix du type d\'usinage')
        msgBox.setText('Quels fichiers voulez-vous traiter ?')
        msgBox.setIcon(QMessageBox.Question)
        cancelBtn   = msgBox.addButton('Abandon',QMessageBox.RejectRole)
        tournageBtn = msgBox.addButton('Fichiers de tournage',
                                       QMessageBox.AcceptRole)
        percageBtn  = msgBox.addButton('Fichiers de perçage',
                                       QMessageBox.RejectRole)
        msgBox.exec();

        if (msgBox.clickedButton() == cancelBtn):
            sys.exit()
        elif (msgBox.clickedButton() == percageBtn):
            choix = "perçage"
            # onglet 1 : tableau des fichiers de perçage/tournage et
            #             métadonnées
            self.metadataTab = MetadataPWidget(self)
            # onglet 2 : Synthèse des données de tous les perçages/tournages
            self.syntheseTab = SynthesePWidget(self)
            # onglet 3 : Détails des données d'un perçage/tournage
            self.detailTab = DetailPWidget(self)
        elif (msgBox.clickedButton() == tournageBtn):
            choix = "tournage"
            self.metadataTab = MetadataTWidget(self)
            self.syntheseTab = SyntheseTWidget(self)
            self.detailTab   = DetailTWidget(self)

        # Ajout des onglets dans le QTabWidget :
        self.tabs.addTab(self.metadataTab, "Métadonnées {}".format(choix))
        self.tabs.addTab(self.syntheseTab, "Synthèse des {}s".format(choix))
        self.tabs.addTab(self.detailTab, "Détails des {}s".format(choix))
        # print("self.dossierU :",self.dossierU)

        # Définition du widget centre du QMainWindow ;
        self.setCentralWidget(self.tabs)

    @property
    def dossierU(self):
        '''Le répertoire dans lequel sont cherchés les fichiers de mesure
           *.txt'''
        du = self.metadataTab.dossierUsin
        return du.replace("\\","/")

    @staticmethod
    def LireFichier(filePath, operation, verbeux=False):
        '''Méthode statique à utiliser pour lire les données d'un fichier
           d'acquisition d'usinage.
           Renvoie un objet de type SignalPercage ou SignalTournage selon
           la valeur du paramètre <operation>, ou None si un problème de
           lecture ou une incohérence est survenue'''
        if verbeux :
            def prt(*args) :
                print(*args)
                return
        else :
            def prt(*args) :
                pass
                return
        if operation not in ("perçage", "tournage") :
            mess = 'ERREUR dans la méthode LireFichierUsinage : '
            mess += 'l\'argument <operation> doit être "perçage" '
            mess += 'ou "tournage"'
            print(mess)
            return
        # Si le fichier n'existe pas...
        if not os.path.isfile(filePath) :
            print("Erreur : le fichier  <{}> n'existe pas.".format(\
                    filePath))
            return None

        prt("Lecture du fichier <{}>".format(filePath))
        M = []
        with open(filePath, "r") as F:
            for line in F:
                line=line.strip()
                if line == "" : continue
                try:
                    ################ TODO ############################
                    # certains fichiers ont des valeurs séparées par
                    # des espaces, d'autres par des virgules!!!
                    # !!! Problème à régler !!!
                    ################ TODO ############################
                    line = line.replace(',',' ')

                    data = [float(x) for x in line.split()]
                except:
                    prt("line sautée : <{}>".format(line.strip()))
                    # information dur la fréquence d'échantilonnage :
                    if "Sample rate" in line:
                        try:
                            Fech = float(line.split(':')[1])
                        except:
                            mess = 'ERREUR dans la lecture de la fréquence'
                            mess += ' d\'échantillonnage ! Abandon de la'
                            mess += 'lecture.'
                            prt(mess)
                            return
                        mess = "\t-> fréquence échantilonnage lue :"
                        prt(mess+" {:.2f}".format(Fech))
                    continue
                # on ne prend pas la colonne <Time> :
                M.append(data[1:])
        data = np.array(M)
        prt(data.shape)
        if operation == 'perçage':
            # Fabriquer un objet SignalPercage :
            if len(data.shape) != 2 or data.shape[1] != 4:
                mess = 'ERREUR : dimension du ndarray {}'.format(data.shape)
                mess += 'incompatible avec un fichier "perçage"'
                prt(mess)
                return None

            # passer au construction de SignaPercage le ndarray
            # avec Fx, Fy, Fz, Mz en ligne :
            signal = SignauxPercage(filePath, Fech, data.transpose())

        elif operation == 'tournage':
            # Fabriquer un objet SignalTournage :
            if len(data.shape) != 2 or data.shape[1] != 3:
                mess = 'ERREUR : dimension du ndarray {}'.format(data.shape)
                mess += 'incompatible avec un fichier "tournage"'
                prt(mess)
                return None

            # passer au construction de SignaPercage le ndarray
            # avec Fx, Fy et Fz en ligne  :
            signal = SignauxTournage(filePath, Fech, data.transpose())

        return signal


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp  = ApplicationUsinage()
    myApp.show()
    sys.exit(app.exec_())
