#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Version 1.4 - 2017, December, 12
# Authors : Jean-Luc Charles & Eric Ducasse
# License : CC-BY-NC
# Program name : ApplicationUsinage
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import numpy as np

class SignauxUsinage():

    def __init__(self, filePath, Fs, operation, data):

        self.__operation    = operation # "perçage" ou "tournage"
        self.__filePath     = filePath.replace("\\","/") # chemin du fichier
        self.__samplingFreq = Fs        # la fréquence d'échantilonnage

        # Remarque : dans le tableau data, les signaux Fx, Fy
        #            sont sur les lignes
        self.dataValues   = np.array(data)
        self.dataValues.setflags(write=False) # Protection des données

    @property
    def filePath(self):
        '''Nom complet du fichier d'acquisition, incluant le chemin d'accès'''
        return self.__filePath

    @property
    def fileName(self):
        '''Nom du fichier d'acquisation'''
        return os.path.basename(self.filePath)

    @property
    def samplingFrequency(self):
        '''Fréquence d'échantillonnage'''
        return self.__samplingFreq

    @property
    def Fx(self):
        '''numpy.ndarray copie de la composante X de la force'''
        return self.dataValues[0]

    @property
    def Fy(self):
        '''numpy.ndarray copie composante Y de la force'''
        return self.dataValues[1]

    @property
    def Fz(self):
        '''numpy.ndarray copie de la composante Z de la force'''
        return self.dataValues[2]

    @property
    def timeValues(self) :
        '''Instants d'échantillonnage.'''
        dt = 1.0/self.samplingFrequency
        return np.array([dt*n for n in range(self.dataValues.shape[1])])


class SignauxPercage(SignauxUsinage)  :
    '''Les signaux acquis sur une opération de perçage :
       - les trois composantes Fx, Fy et Fz mesurés par le capteur de force,
       - le couple selon l'axe Z.'''

    def __init__(self, filePath, Fs, data):
        # exécuter le constructeur de la classe de base :
        SignauxUsinage.__init__(self, filePath, Fs, "perçage", data)

    @property
    def C(self):
        '''Couple d'axe Z '''
        return self.dataValues[3]


class SignauxTournage(SignauxUsinage)  :
    '''Les signaux acquis sur une opération de  tournage :
       - les trois composantes Fx, Fy et Fz mesurés par le capteur de force.'''

    def __init__(self, filePath, Fs, data):
        # exécuter le constructeur de la classe de base :
        SignauxUsinage.__init__(self, filePath, Fs, "tournage", data)


