import numpy as np #Por ahora no se utilizó, pero probablemente sirva más adelante
import sympy

"""

   -------- EULER --------
    Se considera y(k+1) = x(k+1) (refiriendo a función copiada en clase )
    
    Para evaluar f(x,y): https://docs.sympy.org/latest/index.html (recordar instalar el módulo con pip antes de correr el código o importarlo)

"""

def euler(y0,x0,xf,function,N):
    rang = list(range(x0,xf + 1))
    
    y = y0
    x = x0
    h = (xf - x0) / N
    
    fResult = {}
    
    for k in rang:        
        functionEvaluated = 1234 #functionEvaluated = LÓGICA DE SYMPY. Provisorio lo setee con un valor para que no tire error
        y = y + h * functionEvaluated
        fResult[x] = y
        x = x0 + k * h


