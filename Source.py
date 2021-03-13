import numpy as np #Por ahora no se utilizó, pero probablemente sirva más adelante
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

    ##rang = list(range(x0,xf + 1))
    rang = np.arange (x0, xf, h)
    
    
    fResult = {}
    0
    for k in rang:        
        #functionEvaluated = 1234 #functionEvaluated = LÓGICA DE SYMPY. Provisorio lo setee con un valor para que no tire error
        expr = sympy.sympify(function)
        f = sympy.lambdify((x,y),expr)
        functionEvaluated = f(x,y)
        y = y + h * functionEvaluated
        fResult[x] = y
        x = x0 + k * h

    print(fResult) 

x0 = float(input('x0= '))
y0 = float(input('y0= '))
xf = float(input('xf= '))
function = input('function= ')
N = float(input('N= '))

#euler(0.32,0.13,0.14,"sin(x)-ln(y)",4)
euler(y0,x0,xf,function,N)