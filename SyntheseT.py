#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import os, sys

from Synthese import SyntheseWidget # Classe de base
from FaireSyntheseT import SyntheseTData # Calcul de la synthèse

from PyQt5.QtWidgets import (QComboBox, QDoubleSpinBox, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt # paramètres

from matplotlib.backends.backend_qt5agg import  \
    FigureCanvasQTAgg as FigureCanvas,          \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#=========================================================================
class SyntheseTWidget(SyntheseWidget):
    ''' Widget de synthèse des acquisitions de tournages.'''
    __aff_items = ["F / Vc / Ap",\
                   "F / Ap / Vc",\
                   "Vc / F / Ap",\
                   "Vc / Ap / F",\
                   "Ap / F / Vc",\
                   "Ap / Vc / F"]
    def __init__(self, mainWindow):
        SyntheseWidget.__init__(self, mainWindow)
        self.choix_aff.addItems(self.__aff_items)
        self.choix_aff.activated.connect(self.__changer_modalites)
        # Boutons spécifiques
        # Boutons spécifiques
        self.choix_mat = QComboBox(self)
        self.texte_combo = QLabel("F")
        self.choix_combo = QComboBox(self)
        # Initialisation des systèmes d'axes de tracé :
        self.InitAxes(2,2) # Nombre de lignes/nombre de colonnes
        self.__initUI()

    def __initUI(self):
        vlay = QVBoxLayout(self)
        # Insertion de la ligne commune (choix affichage + bouton MAJ)
        vlay.addLayout(self.ligne_commune())
        # Insertion d'une ligne de combos
        texte_mat = QLabel("Matériau-Plaquette")
        ligne = QHBoxLayout(self)
        ligne.addWidget(texte_mat)
        ligne.addWidget(self.choix_mat)
        self.texte_combo.setFixedWidth(90)
        self.texte_combo.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        ligne.addWidget(self.texte_combo)
        ligne.addWidget(self.choix_combo)
        ligne.addStretch()
        vlay.addLayout(ligne)
        # === Zone de tracés ===
        # Réglages Matplolib :
        self.figure.subplots_adjust(left=0.1,right=0.98,bottom=0.1,\
                                    top=0.95,hspace=0.5)
        # La zone des tracés doit s'adapter à la taille de la fenêtre :
        self.canvas.setSizePolicy(QSizePolicy.Expanding,\
                                  QSizePolicy.Expanding)
        vlay.addWidget(self.canvas)
        vlay.addWidget(self.toolbar)

    def updateSyntheseData(self) :
        """ Méthode publique appelée par le bouton 'btn_MAJ' qui génère
            la liste des fichiers à incorporer dans la synthèse puis
            calcule les données de synthèse dans chacun de ceux qui ne sont
            pas encore dans le dictionnaire 'dicoSynthese'."""
        cur_dir = self.mw.dossierU
        ### Partie à modifier :
        file_names = ['T-CNMG120404SM1105-2017AT4-Vc300-f0.04-ap0.5-Dry.txt',
                      'T-CNMG120404SM1105-2017AT4-Vc300-f0.04-ap1-Dry.txt',
                      'T-CNMG120404SM1105-2017AT4-Vc300-f0.05-ap0.5-Dry.txt',
                      'T-CNMG120404SM1105-2017AT4-Vc300-f0.05-ap1-Dry.txt',
                      'T-CNMG120404SM1105-45NiCrMo16Recuit-Vc300-f0.04-ap0.5-Dry.txt',
                      'T-CNMG120404SM1105-45NiCrMo16Recuit-Vc300-f0.04-ap1-Dry.txt',
                      'T-CNMG120404SM1105-45NiCrMo16Recuit-Vc300-f0.05-ap0.5-Dry.txt',
                      'T-CNMG120404SM1105-45NiCrMo16Recuit-Vc300-f0.05-ap1-Dry.txt',
                      'T-TCGX16T304ALH10-2017AT4-Vc300-f0.04-ap0.5-Dry.txt',
                      'T-TCGX16T304ALH10-2017AT4-Vc300-f0.04-ap1.5-Dry.txt',
                      'T-TCGX16T304ALH10-2017AT4-Vc300-f0.05-ap0.5-Dry.txt',
                      'T-TCGX16T304ALH10-2017AT4-Vc300-f0.05-ap1.5-Dry.txt',
                      'T-TCGX16T304ALH10-45NiCrMo16Recuit-Vc300-f0.04-ap0.5-Dry.txt',
                      'T-TCGX16T304ALH10-45NiCrMo16Recuit-Vc300-f0.04-ap1.5-Dry.txt',
                      'T-TCGX16T304ALH10-45NiCrMo16Recuit-Vc300-f0.05-ap0.5-Dry.txt',
                      'T-TCGX16T304ALH10-45NiCrMo16Recuit-Vc300-f0.05-ap1.5-Dry.txt']
        #######################
        new_cases = dict()
        for fn in file_names :
            fp = cur_dir+"/"+fn
            if not os.path.isfile(fp) : # le fichier n'existe pas
                print("Le fichier <{}> n'existe pas !".format(fp))
            elif fp not in self.dicoSynthese : # nouveau cas
                new_cases[fp] = SyntheseTData(fp)
        return new_cases
#+++++++++++++++++++++++++++++++
    def __changer_modalites(self) :
        if self.choix_aff.currentIndex() == 0 :
            print("Tracés pour '{}'".format(self.__aff_items[0]))
            # à compléter


        elif self.choix_aff.currentIndex() == 1 :
            print("Tracés pour '{}'".format(self.__aff_items[1]))
            # à compléter


        elif self.choix_aff.currentIndex() == 2 :
            print("Tracés pour '{}'".format(self.__aff_items[2]))
            # à compléter


        elif self.choix_aff.currentIndex() == 3 :
            print("Tracés pour '{}'".format(self.__aff_items[3]))
            # à compléter


        elif self.choix_aff.currentIndex() == 4 :
            print("Tracés pour '{}'".format(self.__aff_items[4]))
            # à compléter


        elif self.choix_aff.currentIndex() == 5 :
            print("Tracés pour '{}'".format(self.__aff_items[5]))
            # à compléter

        else :
            print("Choix '{}' non prévu...".self.choix_aff.currentText())

#=========================================================================
