# -*-coding:utf-8 -*
import sys, os
from cx_Freeze import setup, Executable

librariesPath = []
if sys.platform.startswith("linux"): 
    librariesPath.append("/usr/lib")

build_exe_options = {"packages" : ["pygame","numpy"], 
                    "includes" : ["narro", "sys", "collections", "random", "queue", "math"],
                    "compressed":"True", 
                    "include_files":[("Ressources", "Ressources"), ("README.txt", "README.txt"), ("License.txt", "License.txt")],
                    "bin_path_includes": librariesPath,
		    "bin_includes": ["libtinfo.so.5"],
                    "icon": [os.path.join("Ressources", "Narro.ico")]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "A_Scholar_in_The_Woods",
        version = "0.2",
        description = "Post Compo version of my Ludum Dare 26 entry, A Scholar In The Woods (http://www.ludumdare.com/compo/ludum-dare-26/?action=preview&uid=3761)",
        author= "Rastagong",
        author_email= "rastagong@gmail.com",
        url= "https://github.com/Rastagong/A-Scholar-In-The-Woods",
        options = {"build_exe": build_exe_options},
        executables =[  Executable("play.py", base=base, icon=os.path.join("Ressources", "Narro.ico") ) ])

