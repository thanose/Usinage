#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import os, sys

from PyQt5.QtWidgets import (QPushButton, QWidget, QComboBox, QHBoxLayout,
                             QVBoxLayout, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt # paramètres

from matplotlib.backends.backend_qt5agg import  \
    FigureCanvasQTAgg as FigureCanvas,          \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

#=========================================================================
class SyntheseWidget(QWidget):
    ''' Widget de synthèse des acquisitions. Classe de base.'''

    def __init__(self, mainWindow):
        QWidget.__init__(self, mainWindow)
        self.mw = mainWindow
        self.dicoSynthese = dict()
        # Bouton des modalités d'affichage
        self.choix_aff = QComboBox()
        # Bouton de mise à jour redimensionné
        self.btn_MAJ = QPushButton("Mettre à jour la synthese",self)
        self.btn_MAJ.clicked.connect(self.__updateDicoSynthese)

        # Les objets utiles aux tracé des courbes :
        self.figure     = Figure()  # figure tracé
        self.axes       = []        # la liste des systèmes d'axes

        # La zone de dessin des tracés matplotlib :
        self.canvas     = FigureCanvas(self.figure)
        # La barre d'outils pour le tracé :
        self.toolbar    = NavigationToolbar(self.canvas, self)
#+++++++++++++++++++++++++++++++
    def ligne_commune(self) :
        """ Ligne commune à insérer dans le layout des classes dérivées."""
        # Bouton du choix de la quantité à afficher
        texte_aff = QLabel("Modalités d'affichage (Combo/Abscisses/couleur)")
        AF = QVBoxLayout(self)
        AF.addWidget(texte_aff)        
        AF.addWidget(self.choix_aff)
        LC = QHBoxLayout(self)         
        LC.addLayout(AF) 
        LC.addStretch()
        self.btn_MAJ.resize(90,35)
        LC.addWidget(self.btn_MAJ)
        return LC
#+++++++++++++++++++++++++++++++
    def __updateDicoSynthese(self) :
        first_time = len(self.dicoSynthese)==0
        new_cases = self.updateSyntheseData()
        for k in new_cases :
            self.dicoSynthese[k] = new_cases[k]
        nb = len(new_cases)
        print("{} syntheses rajoutées dans 'dicoSynthese'".format(nb))
#+++++++++++++++++++++++++++++++
    def InitAxes(self,nL,nC) :
        '''Construit des systèmes d'axes pour nL x nC tracés'''

        # Création automatique des n° des subplots :
        # add_subplot(nL,nC,no) où
        #     nL est le nombre de lignes de graphiques
        #     nC est le nombre de colonnes de graphiques
        #     no le numéro du graphique (de haut en bas et de gauche à
        #                                droite)
        n = nL*nC
        self.axes = [self.figure.add_subplot(nL,nC,i+1) for i in range(n)]
#=========================================================================
