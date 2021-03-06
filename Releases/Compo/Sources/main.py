# -*-coding:utf-8 -*
import pygame, configparser,sys
from pygame.locals import *
from constantes import *
from zonePensee import *
from gestionnairevenements import *
from carte import *
if SESSION_DEBUG:
    import pdb

class Jeu:
    """Classe contenant l'intégralité du jeu"""
    
    ##Méthodes privées
    ##Classées par ordre d'appel dans le code
    def _initialiserTout(self):
        """Initialise le moteur"""
        self._initialiserAffichage(**FENETRE)
        self._zonePensee = ZonePensee(self)
        self._gestionnaireEvenements = GestionnaireEvenements(self)
        self._gestionnaireEvenements.initialiserBoiteOutils()

    def _initialiserAffichage(self, messageErreurInitialisationPygame, messageErreurInitialisationFenetre, longueurFenetre, largeurFenetre, largeurFenetreReelle, couleurFenetre, titreFenetre, flagsFenetre=0):
        """Initialise Pygame et la fenêtre"""
        try:
            pygame.init()
        except pygame.error:
            print(messageErreurInitialisationPygame)
            raise SystemExit
        try:
            self._fenetre = pygame.display.set_mode((longueurFenetre, largeurFenetreReelle), flagsFenetre)
        except pygame.error:
            print(messageErreurInitialisationFenetre)
            pygame.quit()
            raise SystemExit
        self._fenetre.fill(couleurFenetre)
        pygame.display.set_caption(titreFenetre)
        if REPETITION_TOUCHES is True:
            pygame.key.set_repeat(1,INTERVALLE_REPETITION_TOUCHES)
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(LISTE_EVENTS_AUTORISES)
        pygame.mixer.init()

    def _chargerCarteAExecuter(self):
        """Charge en mémoire la carte à exécuter"""
        """if self._carteAExecuter not in self._cartes.keys(): #Si la carte n'a pas encore été initialisée, on l'initialise
            cheminFichierCarte = DOSSIER_RESSOURCES + self._carteAExecuter + EXTENSION_FICHIER_CARTE
            config = configparser.ConfigParser()
            config.read(cheminFichierCarte)
            self._cartes[self._carteAExecuter] = Carte(config, self)"""
        if self._premiereCarteChargee is True: #Il y a une carte précédente, on enlève toutes ses transformations (dont les transitions) 
            """del self._carteActuelle.transformationsGlobales[:]
            del self._carteActuelle.transformationsParties[:]
            self._carteActuelle.mettreToutAChanger()"""
            self._zonePensee.obsSupprimerObservateur(self._carteActuelle, "_surface")
            self._zonePensee.obsSupprimerObservateur(self._carteActuelle, "_positionSurface")
            self._gestionnaireEvenements.evenements["concrets"][self._carteActuelle.nom].clear()
            del self._carteActuelle
        ###
        cheminFichierCarte = DOSSIER_RESSOURCES + self._carteAExecuter + EXTENSION_FICHIER_CARTE
        config = configparser.ConfigParser()
        config.read(cheminFichierCarte)
        self._carteActuelle = Carte(config, self)
        #objgraph.show_backrefs([self._carteActuelle], filename="t.png")
        ###
        self._premiereCarteChargee = True
        #self._carteActuelle = self._cartes[self._carteAExecuter]
        self._carteActuelle.initialiserScrolling(self._joueur.x, self._joueur.y) 
        self._zonePensee.obsAjouterObservateur(self._carteActuelle, "_surface")
        self._zonePensee.obsAjouterObservateur(self._carteActuelle, "_positionSurface")
        self._gestionnaireEvenements.chargerEvenements(self._carteActuelle.nom)
        if self._zonePensee.auMoinsUnePenseeGeree is True:
            self._zonePensee.redonnerPositionSurface()

    def _verifierSiLeJeuEstFini(self):
        return (self._event.type == QUIT) or (self._event.type == KEYDOWN and self._event.dict["key"] == K_ESCAPE)

    ##Méthodes publiques
    #
    def executer(self):
        """Exécute le jeu"""
        self._initialiserTout()
        self._jeuFini, self._carteAExecuter, self._changementCarte, self._cartes = False, str(NOM_CARTE_LANCEMENT), False, dict()
        self._horlogeFps, self._premiereCarteChargee, self._dicoSurfaces = pygame.time.Clock(), False, dict()
        while self._jeuFini is not True: #Tant que le joueur ne veut pas quitter
            self._changementCarte = False #Si on veut changer de carte, il faut pouvoir rentrer dans la boucle ci-dessous pour la nouvelle carte
            self._chargerCarteAExecuter()
            while self._changementCarte is not True and self._jeuFini is not True: #Tant que le joueur ne veut pas quitter ou changer de carte
                self._event = pygame.event.poll()
                self._jeuFini = self._verifierSiLeJeuEstFini()
                self._gestionnaireEvenements.gererEvenements(self._carteActuelle.nom)
                self._gestionnaireEvenements.traiterPositions()
                self._gestionnaireEvenements.actualiserSonsFixes()
                self._zonePensee.gererSurfacePensee()
                self._carteActuelle.afficher()
            #print("###########################################################################")
            #objgraph.show_growth()
        pygame.mixer.quit()
        pygame.quit()

    ##Accesseurs et mutateurs 
    ##
    ##
    def _getEvent(self):
        """Accesseur retournant <event>, qui est le dernier event produit par le joueur"""
        return self._event
    
    def _getFenetre(self):
        return self._fenetre

    def _getJeuFini(self):
        """Accesseur retournant le booléen <jeuFini>, qui vaut True si le joueur veut quitter le jeu"""
        return self._jeuFini

    def _getCarteActuelle(self):
        """Accesseur retournant la carte actuelle"""
        return self._carteActuelle

    def _getCarteAExecuter(self):
        """Accesseur retournant le <str> <carteAExecuter>, qui contient le nom de la carte en cours d'exécution"""
        return self._carteAExecuter

    def _getZonePensee(self):
        return self._zonePensee

    def _getGestionnaireEvenements(self):
        return self._gestionnaireEvenements

    def _getJoueur(self):
        return self._joueur

    def _setJoueur(self, nouveauJoueur):
        self._joueur = nouveauJoueur

    def _getDicoSurfaces(self):
        return self._dicoSurfaces

    def _setDicoSurfaces(self, val):
        self._dicoSurfaces = val

    def _getHorlogeFps(self):
        return self._horlogeFps

    def _setCarteAExecuter(self,nouvelleCarteAExecuter):
        try:
            nouvelleCarteAExecuter = str(nouvelleCarteAExecuter)
        except:
            print(MESSAGE_ERREUR_MUTATION_CARTE_A_EXECUTER)
            raise SystemExit
        else:
            self._carteAExecuter = nouvelleCarteAExecuter

    def _setChangementCarte(self, nouveauChangementCarte):
        if nouveauChangementCarte is True or nouveauChangementCarte is False: #Si <nouveauChangementCarte> est bien un booléen
            self._changementCarte = nouveauChangementCarte
        else:
            print(MESSAGE_ERREUR_MUTATION_CHANGEMENT_CARTE)
            raise SystemExit
    
    event = property(_getEvent)
    fenetre = property(_getFenetre)
    jeuFini = property(_getJeuFini)
    carteAExecuter = property(_getCarteAExecuter, _setCarteAExecuter)
    changementCarte = property(fset=_setChangementCarte)
    carteActuelle = property(_getCarteActuelle)
    zonePensee = property(_getZonePensee)
    joueur = property(fget=_getJoueur, fset=_setJoueur)
    dicoSurfaces = property(_getDicoSurfaces, _setDicoSurfaces)
    horlogeFps = property(fget=_getHorlogeFps)
    gestionnaireEvenements = property(_getGestionnaireEvenements)

if __name__ == "__main__":
    jeu = Jeu()
    jeu.executer()
