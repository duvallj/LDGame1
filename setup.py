import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Paper Plane Simulator 2007",
    options={"build_exe": {"packages": ["pygame", "pygame.gfxdraw", "math", "random", "itertools"],
                           "include_files": ["imgs/cloud1.png", "imgs/cloud2.png", "imgs/grass.png", "imgs/star.png"]}
             },
    executables=executables
)