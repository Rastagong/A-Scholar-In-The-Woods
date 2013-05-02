# -*-coding:iso-8859-1 -*
from constantes import *
from sys import path as syspath
if BUILDING_LOCAL:
    syspath.append(NARRO_ENGINE_PATH)
from narro.main import *
from narro.constantes import *
from gestionnaireEvenements import *

if __name__ == "__main__":
    jeu = Narro()
    jeu.inclureGestionnaire(MonGestionnaireEvenements(jeu))
    jeu.executer()
    if REDIRECTION_FICHIER_ERREURS:
        sys.stderr.close()
