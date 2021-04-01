from distutils.core import setup # Need this to handle modules
import py2exe 
from tkinter import Tk, Toplevel,Label,Button,Frame,Canvas,Scrollbar,VERTICAL,BOTH,LEFT,RIGHT,Y, HORIZONTAL,Entry,IntVar,Radiobutton,Checkbutton,BooleanVar,LabelFrame
from tkinter import filedialog
from tkinter import messagebox, font
import tkinter.ttk

import numpy as np
import sympy
import re
from matplotlib import pyplot as plt

setup(windows=[{'script':'Source.py', "icon_resources": [(1, "Metodos.ico")]}], options={"py2exe":{"packages": ['matplotlib']}}) # Calls setup function to indicate that we're dealing with a single console application