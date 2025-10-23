# main.py
from modelo import Grafo
from vista import VistaApp
from controlador import Controlador

if __name__ == "__main__":
    # 1. Crear las instancias de las tres partes
    modelo_principal = Grafo()
    vista_principal = VistaApp()
    
    # 2. Inyectar el modelo y la vista en el controlador
    controlador_principal = Controlador(modelo_principal, vista_principal)
    
    # 3. Iniciar la aplicación
    controlador_principal.iniciar()