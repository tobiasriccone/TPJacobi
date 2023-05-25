import numpy as np
from tkinter import *
import re

def jacobi(a, b, x0, tol, iteracionesMax):
    diag = np.diag(np.diag(a))
    lu = a - diag
    x = x0
    for i in range(iteracionesMax):
        diagInv = np.linalg.inv(diag)
        xAux = x
        x = np.dot(diagInv, np.dot(-lu, x)) + np.dot(diagInv, b)
        dist = np.linalg.norm(x - xAux)
        print(f"\nIteración {i+1}\nX = {x}\nDistancia: {dist}")
        if dist < tol:
            return x
    return x

def getElementoPorTexto(tipoElemento, texto):
    for widget in root.winfo_children():
        if isinstance(widget, tipoElemento) and widget["text"] == texto:
            return widget
    raise Exception(f"No se encontró el elemento con el texto '{texto}'")

def validarElemMatriz(valor, alturaLabel):
    matrizIncompletaLabel.place_forget()
    if valor == "" or valor == "-" or valor.startswith("."):
        matrizIncompletaLabel.place(x=posX, y=alturaLabel)
        raise Exception("Matriz incompleta")

def obtenerMatrizDesdeInputs(listaFilasMatriz, alturaLabel):
    matrizIncompletaLabel.place_forget()
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

def calcular(listaInputsMatriz, listaInputsVector, alturaLabel):
    matrizA = obtenerMatrizDesdeInputs(listaInputsMatriz, alturaLabel)
    vector = obtenerMatrizDesdeInputs(listaInputsVector, alturaLabel)

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
    if dim != "" and dim != "-" and dim.startswith(".") is False and 5 > int(dim) > 0:
        inputDim.config(state=DISABLED)
        getElementoPorTexto(Button, "Siguiente").config(state=DISABLED)
    else:
        dimInvalidaLabel.place(x=posX, y=135)
        raise Exception("Dimension inválida")

def ingresarMatriz():
    dim = inputDim.get()
    validarDim(dim)
    dim = int(dim)
    Label(root, text="Ingrese la Matríz A y su Vector b:", font=("Arial", 11)).place(x=posX, y=135)
    listaInputsMatriz, ultimoXUsado, ultimaYUsadaMas40 = crearInputs(dim, dim, posX+5, 175)
    listaInputsVector, ultimoXUsado, ultimaYUsadaMas40 = crearInputs(dim, 1, ultimoXUsado+50, 175)
    Button(root, text="Calcular X", command=lambda: calcular(listaInputsMatriz, listaInputsVector, ultimaYUsadaMas40)).place(x=230, y=135)

def teclaValida(input):
    return re.match(r"^(?:-)?\d*(?:\.\d*)?$", input) is not None

def inicio():
    Label(root, text="TP Jacobi - Métodos Numéricos", font=("Arial", 16, "bold")).place(x=posX, y=10)
    Label(root, text="Grupo 08 conformado por Riccone y Nicotra", font=("Arial", 12, "bold")).place(x=posX, y=45)
    Label(root, text="------------------------------------", font=("Arial", 11)).place(x=posX, y=75)
    Label(root, text="Ingrese la dimensión de la Matriz cuadrada a resolver (1-4):", font=("Arial", 11)).place(x=posX, y=105)
    inputDim.place(x=405, y=105, width=30, height=25)
    Button(root, text="Siguiente", command=ingresarMatriz).place(x=445, y=103)

root = Tk()
root.geometry("800x600")
root.title("Método Jacobi")

posX = 10
inputDim = Entry(root, validate="key", validatecommand=(root.register(teclaValida), '%P'))
dimInvalidaLabel = Label(root, text="Dimension inválida, reintente", font=("Arial", 11), fg="red")
matrizIncompletaLabel = Label(root, text="Matriz incompleta", font=("Arial", 11), fg="red")
inicio()

root.mainloop()