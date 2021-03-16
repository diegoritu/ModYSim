from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, font
import numpy as np
import sympy
import re
from matplotlib import pyplot as plt 


"""

   -------- EULER --------
    Se considera y(k+1) = x(k+1) (refiriendo a función copiada en clase )
    
    Para evaluar f(x,y): https://docs.sympy.org/latest/index.html (recordar instalar el módulo con pip antes de correr el código o importarlo)

"""
root = Tk()
root.geometry('800x600')
root.title('Métodos')
root.resizable(0,0)
#Label(root, text="").grid(row=0,column=0) #Espacio en pantalla
Label(root, text='Métodos', font = ('Lucida Bright',25), pady=20, padx=40).grid(row = 0, column=1)

def inputIsValid(params):
    
    for param in params:
        try:
            float(param)
        except:
            return False 

        """
        if(re.match(r"(\+|\-)?\d+(,\d+)?$", param) is None):
            print(param)
            return False
        """
    return True

def nValid(n):
    try:
        int(n)
    except:
        return False 
    return True

def isMathFunction(function):
    try:
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
        ys = sympy.Symbol('y') #Se le declara a sympy que existe una variable llamada "y"
        sympy.lambdify((xs,ys),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
    except:
        return False
    return True

def btnCalcular():  
    yInicial = y0.get().replace(",",".")
    xInicial = x0.get().replace(",",".")
    xFinal = xf.get().replace(",",".")
    functionFix = function.get().replace(",",".")
    print("HEY, ENTRÉ")  
    params = [yInicial,xInicial,xFinal,n.get()]
    if(inputIsValid(params) and nValid(n.get()) and isMathFunction(functionFix)):
        print("HEY, SOY VALIDO")
        fEuler = euler(float(yInicial),float(xInicial),float(xFinal),functionFix,int(n.get()))
        fEulerMejorado = eulerMejorado(float(yInicial),float(xInicial),float(xFinal),functionFix,int(n.get()))
        fRungeKutta = rungeKutta(float(yInicial),float(xInicial),float(xFinal),functionFix,int(n.get()))
        
        print(fEuler)
        print(fEulerMejorado)              
        print(fRungeKutta)

        plt.title("Gráfico") 
        plt.xlabel("Eje X") 
        plt.ylabel("Eje Y") 
        ejeXEuler = list(fEuler.keys())
        ejeYEuler = list(fEuler.values())
        ejeXEulerMejorado = list(fEulerMejorado.keys())
        ejeYEulerMejorado = list(fEulerMejorado.values())
        ejeXRungeKutta = list(fRungeKutta.keys())
        ejeYRungeKutta = list(fRungeKutta.values())

        tempXEuler = []
        tempYEuler = []
        tempXEulerMejorado = []
        tempYEulerMejorado = []
        tempXRungeKutta = []
        tempYRungeKutta = []
        primeraVez = True

        for i in range(int(n.get())+1):
            
            tempXEuler.append(ejeXEuler[i])
            tempYEuler.append(ejeYEuler[i])
            tempXEulerMejorado.append(ejeXEulerMejorado[i])
            tempYEulerMejorado.append(ejeYEulerMejorado[i])
            tempXRungeKutta.append(ejeXRungeKutta[i])
            tempYRungeKutta.append(ejeYRungeKutta[i])
            
            plt.scatter(tempXEuler, tempYEuler, color = "r")
            plt.scatter(tempXEulerMejorado, tempYEulerMejorado, color = "g")
            plt.scatter(tempXRungeKutta, tempYRungeKutta, color = "b")
            plt.pause(0.80)
            plt.plot(tempXEuler, tempYEuler, label = "Euler", color = "r",linewidth=2)
            plt.plot(tempXEulerMejorado, tempYEulerMejorado, label = "Euler Mejorado", color = "g",linewidth=2) 
            plt.plot(tempXRungeKutta, tempYRungeKutta, label = "Runge-Kutta", color = "b",linewidth=2)
            plt.grid()
            plt.pause(0.80)
           
            if primeraVez:
                plt.legend()
                primeraVez = False

        
        plt.show()
    
              
    elif(not nValid(n.get())):
        messagebox.showerror("Métodos", "N inválida.")
    elif(not isMathFunction(function.get())):
        messagebox.showerror("Métodos", "Función inválida.")
    else:
        messagebox.showerror("Métodos", "Datos inválidos. Por favor revise x0, xf e y0.")




#Algoritmo Euler
def euler(y0,x0,xf,function,N):    
    try:
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

        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")
#Algoritmo Euler Mejorado
def eulerMejorado(y0,x0,xf,function,N):    
    try:
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
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
            yOriginal = y #guardo el valor de y actual para cuando tenga que hacer el recalculo
            y = y + h * f(x,y) #predictor
            y = yOriginal + (h/2) * (f(x,yOriginal) + f(x+h,y)) #corrector
          
        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")
#Algoritmo Runge Kutta
def rungeKutta(y0,x0,xf,function,N):    
    try:
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
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
            p1 = h * f(x,y)
            p2 = h * f(x+(h/2),y+(p1/2))
            p3 = h * f(x+(h/2),y+(p2/2))
            p4 = h * f(x+h, y+p3)
            y = y + (1/6) * (p1+2*p2+2*p3+p4)
        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")


Label(root, text="Parámetros: ", font = ('Lucida Bright',15), padx=10).grid(row=1,column=0)

parameters = LabelFrame(root, padx=50, pady=20)

Label(root, text="                            ").grid(row=2,column=1) #Espacio en pantalla

parameters.grid(row=3, column=1)

Label(parameters,text="Y0= ", font = ('Lucida Bright',10)).grid(row=0,column=0)
y0 = Entry(parameters,width=10,borderwidth=5)
y0.grid(row=0,column=1, pady=5, padx=5)
Label(parameters,text="X0= ", font = ('Lucida Bright',10) ).grid(row=0,column=2)
x0 = Entry(parameters,width=10,borderwidth=5)
x0.grid(row=0,column=3, pady=5, padx=5)
Label(parameters,text="Xf= ", font = ('Lucida Bright',10)).grid(row=0,column=4)
xf = Entry(parameters,width=10,borderwidth=5)
xf.grid(row=0,column=5, pady=5, padx=5)
Label(parameters,text="f(x,y)= ", font = ('Lucida Bright',10)).grid(row=1,column=0)
function = Entry(parameters,width=10,borderwidth=5)
function.grid(row=1,column=1, pady=5, padx=5)
Label(parameters,text="N= ", font = ('Lucida Bright',10)).grid(row=1,column=2)
n = Entry(parameters,width=10,borderwidth=5)
n.grid(row=1,column=3, pady=5, padx=5)
Button(parameters,text="Calcular", font = ('Lucida Bright',15), command=btnCalcular).grid(row=1,column=5)


"""
Button(parameters,text="Euler", font = ('Lucida Bright',15), command=btnEuler).grid(row=5,column=1)
Label(parameters, text="                            ").grid(row=6,column=1) #Espacio en pantalla
Button(parameters,text="Euler Mejorado", font = ('Lucida Bright',15), command=btnEulerM).grid(row=7,column=1)
Label(parameters, text="                            ").grid(row=8,column=1) #Espacio en pantalla
Button(parameters,text="Runge Kutta", font = ('Lucida Bright',15), command=btnRK).grid(row=9,column=1)
"""




#Por consola:
"""

x0 = float(input('x0= '))
y0 = float(input('y0= '))
xf = float(input('xf= '))
function = input('function= ')
N = int(input('N= '))

#euler(0.32,0.13,0.14,"sin(x)-ln(y)",4)

print(euler(y0,x0,xf,function,N))
print(eulerMejorado(y0,x0,xf,function,N))
print(rungeKutta(y0,x0,xf,function,N))
"""

root.mainloop()