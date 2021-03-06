# -*-coding:iso-8859-1 -*
import pygame, queue, os, collections
from pygame.locals import *
from .constantes import *
from .horloge import *
from .observable import *
from .interrupteur import *

class ZonePensee(Observable):
    """Classe g�rant la zone de pens�e en bas de l'�cran."""

    def __init__(self, jeu):
        Observable.__init__(self, "_surface", "_positionSurface", "_penseeAGerer")
        self._jeu = jeu
        self._polices, self._queuePensees = dict(), queue.Queue()
        self._polices["parDefaut"] = pygame.font.Font(os.path.join(DOSSIER_RESSOURCES,NOM_FICHIER_POLICE_PAR_DEFAUT), TAILLE_POLICE_PAR_DEFAUT) 
        self._polices["splashText"] = pygame.font.Font(os.path.join(DOSSIER_RESSOURCES,NOM_FICHIER_POLICE_PAR_DEFAUT), TAILLE_POLICE_SPLASH_SCREEN) 
        self._messageActuel, self._vitesse = None, VITESSE_PENSEE_PAR_DEFAUT
        self._etapeAffichage, self._penseeAGerer, self._auMoinsUnePenseeGeree = 0, Interrupteur(False), False
        self._nombreEtapes, self._surface, self._positionSurface, self._policeActuelle = -1, None, None, "parDefaut"
        self._couleur, self._tempsLecture = COULEUR_ECRITURE_PENSEE, 0
        self._compteurMots = collections.Counter(self._messageActuel)

    def _majPenseeActuelle(self, message, vitesse, police, couleur, tempsLecture , nom):
        self._message, self._vitesse, self._nomPensee = message, vitesse, nom
        self._etapeAffichage, self._auMoinsUnePenseeGeree = 0, True
        self._penseeAGerer.activer()
        self._nombreEtapes = len(self._message) #Autant d'�tapes que de caract�res
        Horloge.initialiser(id(self), 1, 0)
        self._policeActuelle, self._couleur, self._tempsLecture = police, couleur, tempsLecture
        self._positionSurface = [0,FENETRE["largeurFenetre"]]
        self._surfaceComplete = self._polices[self._policeActuelle].render(self._message, True, self._couleur, COULEUR_FOND_ZONE_PENSEE)
        self._positionSurface[0] = (FENETRE["longueurFenetre"] - self._surfaceComplete.get_width() ) / 2
        self._positionSurface[1] = ( (FENETRE["largeurFenetreReelle"]-FENETRE["largeurFenetre"]-self._surfaceComplete.get_height() ) / 2)+FENETRE["largeurFenetre"] 
        self.obsOnMiseAJour("_positionSurface", self._positionSurface)
        self.obsOnMiseAJour("_penseeAGerer", self._penseeAGerer)

    def getMotActuel(self):
        """Retourne le no du mot actuel de la pens�e courante"""
        return len(self._message[:self._etapeAffichage])

    def getNomPensee(self):
        return self._nomPensee

    def redonnerPositionSurface(self):
        """Fonction appel�e lors d'un changement de carte qui redonne la position de la surface."""
        self.obsOnMiseAJour("_positionSurface", self._positionSurface)

    def ajouterPensee(self, message, vitesse=VITESSE_PENSEE_PAR_DEFAUT, police="parDefaut", couleur=COULEUR_ECRITURE_PENSEE, tempsLecture=TEMPS_LECTURE_PENSEE, nom=False):
        """Ajoute une pens�e � afficher. Elle devient un <message> affich� � la <vitesse> exprim�e en millisecondes.
        La police <police> fait r�f�rence � un nom dans le dico des polices. Le <tempsLecture> est le temps en millisecondes n�cessaire � la lecture :
        il sert de r�f�rence � de nombreux �v�nements, et permet d'afficher la pens�e suivante apr�s un certain temps seulement.
        Cette pens�e n'est affich�e imm�diatement que si aucune autre pens�e n'est actuellement g�r�e (en train de s'afficher, ou en train d'�tre lue).
        Si une autre pens�e est d�j� g�r�e, on ajoute cette nouvelle pens�e � la queue."""
        if self._penseeAGerer.voir() is False:
            self._majPenseeActuelle(message, vitesse, police, couleur, tempsLecture, nom)
        else:
            self._queuePensees.put_nowait(dict(message=message, vitesse=vitesse, police=police, couleur=couleur, tempsLecture=tempsLecture, nom=nom))
    
    def _gererPenseeActuelle(self):
        """S'il y a une pens�e � g�rer, g�re son affichage. Sinon, g�re la queue (pour prendre la pens�e suivante)."""
        if self._etapeAffichage < self._nombreEtapes and Horloge.sonner(id(self), 1) is True:
            if self._message[self._etapeAffichage] == ' ': #L'espace ne n�cessite pas d'�tape en soi, donc on affiche le caract�re suivant en m�me temps
                self._etapeAffichage += 1
            messageActuel = self._message[:self._etapeAffichage+1]
            self._surface = self._surfaceComplete.copy()
            longueurSurface, largeurSurface = self._polices[self._policeActuelle].size(messageActuel)
            self._surface.fill((0,0,0), Rect(longueurSurface, 0, self._surface.get_width() - longueurSurface, largeurSurface) )
            self.obsOnMiseAJour("_surface", self._surface)
            self._etapeAffichage += 1
            if self._etapeAffichage < self._nombreEtapes:
                Horloge.initialiser(id(self), 1, self._vitesse)
            elif self._tempsLecture <= 0:
                self._etapeAffichage = 0
                self._gererQueuePensees()
            elif self._tempsLecture > 0:
                self._etapeAffichage = 0
                Horloge.initialiser(id(self), "Lecture", self._tempsLecture)
        elif Horloge.sonner(id(self), "Lecture") is True:
            self._gererQueuePensees()
    
    def _gererQueuePensees(self):
        """Fonction appel�e quand une pens�e a �t� trait�e (et lue si n�cessaire). Elle se charge de prendre la prochaine pens�e dans la queue  s'il y en a.
        S'il n'y a rien dans la queue, on dit que plus aucune pens�e n'est � g�rer."""
        if self._queuePensees.empty() is True: #S'il n'y aucune pens�e dans la queue, il n'y a rien � g�rer, on le dit
            self._penseeAGerer.desactiver()
            self.obsOnMiseAJour("_penseeAGerer", self._penseeAGerer)
        else: #S'il y a encore des pens�es dans la queue, on charge la prochaine pens�e, on dit qu'elle est � g�rer
            penseeCourante = self._queuePensees.get()
            self._majPenseeActuelle(penseeCourante["message"], penseeCourante["vitesse"], penseeCourante["police"], penseeCourante["couleur"], penseeCourante["tempsLecture"], penseeCourante["nom"])

    def gererSurfacePensee(self):
        self._gererPenseeActuelle()

    ###
    #Accesseurs et mutateurs
    ###

    def _getPenseeAGerer(self):
        return self._penseeAGerer

    def _getAuMoinsUnePenseeGeree(self):
        return self._auMoinsUnePenseeGeree

    def _getPolices(self):
        return self._polices

    penseeAGerer = property(_getPenseeAGerer)
    auMoinsUnePenseeGeree = property(_getAuMoinsUnePenseeGeree)
    polices = property(_getPolices)

