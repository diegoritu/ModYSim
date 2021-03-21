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

def nValidOrhValid(n, h):
    try:
        if (n != ""):
            int(n)
        else:
            float(h)
    except:
        return False 
    return True

def nAndh(n, h):
    if ((n != "" and h != "") or (n == "" and h == "")):
        return True
    else:
        return False

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
    hIngresada = h.get().replace(",",".")
    print("HEY, ENTRÉ")  
    params = [xInicial,tInicial,tFinal]
    if(inputIsValid(params) and nValidOrhValid(n.get(), hIngresada) and isMathFunction(functionFix) and not nAndh(n.get(), hIngresada)):
        print("HEY, SOY VALIDO")
        N = n.get()
        if(n.get() != ""):
            N = int(N)
        else:
            #Ingresa h en vez de N
            N = int((float(tFinal) - float(tInicial)) / float(hIngresada))
            print(N)



        fEuler = euler(float(xInicial),float(tInicial),float(tFinal),functionFix,N)
        fEulerMejorado = eulerMejorado(float(xInicial),float(tInicial),float(tFinal),functionFix,N)
        fRungeKutta = rungeKutta(float(xInicial),float(tInicial),float(tFinal),functionFix,N)
        
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
        
        if(v.get() == 1):

            for i in range(N+1):
                
                if(valorEuler.get()):
                    tempTEuler.append(ejeTEuler[i])
                    tempXEuler.append(ejeXEuler[i])
                if(valorEulerMejorado.get()):
                    tempTEulerMejorado.append(ejeTEulerMejorado[i])
                    tempXEulerMejorado.append(ejeXEulerMejorado[i])
                if(valorRungeKutta.get()):
                    tempTRungeKutta.append(ejeTRungeKutta[i])
                    tempXRungeKutta.append(ejeXRungeKutta[i])
                
                if(valorEuler.get()):
                    plt.scatter(tempTEuler, tempXEuler, color = "r")
                if(valorEulerMejorado.get()):           
                    plt.scatter(tempTEulerMejorado, tempXEulerMejorado, color = "g")
                if(valorRungeKutta.get()):            
                    plt.scatter(tempTRungeKutta, tempXRungeKutta, color = "b")
                plt.grid()
                plt.pause(0.80)
                
                if(valorEuler.get()):
                    plt.plot(tempTEuler, tempXEuler, label = "Euler", color = "r",linewidth=2)
                if(valorEulerMejorado.get()):            
                    plt.plot(tempTEulerMejorado, tempXEulerMejorado, label = "Euler Mejorado", color = "g",linewidth=2)
                if(valorRungeKutta.get()): 
                    plt.plot(tempTRungeKutta, tempXRungeKutta, label = "Runge-Kutta", color = "b",linewidth=2)
                plt.grid()
                plt.pause(0.80)
            
                if primeraVez:
                    plt.legend()
                    primeraVez = False

            plt.grid()       
            plt.show()

        else:
            if(valorEuler.get()):
                for i in range(N+1):
                    
                    tempTEuler.append(ejeTEuler[i])
                    tempXEuler.append(ejeXEuler[i])
                    
                    plt.scatter(tempTEuler, tempXEuler, color = "r")
                    plt.grid()
                    plt.pause(0.80)
                    
                    if(primeraVez):
                        plt.plot(tempTEuler, tempXEuler, label = "Euler", color = "r",linewidth=2)
                    else:
                        plt.plot(tempTEuler, tempXEuler, label = "", color = "r",linewidth=2)

                    plt.grid()
                    plt.pause(0.80)
                
                    if primeraVez:
                        plt.legend()
                        primeraVez = False
            
            if(valorEulerMejorado.get()):
                primeraVez = True
                for i in range(N+1):
                    
                    tempTEulerMejorado.append(ejeTEulerMejorado[i])
                    tempXEulerMejorado.append(ejeXEulerMejorado[i])
                    
                    plt.scatter(tempTEulerMejorado, tempXEulerMejorado, color = "g")
                    plt.grid()
                    plt.pause(0.80)
                    if(primeraVez):
                        plt.plot(tempTEulerMejorado, tempXEulerMejorado, label = "Euler Mejorado", color = "g",linewidth=2)
                    else:
                        plt.plot(tempTEulerMejorado, tempXEulerMejorado, label = "", color = "g",linewidth=2)
                    plt.grid()
                    plt.pause(0.80)
                
                    if primeraVez:
                        
                        plt.legend()
                        primeraVez = False
            
            if(valorRungeKutta.get()):
                primeraVez = True
                for i in range(N+1):
                    
                    tempTRungeKutta.append(ejeTRungeKutta[i])
                    tempXRungeKutta.append(ejeXRungeKutta[i])
                    
                    plt.scatter(tempTRungeKutta, tempXRungeKutta, color = "b")
                    plt.grid()
                    plt.pause(0.80)
                    
                    if(primeraVez):
                        plt.plot(tempTRungeKutta, tempXRungeKutta, label = "Runge-Kutta", color = "b",linewidth=2)
                    else:
                        plt.plot(tempTRungeKutta, tempXRungeKutta, label = "", color = "b",linewidth=2)

                    plt.grid()
                    plt.pause(0.80)
                
                    if primeraVez:
                        plt.legend()
                        primeraVez = False

            plt.grid()       
            plt.show()
              
    elif(nAndh(n.get(), hIngresada)):
        if(n.get() != "" and h.get() != ""):
            messagebox.showerror("Métodos", "Debe ingresar el valor de N o h.")
        else:
            messagebox.showerror("Métodos", "No puede ingresar tanto N como h. Debe elegir uno de los 2 para ingresar.")
    elif(not nValidOrhValid(n.get(), hIngresada)):
        if(n.get() != ""):
            messagebox.showerror("Métodos", "N inválida.")
        else:
            messagebox.showerror("Métodos", "h inválida.")
    elif(not isMathFunction(function.get())):
        messagebox.showerror("Métodos", "Función inválida.")
    else:
        messagebox.showerror("Métodos", "Datos inválidos. Por favor revise t0, tf y x0.")




#Algoritmo Euler
def euler(x0,t0,tf,function,N):    
    try:
        x = x0
        t = t0
        h = (tf - t0) / N
        
        fResult = {} #Se crea un diccionario resultado que guarda t:x como clave:valor
        fResult[t] = x #Se asigna manualmente t0:x0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "t"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando t y x como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave t:x en el diccionario resultado
            functionEvaluated = f(t,x) #Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de t y x
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
        
        fResult = {} #Se crea un diccionario resultado que guarda t:x como clave:valor
        fResult[t] = x #Se asigna manualmente t0:x0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "t"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando t y x como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave t:x en el diccionario resultado
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de t y x
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
        
        fResult = {} #Se crea un diccionario resultado que guarda t:x como clave:valor
        fResult[t] = x #Se asigna manualmente t0:x0
        expr = sympy.sympify(function) #Se guarda en expr la misma expresión que se introdujo en function, pero formateada como expresión de simpy
        ts = sympy.Symbol('t') #Se le declara a sympy que existe una variable llamada "t"
        xs = sympy.Symbol('x') #Se le declara a sympy que existe una variable llamada "x"
        f = sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando t y x como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
        for k in range(N+1): #Se recorre k desde 0 hasta N
            t = t0 + k * h  
            fResult[t] = x #Se asigna una nueva clave t:x en el diccionario resultado
            #f(x,y): Se evalúa la función f (anteriormente dinamizada con lambdify) con los valores específicos de t y x
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
valorEuler = BooleanVar()
valorEulerMejorado = BooleanVar()
valorRungeKutta = BooleanVar()

muestraEuler = Checkbutton(parameters, text="Euler", variable=valorEuler, onvalue=True, offvalue=False)
muestraEuler.grid(row=0,column=0, pady=5, padx=5)
muestraEuler.select()

muestraEulerMejorado = Checkbutton(parameters, text="Euler Mejorado", variable=valorEulerMejorado, onvalue=True, offvalue=False)
muestraEulerMejorado.grid(row=0,column=2, pady=5, padx=5)
muestraEulerMejorado.select()

muestraRunge = Checkbutton(parameters, text="Runge Kutta", variable=valorRungeKutta, onvalue=True, offvalue=False)
muestraRunge.grid(row=0,column=4, pady=5, padx=5)
muestraRunge.select()


v = IntVar()

labelForma = Label(parameters, text="Forma de graficar:")
labelForma.grid(row=1,column=0, pady=5, padx=5)

r1 = Radiobutton(parameters, text="En simultáneo", variable=v, value=1)
r1.grid(row=1,column=1, pady=5, padx=5)


r2 = Radiobutton(parameters, text="En orden", variable=v, value=2)
r2.grid(row=1,column=2, pady=5, padx=5)

v.set(1)


Label(parameters,text="X0= ", font = ('Lucida Bright',10)).grid(row=2,column=0)
x0 = Entry(parameters,width=10,borderwidth=5)
x0.grid(row=2,column=1, pady=5, padx=5)
Label(parameters,text="T0= ", font = ('Lucida Bright',10) ).grid(row=2,column=2)
t0 = Entry(parameters,width=10,borderwidth=5)
t0.grid(row=2,column=3, pady=5, padx=5)
Label(parameters,text="Tf= ", font = ('Lucida Bright',10)).grid(row=2,column=4)
tf = Entry(parameters,width=10,borderwidth=5)
tf.grid(row=2,column=5, pady=5, padx=5)
Label(parameters,text="f(t,x)= ", font = ('Lucida Bright',10)).grid(row=3,column=0)
function = Entry(parameters,width=10,borderwidth=5)
function.grid(row=3,column=1, pady=5, padx=5)
Label(parameters,text="N= ", font = ('Lucida Bright',10)).grid(row=3,column=2)
n = Entry(parameters,width=10,borderwidth=5)
n.grid(row=3,column=3, pady=5, padx=5)
Label(parameters,text="h= ", font = ('Lucida Bright',10)).grid(row=3,column=4)
h = Entry(parameters,width=10,borderwidth=5)
h.grid(row=3,column=5, pady=5, padx=5)
Button(parameters,text="Calcular", font = ('Lucida Bright',15), command=btnCalcular).grid(row=4,column=1)

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