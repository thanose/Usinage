#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import os, sys
import matplotlib.pyplot as plt
#=========================================================================
class SyntheseData :
    ''' Synthèse des acquisitions sur un fichier donné. Classe de base.'''
    def __init__(self, filePath):
        self.__filepath = filePath

    @property
    def fp(self) : return self.__filepath

    @property
    def noms_attributs(self) :
        noms = [ nom for nom in dir(self) if "__" not in nom ]
        a_enlever = ["fp","noms_attributs"]
        return [ nom for nom in noms if nom not in a_enlever ]
#=========================================================================
