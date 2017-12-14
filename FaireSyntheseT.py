#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import os, sys
import matplotlib.pyplot as plt
from FaireSynthese import SyntheseData  # Classe de base
if __name__ == "__main__" :
    from main import ApplicationUsinage
#===========================================================================
class SyntheseTData(SyntheseData):
    ''' Synthèse des acquisitions de tournage.'''
    def __init__(self, filePath):
        SyntheseData.__init__(self,filePath)

#+++++++++++ Partie à enlever par les développeurs de l'équipe 4T ++++++++++
        self.__Ff_moy = np.random.normal(20.0,2.0)
        self.__Fp_moy = np.random.normal(100.0,10.0)
        self.__Fc_moy =  np.random.normal(30.0,2.0)
        self.__Kcc_moy = np.random.uniform(0.0,0.7)
        self.__f1 = 0.1*np.random.randint(200,401)

# Partie à décommenter et à compléter par les développeurs de l'équipe 4T ++
##
##        signaux = ApplicationUsinage.LireFichier(self.fp,"tournage")
##
##        self.__Ff_moy =
##        self.__Fp_moy =
##        self.__Fc_moy =
##        self.__Kcc_moy =
##
##        self.__f1 =
##
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @property
    def Ff_moy(self) :
        '''Effort d'avance moyen (axial).'''
        return self.__Ff_moy

    @property
    def Fp_moy(self) :
        '''Effort radial moyen.'''
        return self.__Fp_moy

    @property
    def Fc_moy(self) :
        '''Effort tangentiel moyen.'''
        return self.__Fc_moy

    @property
    def Kcc_moy(self) :
        '''Coefficient moyen d'effort spécifique de coupe.'''
        return self.__Kcc_moy

    @property
    def freq_1(self) :
        '''Fréquence du premier pic dans le signal d'effort radial.'''
        return self.__f1

#===========================================================================
if __name__ == "__main__" :
    dir_test = "Tests/"
    ftn = "Ch_Alu2017_Ap2,5_Vc300.txt"
    ftp = dir_test+ftn
    print("Fichier lu :",ftp)
    tourn_data = SyntheseTData(ftp)
    liste_noms = tourn_data.noms_attributs
    msg = "Nom des données de synthèse : {}".format(liste_noms)
    for an in liste_noms :
        msg += "\n\t{} ~ {:6.3f}".format(an,eval("tourn_data."+an))
    print(msg)
