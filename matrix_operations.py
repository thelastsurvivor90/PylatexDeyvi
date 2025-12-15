"""
Sistema de Álgebra Lineal con PyLaTeX
Generación de matrices aleatorias, cálculo de determinantes e inversas
con documentación paso a paso en LaTeX
"""

import numpy as np
from pylatex import Document, Section, Subsection, Math, Matrix as LatexMatrix
from pylatex import Package, NoEscape, Alignat
from pylatex.utils import bold
import random


class MatrixGenerator:
    """Clase para generar diferentes tipos de matrices aleatorias"""
    
    @staticmethod
    def matriz_fila(n=5, rango=(1, 10)):
        """Genera una matriz fila (1xn)"""
        return np.random.randint(rango[0], rango[1], size=(1, n))
    
    @staticmethod
    def matriz_columna(m=5, rango=(1, 10)):
        """Genera una matriz columna (mx1)"""
        return np.random.randint(rango[0], rango[1], size=(m, 1))
    
    @staticmethod
    def matriz_cuadrada(n=4, rango=(1, 10)):
        """Genera una matriz cuadrada (nxn)"""
        return np.random.randint(rango[0], rango[1], size=(n, n))
    
    @staticmethod
    def matriz_rectangular(m=3, n=5, rango=(1, 10)):
        """Genera una matriz rectangular (mxn)"""
        return np.random.randint(rango[0], rango[1], size=(m, n))
    
    @staticmethod
    def matriz_diagonal(n=4, rango=(1, 10)):
        """Genera una matriz diagonal"""
        matriz = np.zeros((n, n), dtype=int)
        np.fill_diagonal(matriz, np.random.randint(rango[0], rango[1], n))
        return matriz
    
    @staticmethod
    def matriz_triangular_superior(n=4, rango=(1, 10)):
        """Genera una matriz triangular superior"""
        matriz = np.random.randint(rango[0], rango[1], size=(n, n))
        return np.triu(matriz)
    
    @staticmethod
    def matriz_triangular_inferior(n=4, rango=(1, 10)):
        """Genera una matriz triangular inferior"""
        matriz = np.random.randint(rango[0], rango[1], size=(n, n))
        return np.tril(matriz)
    
    @staticmethod
    def matriz_identidad(n=4):
        """Genera una matriz identidad"""
        return np.eye(n, dtype=int)
    
    @staticmethod
    def matriz_nula(m=3, n=3):
        """Genera una matriz nula"""
        return np.zeros((m, n), dtype=int)


class DeterminantCalculator:
    """Clase para calcular determinantes usando el método de Gauss"""
    
    def __init__(self, matriz):
        self.matriz_original = np.array(matriz, dtype=float)
        self.matriz = np.array(matriz, dtype=float)
        self.pasos = []
        self.multiplicadores = 1
        
    def calcular_determinante(self):
        """Calcula el determinante usando eliminación gaussiana"""
        n = len(self.matriz)
        self.pasos.append(("Matriz original:", self.matriz.copy()))
        
        for i in range(n):
            # Búsqueda de pivote
            max_fila = i
            for k in range(i+1, n):
                if abs(self.matriz[k][i]) > abs(self.matriz[max_fila][i]):
                    max_fila = k
            
            # Intercambio de filas si es necesario
            if max_fila != i:
                self.matriz[[i, max_fila]] = self.matriz[[max_fila, i]]
                self.multiplicadores *= -1
                self.pasos.append((f"Intercambio F{i+1} ↔ F{max_fila+1}:", self.matriz.copy()))
            
            # Verificar si el pivote es cero
            if abs(self.matriz[i][i]) < 1e-10:
                return 0
            
            # Eliminación hacia abajo
            for j in range(i+1, n):
                if self.matriz[j][i] != 0:
                    factor = self.matriz[j][i] / self.matriz[i][i]
                    self.matriz[j] = self.matriz[j] - factor * self.matriz[i]
                    self.pasos.append((f"F{j+1} → F{j+1} - ({factor:.2f})F{i+1}:", self.matriz.copy()))
        
        # Calcular el determinante como producto de la diagonal
        determinante = self.multiplicadores * np.prod(np.diag(self.matriz))
        return determinante


class InverseCalculator:
    """Clase para calcular la matriz inversa"""
    
    def __init__(self, matriz):
        self.matriz = np.array(matriz, dtype=float)
        self.n = len(matriz)
        self.cofactores = None
        self.adjunta = None
        self.inversa = None
        
    def calcular_menor(self, i, j):
        """Calcula el menor de la matriz eliminando fila i y columna j"""
        submatriz = np.delete(np.delete(self.matriz, i, axis=0), j, axis=1)
        return np.linalg.det(submatriz)
    
    def calcular_cofactores(self):
        """Calcula la matriz de cofactores"""
        self.cofactores = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                menor = self.calcular_menor(i, j)
                self.cofactores[i][j] = ((-1) ** (i + j)) * menor
        return self.cofactores
    
    def calcular_adjunta(self):
        """Calcula la matriz adjunta (transpuesta de cofactores)"""
        if self.cofactores is None:
            self.calcular_cofactores()
        self.adjunta = self.cofactores.T
        return self.adjunta
    
    def calcular_inversa(self):
        """Calcula la matriz inversa"""
        det = np.linalg.det(self.matriz)
        if abs(det) < 1e-10:
            raise ValueError("La matriz no tiene inversa (determinante = 0)")
        
        if self.adjunta is None:
            self.calcular_adjunta()
        
        self.inversa = self.adjunta / det
        return self.inversa


class LaTeXDocumentGenerator:
    """Clase para generar documentos LaTeX con PyLaTeX"""
    
    def __init__(self, titulo="Operaciones con Matrices"):
        self.doc = Document()
        self.doc.packages.append(Package('amsmath'))
        self.doc.packages.append(Package('amssymb'))
        self.doc.packages.append(Package('babel', options=['spanish']))
        self.doc.preamble.append(NoEscape(r'\title{' + titulo + '}'))
        self.doc.preamble.append(NoEscape(r'\author{Sistema de Álgebra Lineal}'))
        self.doc.preamble.append(NoEscape(r'\date{\today}'))
        self.doc.append(NoEscape(r'\maketitle'))
    
    def agregar_matriz(self, matriz, titulo="Matriz"):
        """Agrega una matriz al documento"""
        with self.doc.create(Subsection(titulo)):
            with self.doc.create(Math(data=None)):
                mat_str = self._matriz_to_latex(matriz)
                self.doc.append(NoEscape(mat_str))
    
    def _matriz_to_latex(self, matriz):
        """Convierte una matriz numpy a formato LaTeX"""
        filas = matriz.shape[0]
        cols = matriz.shape[1]
        
        latex_str = r"\begin{bmatrix}" + "\n"
        for i in range(filas):
            fila = " & ".join([f"{matriz[i][j]:.2f}" if isinstance(matriz[i][j], float) 
                              else str(matriz[i][j]) for j in range(cols)])
            latex_str += fila
            if i < filas - 1:
                latex_str += r" \\" + "\n"
        latex_str += "\n" + r"\end{bmatrix}"
        return latex_str
    
    def documento_tipos_matrices(self):
        """Genera un documento con todos los tipos de matrices"""
        with self.doc.create(Section('Tipos de Matrices Aleatorias')):
            
            gen = MatrixGenerator()
            
            self.agregar_matriz(gen.matriz_fila(), "Matriz Fila (1x5)")
            self.agregar_matriz(gen.matriz_columna(), "Matriz Columna (5x1)")
            self.agregar_matriz(gen.matriz_cuadrada(), "Matriz Cuadrada (4x4)")
            self.agregar_matriz(gen.matriz_rectangular(), "Matriz Rectangular (3x5)")
            self.agregar_matriz(gen.matriz_diagonal(), "Matriz Diagonal (4x4)")
            self.agregar_matriz(gen.matriz_triangular_superior(), "Matriz Triangular Superior (4x4)")
            self.agregar_matriz(gen.matriz_triangular_inferior(), "Matriz Triangular Inferior (4x4)")
            self.agregar_matriz(gen.matriz_identidad(), "Matriz Identidad (4x4)")
            self.agregar_matriz(gen.matriz_nula(), "Matriz Nula (3x3)")
    
    def documento_determinante(self, matriz):
        """Genera un documento mostrando el cálculo del determinante"""
        with self.doc.create(Section('Cálculo de Determinante - Método de Gauss')):
            
            calc = DeterminantCalculator(matriz)
            det = calc.calcular_determinante()
            
            self.doc.append("A continuación se muestra el proceso paso a paso:\n\n")
            
            for descripcion, mat in calc.pasos:
                self.doc.append(NoEscape(r'\textbf{' + descripcion + r'}'))
                with self.doc.create(Math(data=None)):
                    self.doc.append(NoEscape(self._matriz_to_latex(mat)))
                self.doc.append("\n\n")
            
            self.doc.append(NoEscape(r'\textbf{Determinante final: } $\det(A) = ' + f'{det:.4f}' + r'$'))
    
    def documento_inversa(self, matriz):
        """Genera un documento mostrando el cálculo de la matriz inversa"""
        with self.doc.create(Section('Cálculo de Matriz Inversa')):
            
            calc = InverseCalculator(matriz)
            
            self.agregar_matriz(matriz, "Matriz Original A")
            
            cofactores = calc.calcular_cofactores()
            self.agregar_matriz(cofactores, "Matriz de Cofactores")
            
            adjunta = calc.calcular_adjunta()
            self.agregar_matriz(adjunta, "Matriz Adjunta (Transpuesta de Cofactores)")
            
            det = np.linalg.det(matriz)
            self.doc.append(NoEscape(r'\textbf{Determinante: } $\det(A) = ' + f'{det:.4f}' + r'$'))
            self.doc.append("\n\n")
            
            try:
                inversa = calc.calcular_inversa()
                self.doc.append(NoEscape(r'La matriz inversa se calcula como: $A^{-1} = \frac{1}{\det(A)} \cdot \text{Adj}(A)$'))
                self.doc.append("\n\n")
                self.agregar_matriz(inversa, "Matriz Inversa A⁻¹")
                
                # Verificación
                producto = np.dot(matriz, inversa)
                self.agregar_matriz(producto, "Verificación: A × A⁻¹ (debe ser I)")
                
            except ValueError as e:
                self.doc.append(str(e))
    
    def generar_pdf(self, nombre_archivo="output"):
        """Genera el archivo PDF"""
        self.doc.generate_pdf(nombre_archivo, clean_tex=False)


# Ejemplo de uso
if __name__ == "__main__":
    print("Sistema de Álgebra Lineal con PyLaTeX")
    print("=" * 50)
    
    # 1. Documento con tipos de matrices
    print("\n1. Generando documento con tipos de matrices...")
    doc1 = LaTeXDocumentGenerator("Tipos de Matrices Aleatorias")
    doc1.documento_tipos_matrices()
    doc1.generar_pdf("tipos_matrices")
    print("✓ Documento generado: tipos_matrices.pdf")
    
    # 2. Documento con cálculo de determinante
    print("\n2. Generando documento con cálculo de determinante...")
    matriz_det = np.array([[4, 3, 2], [1, 5, 7], [2, 8, 3]])
    doc2 = LaTeXDocumentGenerator("Cálculo de Determinante")
    doc2.documento_determinante(matriz_det)
    doc2.generar_pdf("calculo_determinante")
    print("✓ Documento generado: calculo_determinante.pdf")
    
    # 3. Documento con cálculo de matriz inversa
    print("\n3. Generando documento con cálculo de matriz inversa...")
    matriz_inv = np.array([[4, 7], [2, 6]])
    doc3 = LaTeXDocumentGenerator("Cálculo de Matriz Inversa")
    doc3.documento_inversa(matriz_inv)
    doc3.generar_pdf("calculo_inversa")
    print("✓ Documento generado: calculo_inversa.pdf")
    
    print("\n¡Todos los documentos han sido generados exitosamente!")
