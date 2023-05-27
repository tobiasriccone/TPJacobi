import numpy as np
from tkinter import *
import re

def validarTolerancia(tol, alturaLabel):
    if tol.startswith(".") or tol == "":
        toleranciaIncompletaLabel.place(x=80, y=alturaLabel)
        raise Exception("Tolerancia incompleta")

def validarIteracionesMax(iteracionesMax, alturaLabel):
    if iteracionesMax == "":
        iteracionesIncompletasLabel.place(x=80, y=alturaLabel)
        raise Exception("Número iteraciones incompleto")

def armarFrame(alturaLabel):
    seccion.grid(row=1, column=0, padx=35, pady=alturaLabel, sticky="w")
    Label(content_frame, text="Iteraciones", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=70, pady=10)
    Label(content_frame, text="Vector Aprox.", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=70, pady=10)
    Label(content_frame, text="Distancia", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=70, pady=10)

def getXAMostrar(x):
    vector = "["
    primerElem = True
    for lista in x:
        for elem in lista:
            nro = str(round(float(elem), 3))
            if primerElem:
                vector += nro
            else:
                vector += ",  " + nro
            primerElem = False
    vector += "]"
    return vector

def jacobi(a, b, x0, tol, iteracionesMax, alturaLabel):
    toleranciaIncompletaLabel.place_forget()
    iteracionesIncompletasLabel.place_forget()
    validarTolerancia(tol, alturaLabel)
    cantNrosTol = len(str(tol).replace(".", ""))
    validarIteracionesMax(iteracionesMax, alturaLabel)
    getElementoPorTexto(Button, "Calcular X").config(state=DISABLED)
    inputTol.config(state=DISABLED)
    inputIterMax.config(state=DISABLED)
    armarFrame(alturaLabel+40)
    diag = np.diag(np.diag(a))
    lu = a - diag
    x = x0
    for i in range(int(iteracionesMax)):
        diagInv = np.linalg.inv(diag)
        xAux = x
        x = np.dot(diagInv, np.dot(-lu, x)) + np.dot(diagInv, b)
        xAMostrar = getXAMostrar(x)
        dist = round(np.linalg.norm(x - xAux), cantNrosTol - 1)
        Label(content_frame, text=i + 1, font=("Arial", 11)).grid(row=i + 1, column=0, padx=70,pady=10)
        Label(content_frame, text=xAMostrar, font=("Arial", 11)).grid(row=i + 1, column=1, padx=70,pady=10)
        Label(content_frame, text=dist, font=("Arial", 11)).grid(row=i + 1, column=2, padx=70,pady=10)
        if dist <= round(float(tol), cantNrosTol - 1):
            break
    Label(root, text=f"Vector X aproximado, obtenido en la iteración {i+1}: {xAMostrar}", font=("Arial", 11)).place(x=80, y=alturaLabel)

def getElementoPorTexto(tipoElemento, texto):
    for widget in root.winfo_children():
        if isinstance(widget, tipoElemento) and widget["text"] == texto:
            return widget
    raise Exception(f"No se encontró el elemento con el texto '{texto}'")

def deshabilitarInputsMatrices(listaDeListasDeListasInputs):
    for listaDeListas in listaDeListasDeListasInputs:
        for lista in listaDeListas:
            for input in lista:
                input.config(state=DISABLED)

def validarMatrizParaJacobi(matriz, alturaLabel):
    for row in range(len(matriz)):
        elemDiag = abs(matriz[row, row])
        sumOtrosElem = np.sum(np.abs(matriz[row, :])) - elemDiag
        if elemDiag <= sumOtrosElem:
            matrizInvalidaLabel.place(x=70, y=alturaLabel)
            raise Exception("La matriz no es diagonal dominante")
    matrizValidaLabel.place(x=70, y=alturaLabel)

def validarElemMatriz(valor, alturaLabel):
    if valor == "" or valor == "-" or valor.startswith(".") or valor.startswith("-."):
        matrizIncompletaLabel.place(x=70, y=alturaLabel)
        raise Exception("Matriz incompleta")

def obtenerMatrizDesdeInputs(listaFilasMatriz, alturaLabel):
    matriz = np.zeros((len(listaFilasMatriz), len(listaFilasMatriz[0])))
    i = 0
    j = 0
    for fila in listaFilasMatriz:
        for elemento in fila:
            valor = elemento.get()
            validarElemMatriz(valor, alturaLabel)
            matriz[i][j] = valor
            j += 1
        j = 0
        i += 1
    return matriz

def calcular(listaInputsMatriz, listaInputsVector, listaInputsSemilla, alturaLabel):
    matrizIncompletaLabel.place_forget()
    matrizInvalidaLabel.place_forget()
    matrizA = obtenerMatrizDesdeInputs(listaInputsMatriz, alturaLabel)
    vector = obtenerMatrizDesdeInputs(listaInputsVector, alturaLabel)
    semilla = obtenerMatrizDesdeInputs(listaInputsSemilla, alturaLabel)
    validarMatrizParaJacobi(matrizA, alturaLabel)
    getElementoPorTexto(Button, "Verificar").config(state=DISABLED)
    deshabilitarInputsMatrices([listaInputsMatriz, listaInputsVector, listaInputsSemilla])
    ingreseTolLabel.place(x=posX, y=alturaLabel+35)
    inputTol.place(x=155, y=alturaLabel+35, height=25)
    ingreseIterMaxLabel.place(x=posX, y=alturaLabel+70)
    inputIterMax.place(x=235, y=alturaLabel+70, width=30, height=25)
    Button(root, text="Calcular X", command=lambda: jacobi(matrizA, vector, semilla, inputTol.get(), inputIterMax.get(), alturaLabel+105)).place(x=posX, y=alturaLabel+105)

def crearInputs(fil, col, x0, y0):
    listaFilas = []
    x = x0
    for fila in range(fil):
        listaElementos = []
        for columna in range(col):
            input = Entry(root, validate="key", validatecommand=(root.register(teclaValida), '%P'))
            input.place(x=x, y=y0, width=30, height=25)
            listaElementos.append(input)
            x += 40
        listaFilas.append(listaElementos)
        ultimoX = x
        x = x0
        y0 += 40
    return listaFilas, ultimoX, y0

def validarDim(dim):
    dimInvalidaLabel.place_forget()
    if dim != "" and dim != "-" and dim.startswith(".") is False and dim != "-." and 4 > int(dim) > 0:
        inputDim.config(state=DISABLED)
        getElementoPorTexto(Button, "Siguiente").config(state=DISABLED)
    else:
        dimInvalidaLabel.place(x=posX, y=135)
        raise Exception("Dimension inválida")

def ingresarMatriz():
    dim = inputDim.get()
    validarDim(dim)
    dim = int(dim)
    Label(root, text="Ingrese la Matríz A, el Vector b y el Vector semilla:", font=("Arial", 11)).place(x=posX, y=135)
    listaInputsMatriz, ultimoXUsado, ultimaYUsadaMas40 = crearInputs(dim, dim, posX+5, 175)
    listaInputsVector, ultimoXUsado, ultimaYUsadaMas40 = crearInputs(dim, 1, ultimoXUsado+50, 175)
    listaInputsSemilla, ultimoXUsado, ultimaYUsadaMas40 = crearInputs(dim, 1, ultimoXUsado+50, 175)
    Button(root, text="Verificar", command=lambda: calcular(listaInputsMatriz, listaInputsVector, listaInputsSemilla, ultimaYUsadaMas40)).place(x=posX, y=ultimaYUsadaMas40)

def teclaValidaEnteroPositivo(input):
    return re.match("^(?:\d+)?$", input) is not None

def teclaValidaPositiva(input):
    return re.match(r"^\d*(?:\.\d*)?$", input) is not None

def teclaValida(input):
    return re.match(r"^(?:-)?\d*(?:\.\d*)?$", input) is not None

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def inicio():
    Label(root, text="TP Jacobi - Métodos Numéricos", font=("Arial", 16, "bold")).place(x=posX, y=10)
    Label(root, text="Grupo 08 conformado por Riccone y Nicotra", font=("Arial", 12, "bold")).place(x=posX, y=45)
    Label(root, text="------------------------------------", font=("Arial", 11)).place(x=posX, y=75)
    Label(root, text="Ingrese la dimensión de la Matriz cuadrada a resolver (1-3):", font=("Arial", 11)).place(x=posX, y=105)
    inputDim.place(x=405, y=105, width=30, height=25)
    Button(root, text="Siguiente", command=ingresarMatriz).place(x=445, y=103)

root = Tk()
root.geometry("800x600")
root.resizable(False, False)
root.title("Método Jacobi")

seccion = LabelFrame(root, text="Convergencia")
canvas = Canvas(seccion, width=700, height=120)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(seccion, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)
content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")
canvas.bind("<Configure>", on_canvas_configure)

posX = 10
inputDim = Entry(root, validate="key", validatecommand=(root.register(teclaValida), '%P'))
dimInvalidaLabel = Label(root, text="Dimension inválida, reintente", font=("Arial", 11), fg="red")
matrizIncompletaLabel = Label(root, text="Matriz incompleta", font=("Arial", 11), fg="red")
matrizInvalidaLabel = Label(root, text="Matriz no diagonal dominante", font=("Arial", 11), fg="red")
matrizValidaLabel = Label(root, text="Matriz diagonal dominante", font=("Arial", 11), fg="green")
ingreseTolLabel = Label(root, text="Ingrese la tolerancia:", font=("Arial", 11))
inputTol = Entry(root, validate="key", validatecommand=(root.register(teclaValidaPositiva), '%P'))
ingreseIterMaxLabel = Label(root, text="Ingrese las iteraciones máximas:", font=("Arial", 11))
inputIterMax = Entry(root, validate="key", validatecommand=(root.register(teclaValidaEnteroPositivo), '%P'))
toleranciaIncompletaLabel = Label(root, text="Tolerancia incompleta", font=("Arial", 11), fg="red")
iteracionesIncompletasLabel = Label(root, text="Número iteraciones máximas incompleto", font=("Arial", 11), fg="red")
inicio()

root.mainloop()