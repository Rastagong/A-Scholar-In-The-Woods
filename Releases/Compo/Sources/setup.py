import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["pygame","numpy"], "includes":["sys","configparser","collections","random","queue","math","listeEvenementsLD26"], "compressed":"True", "include_files":[("YeuxScholar.png","YeuxScholar.png"), ("YeuxAnna.png", "YeuxAnna.png"), ("YeuxMonstre.png", "YeuxMonstre.png"), ("TilesetLD26.png","TilesetLD26.png"), ("Anna.png","Anna.png"), ("Mother.png","Mother.png"), ("Savant.png","Savant.png"),("BookAntiqua.ttf","BookAntiqua.ttf"),("LD26-Ferme.narromap","LD26-Ferme.narromap"),("LD26-Foret.narromap","LD26-Foret.narromap"),("LD26-Fin.narromap","LD26-Fin.narromap"),("TocPorte.wav","TocPorte.wav"),("Bete.wav","Bete.wav"),("Blip.wav","Blip.wav"),("Ouverture.wav","Ouverture.wav")]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [  Executable("main.py",base="Win32GUI") ]

setup(  name = "A Scholar in The Woods",
        version = "0.1",
        description = "LD26 Game",
        options = {"build_exe": build_exe_options},
        executables = executables)

