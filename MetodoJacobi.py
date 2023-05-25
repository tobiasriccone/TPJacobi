import numpy as np


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


a = np.array([[10, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8]])
b = np.array([6, 25, -11, 15])
x0 = np.zeros_like(b)
x1 = jacobi(a, b, x0, 1e-3, 100)
print(f"\nSolución del sistema: {x1}")