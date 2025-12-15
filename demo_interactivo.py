"""
Interfaz interactiva para el Sistema de Álgebra Lineal
Permite al usuario elegir operaciones y personalizar parámetros
"""

from matrix_operations import (
    MatrixGenerator, 
    DeterminantCalculator, 
    InverseCalculator, 
    LaTeXDocumentGenerator
)
import numpy as np


def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "="*60)
    print("  SISTEMA DE ÁLGEBRA LINEAL CON PYLATEX")
    print("="*60)
    print("\n[1] Generar diferentes tipos de matrices")
    print("[2] Calcular determinante (Método de Gauss)")
    print("[3] Calcular matriz inversa")
    print("[4] Generar documento completo con todos los ejemplos")
    print("[5] Salir")
    print("\n" + "="*60)


def menu_tipos_matrices():
    """Menú para generar tipos de matrices"""
    print("\n--- TIPOS DE MATRICES ---")
    print("[1] Matriz Fila")
    print("[2] Matriz Columna")
    print("[3] Matriz Cuadrada")
    print("[4] Matriz Rectangular")
    print("[5] Matriz Diagonal")
    print("[6] Matriz Triangular Superior")
    print("[7] Matriz Triangular Inferior")
    print("[8] Matriz Identidad")
    print("[9] Matriz Nula")
    print("[10] Todas las anteriores")
    
    opcion = input("\nSeleccione tipo de matriz: ")
    
    gen = MatrixGenerator()
    doc = LaTeXDocumentGenerator("Matrices Generadas")
    
    matrices = {
        "1": ("Matriz Fila", gen.matriz_fila()),
        "2": ("Matriz Columna", gen.matriz_columna()),
        "3": ("Matriz Cuadrada", gen.matriz_cuadrada()),
        "4": ("Matriz Rectangular", gen.matriz_rectangular()),
        "5": ("Matriz Diagonal", gen.matriz_diagonal()),
        "6": ("Matriz Triangular Superior", gen.matriz_triangular_superior()),
        "7": ("Matriz Triangular Inferior", gen.matriz_triangular_inferior()),
        "8": ("Matriz Identidad", gen.matriz_identidad()),
        "9": ("Matriz Nula", gen.matriz_nula()),
    }
    
    if opcion == "10":
        doc.documento_tipos_matrices()
        doc.generar_pdf("todas_las_matrices")
        print("\n✓ Documento generado: todas_las_matrices.pdf")
    elif opcion in matrices:
        titulo, matriz = matrices[opcion]
        print(f"\n{titulo}:")
        print(matriz)
        doc.agregar_matriz(matriz, titulo)
        doc.generar_pdf(f"matriz_{opcion}")
        print(f"\n✓ Documento generado: matriz_{opcion}.pdf")
    else:
        print("Opción no válida")


def menu_determinante():
    """Menú para calcular determinantes"""
    print("\n--- CÁLCULO DE DETERMINANTE ---")
    print("[1] Usar matriz aleatoria 3x3")
    print("[2] Usar matriz aleatoria 4x4")
    print("[3] Ingresar matriz manualmente")
    
    opcion = input("\nSeleccione opción: ")
    
    if opcion == "1":
        matriz = np.random.randint(1, 10, size=(3, 3))
    elif opcion == "2":
        matriz = np.random.randint(1, 10, size=(4, 4))
    elif opcion == "3":
        try:
            n = int(input("Ingrese el tamaño de la matriz (n×n): "))
            print(f"Ingrese los elementos de la matriz {n}×{n}:")
            matriz = []
            for i in range(n):
                fila = []
                for j in range(n):
                    valor = float(input(f"Elemento [{i+1},{j+1}]: "))
                    fila.append(valor)
                matriz.append(fila)
            matriz = np.array(matriz)
        except:
            print("Error en la entrada de datos")
            return
    else:
        print("Opción no válida")
        return
    
    print("\nMatriz seleccionada:")
    print(matriz)
    
    calc = DeterminantCalculator(matriz)
    det = calc.calcular_determinante()
    
    print(f"\n✓ Determinante calculado: {det:.4f}")
    
    # Generar documento
    doc = LaTeXDocumentGenerator("Cálculo de Determinante")
    doc.documento_determinante(matriz)
    doc.generar_pdf("determinante_calculado")
    print("✓ Documento generado: determinante_calculado.pdf")


def menu_matriz_inversa():
    """Menú para calcular matriz inversa"""
    print("\n--- CÁLCULO DE MATRIZ INVERSA ---")
    print("[1] Usar matriz aleatoria 2x2")
    print("[2] Usar matriz aleatoria 3x3")
    print("[3] Ingresar matriz manualmente")
    
    opcion = input("\nSeleccione opción: ")
    
    if opcion == "1":
        # Generar matriz 2x2 con determinante no nulo
        while True:
            matriz = np.random.randint(1, 10, size=(2, 2))
            if np.linalg.det(matriz) != 0:
                break
    elif opcion == "2":
        # Generar matriz 3x3 con determinante no nulo
        while True:
            matriz = np.random.randint(1, 10, size=(3, 3))
            if np.linalg.det(matriz) != 0:
                break
    elif opcion == "3":
        try:
            n = int(input("Ingrese el tamaño de la matriz (n×n): "))
            print(f"Ingrese los elementos de la matriz {n}×{n}:")
            matriz = []
            for i in range(n):
                fila = []
                for j in range(n):
                    valor = float(input(f"Elemento [{i+1},{j+1}]: "))
                    fila.append(valor)
                matriz.append(fila)
            matriz = np.array(matriz)
        except:
            print("Error en la entrada de datos")
            return
    else:
        print("Opción no válida")
        return
    
    print("\nMatriz seleccionada:")
    print(matriz)
    
    # Verificar que tenga inversa
    det = np.linalg.det(matriz)
    if abs(det) < 1e-10:
        print("\n⚠ Esta matriz NO tiene inversa (determinante = 0)")
        return
    
    print(f"\nDeterminante: {det:.4f}")
    
    try:
        calc = InverseCalculator(matriz)
        inversa = calc.calcular_inversa()
        
        print("\n✓ Matriz inversa calculada:")
        print(inversa)
        
        # Generar documento
        doc = LaTeXDocumentGenerator("Cálculo de Matriz Inversa")
        doc.documento_inversa(matriz)
        doc.generar_pdf("inversa_calculada")
        print("\n✓ Documento generado: inversa_calculada.pdf")
        
    except Exception as e:
        print(f"\n⚠ Error: {e}")


def generar_documento_completo():
    """Genera un documento completo con todos los ejemplos"""
    print("\n--- GENERANDO DOCUMENTO COMPLETO ---")
    print("Este proceso puede tomar unos segundos...")
    
    # Documento 1: Tipos de matrices
    print("\n[1/3] Generando tipos de matrices...")
    doc1 = LaTeXDocumentGenerator("Tipos de Matrices Aleatorias")
    doc1.documento_tipos_matrices()
    doc1.generar_pdf("01_tipos_matrices")
    
    # Documento 2: Determinante
    print("[2/3] Generando cálculo de determinante...")
    matriz_det = np.array([[4, 3, 2, 1], [2, 5, 7, 3], [1, 8, 3, 6], [3, 2, 9, 4]])
    doc2 = LaTeXDocumentGenerator("Cálculo de Determinante - Método de Gauss")
    doc2.documento_determinante(matriz_det)
    doc2.generar_pdf("02_determinante")
    
    # Documento 3: Matriz inversa
    print("[3/3] Generando cálculo de matriz inversa...")
    matriz_inv = np.array([[4, 7, 2], [1, 6, 3], [2, 5, 8]])
    doc3 = LaTeXDocumentGenerator("Cálculo de Matriz Inversa Completo")
    doc3.documento_inversa(matriz_inv)
    doc3.generar_pdf("03_matriz_inversa")
    
    print("\n" + "="*60)
    print("✓ TODOS LOS DOCUMENTOS GENERADOS EXITOSAMENTE")
    print("="*60)
    print("\nArchivos creados:")
    print("  • 01_tipos_matrices.pdf")
    print("  • 02_determinante.pdf")
    print("  • 03_matriz_inversa.pdf")
    print("\n" + "="*60)


def main():
    """Función principal del programa interactivo"""
    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            menu_tipos_matrices()
        elif opcion == "2":
            menu_determinante()
        elif opcion == "3":
            menu_matriz_inversa()
        elif opcion == "4":
            generar_documento_completo()
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n⚠ Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "BIENVENIDO AL SISTEMA" + " "*22 + "║")
    print("║" + " "*10 + "DE ÁLGEBRA LINEAL CON PYLATEX" + " "*19 + "║")
    print("╚" + "═"*58 + "╝")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario!")
    except Exception as e:
        print(f"\n⚠ Error inesperado: {e}")
        print("Por favor, reporte este error al desarrollador.")
