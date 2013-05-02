# -*-coding:iso-8859-1 -*
import pygame
from sys import  stderr
from pygame.locals import *


BUILDING_LOCAL = True #Doit valoir <True> si le Narro Engine est utilisé en local, et qu'il ne se trouve pas dans le PYTHONPATH
NARRO_ENGINE_PATH = "../../" #Dossier dans lequel doit se trouver le package narro quand on est en local (il est ajouté au PYTHONPATH)

NOM_CARTE_LANCEMENT = "LD26-Ferme"
DOSSIER_RESSOURCES = "Ressources/"

FENETRE = dict()
FENETRE["messageErreurInitialisationPygame"]="Une erreur s'est produite durant l'initialisation de Pygame, le programme doit donc se fermer." 
FENETRE["messageErreurInitialisationFenetre"]="Une erreur s'est produite durant l'initialisation de la fenêtre, le programme doit donc se fermer." 
FENETRE["longueurFenetre"] = 512
FENETRE["largeurFenetre"] = 384
FENETRE["largeurFenetreReelle"] = 416
FENETRE["couleurFenetre"] = (0,0,0) ##Couleur de fond de la fenêtre (hors zones spéciales comme tileset, outils...)
FENETRE["titreFenetre"] = "A Scholar In The Woods"
FENETRE["flagsFenetre"] = pygame.DOUBLEBUF#|pygame.FULLSCREEN|pygame.HWSURFACE
