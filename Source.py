from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, font
import numpy as np
import sympy


"""

   -------- EULER --------
    Se considera y(k+1) = x(k+1) (refiriendo a función copiada en clase )
    
    Para evaluar f(x,y): https://docs.sympy.org/latest/index.html (recordar instalar el módulo con pip antes de correr el código o importarlo)

"""

def euler(y0,x0,xf,function,N):
    
    y = y0
    x = x0
    h = (xf - x0) / N
    
    fResult = {} #Se crea un diccionario resultado que guarda x:y como clave:valor
    fResult[x] = y #Se asigna manualmente x0:y0
    expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
    xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
    ys = sympy.Symbol('y') #Se le declara a sympy que existe una variable llamada "y"
    f = sympy.lambdify((xs,ys),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
    
    for k in range(N+1): #Se recorre k desde 0 hasta N
        x = x0 + k * h  
        fResult[x] = y #Se asigna una nueva clave x:y en el diccionario resultado
        functionEvaluated = f(x,y) #Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
        y = y + h * functionEvaluated        

    print(fResult) 

x0 = float(input('x0= '))
y0 = float(input('y0= '))
xf = float(input('xf= '))
function = input('function= ')
N = int(input('N= '))

#euler(0.32,0.13,0.14,"sin(x)-ln(y)",4)
euler(y0,x0,xf,function,N)