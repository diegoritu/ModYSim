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
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "t"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
        sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
    except:
        return False
    return True

def btnCalcular():  
    xInicial = x0.get().replace(",",".")
    tInicial = t0.get().replace(",",".")
    tFinal = tf.get().replace(",",".")
    functionFix = function.get().replace(",",".")
    print("HEY, ENTRÉ")  
    params = [xInicial,tInicial,tFinal,n.get()]
    if(inputIsValid(params) and nValid(n.get()) and isMathFunction(functionFix)):
        print("HEY, SOY VALIDO")
        fEuler = euler(float(xInicial),float(tInicial),float(tFinal),functionFix,int(n.get()))
        fEulerMejorado = eulerMejorado(float(xInicial),float(tInicial),float(tFinal),functionFix,int(n.get()))
        fRungeKutta = rungeKutta(float(xInicial),float(tInicial),float(tFinal),functionFix,int(n.get()))
        
        print(fEuler)
        print(fEulerMejorado)              
        print(fRungeKutta)

        plt.title("Gráfico") 
        plt.xlabel("t") 
        plt.ylabel("X") 
        ejeTEuler = list(fEuler.keys())
        ejeXEuler = list(fEuler.values())
        ejeTEulerMejorado = list(fEulerMejorado.keys())
        ejeXEulerMejorado = list(fEulerMejorado.values())
        ejeTRungeKutta = list(fRungeKutta.keys())
        ejeXRungeKutta = list(fRungeKutta.values())

        tempTEuler = []
        tempXEuler = []
        tempTEulerMejorado = []
        tempXEulerMejorado = []
        tempTRungeKutta = []
        tempXRungeKutta = []
        primeraVez = True

        for i in range(int(n.get())+1):
            
            tempTEuler.append(ejeTEuler[i])
            tempXEuler.append(ejeXEuler[i])
            tempTEulerMejorado.append(ejeTEulerMejorado[i])
            tempXEulerMejorado.append(ejeXEulerMejorado[i])
            tempTRungeKutta.append(ejeTRungeKutta[i])
            tempXRungeKutta.append(ejeXRungeKutta[i])
            

            plt.scatter(tempTEuler, tempXEuler, color = "r")
            plt.scatter(tempTEulerMejorado, tempXEulerMejorado, color = "g")
            plt.scatter(tempTRungeKutta, tempXRungeKutta, color = "b")
            plt.pause(0.80)
            plt.plot(tempTEuler, tempXEuler, label = "Euler", color = "r",linewidth=2)
            plt.plot(tempTEulerMejorado, tempXEulerMejorado, label = "Euler Mejorado", color = "g",linewidth=2) 
            plt.plot(tempTRungeKutta, tempXRungeKutta, label = "Runge-Kutta", color = "b",linewidth=2)
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
def euler(x0,t0,tf,function,N):    
    try:
        x = x0
        t = t0
        h = (tf - t0) / N
        
        fResult = {} #Se crea un diccionario resultado que guarda x:y como clave:valor
        fResult[t] = x #Se asigna manualmente x0:y0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "x"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "y"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave x:y en el diccionario resultado
            functionEvaluated = f(t,x) #Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
            x = x + h * functionEvaluated        

        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")
#Algoritmo Euler Mejorado
def eulerMejorado(x0,t0,tf,function,N):    
    try:
        x = x0
        t = t0
        h = (tf - t0) / N
        
        fResult = {} #Se crea un diccionario resultado que guarda x:y como clave:valor
        fResult[t] = x #Se asigna manualmente x0:y0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "x"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "y"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave x:y en el diccionario resultado
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
            xOriginal = x #guardo el valor de y actual para cuando tenga que hacer el recalculo
            x = x + h * f(t,x) #predictor
            x = xOriginal + (h/2) * (f(t,xOriginal) + f(t+h,x)) #corrector
          
        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")
#Algoritmo Runge Kutta
def rungeKutta(x0,t0,tf,function,N):    
    try:
        x = x0
        t = t0
        h = (tf - t0) / N
        
        fResult = {} #Se crea un diccionario resultado que guarda x:y como clave:valor
        fResult[t] = x #Se asigna manualmente x0:y0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "x"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "y"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando x e y como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave x:y en el diccionario resultado
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de x e y
            p1 = h * f(t,x)
            p2 = h * f(t+(h/2),x+(p1/2))
            p3 = h * f(t+(h/2),x+(p2/2))
            p4 = h * f(t+h, x+p3)
            x = x + (1/6) * (p1+2*p2+2*p3+p4)
        return fResult
    except:
        messagebox.showerror("Métodos", "Error inesperado.")


Label(root, text="Parámetros: ", font = ('Lucida Bright',15), padx=10).grid(row=1,column=0)

parameters = LabelFrame(root, padx=50, pady=20)

Label(root, text="                            ").grid(row=2,column=1) #Espacio en pantalla

parameters.grid(row=3, column=1)

Label(parameters,text="X0= ", font = ('Lucida Bright',10)).grid(row=0,column=0)
x0 = Entry(parameters,width=10,borderwidth=5)
x0.grid(row=0,column=1, pady=5, padx=5)
Label(parameters,text="T0= ", font = ('Lucida Bright',10) ).grid(row=0,column=2)
t0 = Entry(parameters,width=10,borderwidth=5)
t0.grid(row=0,column=3, pady=5, padx=5)
Label(parameters,text="Tf= ", font = ('Lucida Bright',10)).grid(row=0,column=4)
tf = Entry(parameters,width=10,borderwidth=5)
tf.grid(row=0,column=5, pady=5, padx=5)
Label(parameters,text="f(t,x)= ", font = ('Lucida Bright',10)).grid(row=1,column=0)
function = Entry(parameters,width=10,borderwidth=5)
function.grid(row=1,column=1, pady=5, padx=5)
Label(parameters,text="N= ", font = ('Lucida Bright',10)).grid(row=1,column=2)
n = Entry(parameters,width=10,borderwidth=5)
n.grid(row=1,column=3, pady=5, padx=5)
Button(parameters,text="Calcular", font = ('Lucida Bright',15), command=btnCalcular).grid(row=1,column=5)

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