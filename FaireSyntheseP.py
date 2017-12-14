#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import numpy as np
import os, sys
import matplotlib.pyplot as plt
from FaireSynthese import SyntheseData # Classe de base
if __name__ == "__main__" :
    from main import ApplicationUsinage
#===========================================================================
class SynthesePData(SyntheseData):
    '''Synthèse des acquisitions de perçage.'''
    def __init__(self, filePath):
        SyntheseData.__init__(self,filePath)

#+++++++++++ Partie à enlever par les développeurs de l'équipe 4P +++++++++++
        self.__Fx_moy = np.random.normal(-15.0,2.0)
        self.__Fy_moy = np.random.normal(-20.0,2.0)
        self.__Fz_moy =  np.random.normal(280.0,40.0)
        self.__Mz_moy = np.random.uniform(4.0,0.5)
        self.__Fcc_moy = np.random.uniform(50.0,10.0)
        self.__f1 = 0.1*np.random.randint(400,801)

# Partie à décommenter et à compléter par les développeurs de l'équipe 4P ++
##
##        signaux = ApplicationUsinage.LireFichier(self.fp,"perçage")
##
##        self.__Fx_moy =
##        self.__Fy_moy =
##        self.__Fz_moy =
##        self.__Mz_moy =
##        self.__Fcc_moy =
##
##        self.__f1 =
##
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @property
    def Fx_moy(self) :
        '''Effort moyen selon x.'''
        return self.__Fx_moy

    @property
    def Fy_moy(self) :
        '''Effort moyen selon y.'''
        return self.__Fy_moy

    @property
    def Fz_moy(self) :
        '''Effort moyen selon z.'''
        return self.__Fz_moy

    @property
    def Mz_moy(self) :
        '''Moment moyen par rapport à l'axe Oz.'''
        return self.__Mz_moy

    @property
    def Fcc_moy(self) :
        '''Effort spécifique de coupe moyen.'''
        return self.__Fcc_moy

    @property
    def freq_1(self) :
        '''Fréquence du premier pic dans le signal d'effort radial.'''
        return self.__f1

#=========================================================================
if __name__ == "__main__" :
    dir_test = "Tests/"
    fpn = "45NiCrMo16Recuit_VC15_f004repet1.txt"
    fpp = dir_test+fpn
    print("Fichier lu :",fpp)
    perc_data = SynthesePData(fpp)
    liste_noms = perc_data.noms_attributs
    msg = "Nom des données de synthèse : {}".format(liste_noms)
    for an in liste_noms :
        msg += "\n\t{} ~ {:.3f}".format(an,eval("perc_data."+an))
    print(msg)
