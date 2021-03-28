from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, font
import tkinter.ttk

import numpy as np
import sympy
import re
from matplotlib import pyplot as plt 


root = Tk()
appWidth = 960
appHeight= 410

screenWidth= root.winfo_screenwidth()
screenHeight= root.winfo_screenheight()
x= (screenWidth/2) - (appWidth/2)
y= (screenHeight/2) - (appHeight/2)
root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

root.title('Métodos')
root.resizable(0,0)
root.iconbitmap('Metodos.ico')

Label(root, text='Métodos', font = ('Lucida Bright',25,'underline'), pady=20, padx=40).grid(row = 1, column=1)

def graficarTabla(fEuler,fEulerMejorado,fRungeKutta):   
    global tables 
    tables = Toplevel(root)
    tables.title('Tablas')
    tables.geometry('500x600')
    tables.resizable(0,0)
    tables.iconbitmap('Metodos.ico')

    mainframe = Frame(tables)
    mainframe.pack(fill=BOTH,expand=1)
    
    canvas = Canvas(mainframe)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(mainframe,orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    secondFrame = Frame(canvas)
    canvas.create_window((0,0), window=secondFrame, anchor="nw")

    Label(secondFrame, text='t', font = ('Lucida Bright',15)).grid(row = 1, column=0)
    tkinter.ttk.Separator(secondFrame, orient=VERTICAL).grid(column=1, row=0, rowspan=5000, sticky=(tkinter.N, tkinter.S))
    Label(secondFrame, text='X', font = ('Lucida Bright',15)).grid(row = 0, column=4)
    tkinter.ttk.Separator(secondFrame, orient=HORIZONTAL).grid(column=1, row=1, columnspan=5000, sticky=(tkinter.W, tkinter.E))
    numCol = 2
    if(valorEuler.get()):
        Label(secondFrame, text='Euler', font = ('Lucida Bright',15)).grid(row = 2, column=numCol)
        tkinter.ttk.Separator(secondFrame, orient=VERTICAL).grid(column=numCol+1, row=2, rowspan=5000, sticky=(tkinter.N, tkinter.S))
        numCol = numCol+2
    if(valorEulerMejorado.get()):
        Label(secondFrame, text='Euler Mejorado', font = ('Lucida Bright',15)).grid(row = 2, column=numCol)
        tkinter.ttk.Separator(secondFrame, orient=VERTICAL).grid(column=numCol+1, row=2, rowspan=5000, sticky=(tkinter.N, tkinter.S))
        numCol = numCol+2
    if(valorRungeKutta.get()):        
        Label(secondFrame, text='Runge-Kutta', font = ('Lucida Bright',15)).grid(row = 2, column=numCol)
        tkinter.ttk.Separator(secondFrame, orient=VERTICAL).grid(column=numCol+1, row=0, rowspan=5000, sticky=(tkinter.N, tkinter.S))
        numCol = numCol+2

    tkinter.ttk.Separator(secondFrame, orient=HORIZONTAL).grid(column=0, row=3, columnspan=5000, sticky=(tkinter.W, tkinter.E))


    cont = 4
    for t in list(fEuler.keys()):
        display = round(t,4)
        display = format(display, '.4f')
        display = str(display)
        display = display.replace(".", ",")
        Label(secondFrame, text=display, font = ('Lucida Bright',15)).grid(row = cont, column=0)
        tkinter.ttk.Separator(secondFrame, orient=HORIZONTAL).grid(column=0, row=cont+1, columnspan=5000, sticky=(tkinter.W, tkinter.E))

        cont += 2

    numCol = 2
    if(valorEuler.get()):
        cont=4
        for xEuler in list(fEuler.values()):
            if(valorEuler.get()):
                if(np.isnan(xEuler)):
                    display = "NaN"
                else:
                    display = round(xEuler,4)
                    display = format(display, '.4f')
                    display = str(display)
                    display = display.replace(".", ",")
                Label(secondFrame, text=display, font = ('Lucida Bright',15), padx=10).grid(row = cont, column=numCol)
            else:
                Label(secondFrame, text="-", font = ('Lucida Bright',15)).grid(row = cont, column=numCol)
            cont += 2
        numCol = numCol + 2

    if(valorEulerMejorado.get()):    
        cont=4
        for xEulerM in list(fEulerMejorado.values()):
            if(valorEulerMejorado.get()):
                if(np.isnan(xEulerM)):
                    display = "NaN"
                else:
                    display = round(xEulerM,4)
                    display = format(display, '.4f')
                    display = str(display)
                    display = display.replace(".", ",")
                Label(secondFrame, text=display, font = ('Lucida Bright',15)).grid(row = cont, column=numCol)
            else:
                Label(secondFrame, text="-", font = ('Lucida Bright',15)).grid(row = cont, column=numCol)
            cont += 2
        numCol = numCol + 2

        
    if(valorRungeKutta.get()):        
        cont=4
        for xRK in list(fRungeKutta.values()):
            if(valorRungeKutta.get()):
                if(np.isnan(xRK)):
                    display = "NaN"
                else:
                    display = round(xRK,4)
                    display = format(display, '.4f')
                    display = str(display)
                    display = display.replace(".", ",")
                Label(secondFrame, text=display, font = ('Lucida Bright',15)).grid(row = cont, column=numCol)
            else:
                Label(secondFrame, text="-", font = ('Lucida Bright',15)).grid(row = cont, column=numCol)
            cont += 2
        numCol = numCol + 2

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
        sympy.lambdify((ts,xs),expr) #Sympy construye la función considerando t y x como variables, para posteriormente poder calcular su resultado solamente reemplazando esos valores
    except:
        return False
    return True

def btnCalcular():  
    try:
        tables.destroy()
        plt.close()
    except:
        pass

    xInicial = x0.get().replace(",",".")
    tInicial = t0.get().replace(",",".")
    tFinal = tf.get().replace(",",".")
    functionFix = function.get().replace(",",".")
    hIngresada = h.get().replace(",",".")
    params = [xInicial,tInicial,tFinal]
    if(inputIsValid(params) and nValidOrhValid(n.get(), hIngresada) and isMathFunction(functionFix) and not nAndh(n.get(), hIngresada) and (valorEuler.get() or valorEulerMejorado.get() or valorRungeKutta.get())):
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

        graficarTabla(fEuler,fEulerMejorado,fRungeKutta)

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
            #Simultáneo
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

        elif(v.get() == 2):
            #En orden
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
        else:
            #Gráfico inmediato
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
                
                if(valorEuler.get()):
                    plt.plot(tempTEuler, tempXEuler, label = "Euler", color = "r",linewidth=2)
                if(valorEulerMejorado.get()):            
                    plt.plot(tempTEulerMejorado, tempXEulerMejorado, label = "Euler Mejorado", color = "g",linewidth=2)
                if(valorRungeKutta.get()): 
                    plt.plot(tempTRungeKutta, tempXRungeKutta, label = "Runge-Kutta", color = "b",linewidth=2)
                plt.grid()
            
                if primeraVez:
                    plt.legend()
                    primeraVez = False
            plt.grid()
            plt.show()
              
    elif (not(valorEuler.get() or valorEulerMejorado.get() or valorRungeKutta.get())):
         messagebox.showerror("Métodos", "Debe seleccionar algún método para realizar los cálculos.")
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



parameters = LabelFrame(root, padx=30, pady=10)

Label(root, text="                            ").grid(row=2,column=1) #Espacio en pantalla

parameters.grid(row=3, column=1)
valorEuler = BooleanVar()
valorEulerMejorado = BooleanVar()
valorRungeKutta = BooleanVar()

muestraEuler = Checkbutton(parameters, text="Euler", font = ('Lucida Bright',13), variable=valorEuler, onvalue=True, offvalue=False)
muestraEuler.grid(row=0,column=0, padx=5)
muestraEuler.select()

muestraEulerMejorado = Checkbutton(parameters, text="Euler Mejorado", font = ('Lucida Bright',13), variable=valorEulerMejorado, onvalue=True, offvalue=False)
muestraEulerMejorado.grid(row=0,column=2, padx=5)
muestraEulerMejorado.select()

muestraRunge = Checkbutton(parameters, text="Runge Kutta", font = ('Lucida Bright',13), variable=valorRungeKutta, onvalue=True, offvalue=False)
muestraRunge.grid(row=0,column=4, pady=5, padx=5)
muestraRunge.select()


v = IntVar()

labelForma = Label(parameters, text="Forma de graficar:", font = ('Lucida Bright',13))
labelForma.grid(row=1,column=0, pady=5, padx=5)

r1 = Radiobutton(parameters, text="En simultáneo", font = ('Lucida Bright',13), variable=v, value=1,activeforeground="#1faa00")
r1.grid(row=1,column=1, pady=5, padx=5)


r2 = Radiobutton(parameters, text="En orden", font = ('Lucida Bright',13), variable=v, value=2,activeforeground="#1faa00")
r2.grid(row=1,column=2, padx=5)

r2 = Radiobutton(parameters, text="Inmediato",font = ('Lucida Bright',13), variable=v, value=3,activeforeground="#1faa00")
r2.grid(row=1,column=3, pady=5, padx=5)

v.set(1)


Label(parameters,text="x0= ", font = ('Lucida Bright',13)).grid(row=2,column=0)
x0 = Entry(parameters,width=20,borderwidth=5, font = ('Lucida Bright',13))
x0.grid(row=2,column=1, pady=5)

Label(parameters,text="t0= ", font = ('Lucida Bright',13) ).grid(row=2,column=2)
t0 = Entry(parameters,width=20,borderwidth=5,font = ('Lucida Bright',13))
t0.grid(row=2,column=3, pady=5)

Label(parameters,text="tf= ", font = ('Lucida Bright',13)).grid(row=3,column=0)
tf = Entry(parameters,width=20,borderwidth=5,font = ('Lucida Bright',13))
tf.grid(row=3,column=1, pady=5)

Label(parameters,text="f(x,t)= ", font = ('Lucida Bright',13)).grid(row=3,column=2)
function = Entry(parameters,width=20,borderwidth=5,font = ('Lucida Bright',13))
function.grid(row=3,column=3, pady=5)

Label(parameters,text="N= ", font = ('Lucida Bright',13)).grid(row=4,column=0)
n = Entry(parameters,width=20,borderwidth=5,font = ('Lucida Bright',13))
n.grid(row=4,column=1, pady=5)

Label(parameters,text="h= ", font = ('Lucida Bright',13)).grid(row=4,column=2)
h = Entry(parameters,width=20,borderwidth=5,font = ('Lucida Bright',13))
h.grid(row=4,column=3, pady=5)

Button(parameters,text="Calcular", font = ('Lucida Bright',15),background="#A2EFAC", activeforeground="white", activebackground="#85C38D",command=btnCalcular).grid(row=5,column=4)

root.mainloop()