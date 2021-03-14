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
    
    fResult = {}
    fResult[x] = y
    expr = sympy.sympify(function)
    xs = sympy.Symbol('x')
    ys = sympy.Symbol('y')
    f = sympy.lambdify((xs,ys),expr)
    
    for k in range(N+1): 
        x = x0 + k * h   
        fResult[x] = y
        functionEvaluated = f(x,y)
        y = y + h * functionEvaluated        

    print(fResult) 

x0 = float(input('x0= '))
y0 = float(input('y0= '))
xf = float(input('xf= '))
function = input('function= ')
N = int(input('N= '))

#euler(0.32,0.13,0.14,"sin(x)-ln(y)",4)
euler(y0,x0,xf,function,N)