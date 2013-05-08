# -*-coding:utf-8 -*
# -*-coding:utf-8 -*
import pygame
from pygame.locals import *

NOM_CARTE_LANCEMENT = "LD26-Foret"
DOSSIER_RESSOURCES = "Ressources"

FENETRE = dict()
FENETRE["messageErreurInitialisationPygame"]="Une erreur s'est produite durant l'initialisation de Pygame, le programme doit donc se fermer." 
FENETRE["messageErreurInitialisationFenetre"]="Une erreur s'est produite durant l'initialisation de la fenêtre, le programme doit donc se fermer." 
FENETRE["longueurFenetre"] = 512
FENETRE["largeurFenetre"] = 384
FENETRE["largeurFenetreReelle"] = 416
FENETRE["couleurFenetre"] = (0,0,0) ##Couleur de fond de la fenêtre (hors zones spéciales comme tileset, outils...)
FENETRE["titreFenetre"] = "A Scholar In The Woods"
FENETRE["flagsFenetre"] = DOUBLEBUF#|FULLSCREEN|HWSURFACE
FENETRE["forceDirectX"] = False


VITESSE_DEPLACEMENT_JOUEUR_PAR_DEFAUT = 170
LIMITER_FPS = True
NOMBRE_MAX_DE_FPS = 60

