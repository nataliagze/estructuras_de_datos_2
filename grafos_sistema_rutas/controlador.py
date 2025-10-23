import tkinter as tk
from tkinter import Toplevel, Text
from tkinter import ttk
import webbrowser  
import os          

class Controlador:
    """
    El Controlador que une la Vista y el Modelo.
    """
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        
        # Asignar los "comandos" (event handlers) a los botones de la vista
        self.vista.boton_calcular.config(command=self.manejar_calculo)
        # EN: __init__(self, modelo, vista):
        self.vista.boton_dot.config(command=self.mostrar_mapa_interactivo)

    def iniciar(self):
        """Inicia la aplicación."""
        self._cargar_datos_demo()
        self._actualizar_combos()
        self.vista.mainloop() # Inicia el bucle de la GUI

    def _cargar_datos_demo(self):
        """Carga un mapa ficticio en el modelo."""
        # Esto simula cargar datos desde una BD o archivo
        ciudades = ["La Paz", "Cochabamba", "Santa Cruz", "Oruro", "Potosí", "Tarija", "Sucre"]
        for c in ciudades:
            self.modelo.agregar_ciudad(c)

        self.modelo.agregar_carretera("La Paz", "Oruro", 230)
        self.modelo.agregar_carretera("La Paz", "Cochabamba", 380)
        self.modelo.agregar_carretera("Oruro", "Cochabamba", 210)
        self.modelo.agregar_carretera("Oruro", "Potosí", 330)
        self.modelo.agregar_carretera("Cochabamba", "Santa Cruz", 470)
        self.modelo.agregar_carretera("Cochabamba", "Sucre", 360)
        self.modelo.agregar_carretera("Santa Cruz", "Sucre", 550) # Ruta larga
        self.modelo.agregar_carretera("Sucre", "Potosí", 160)
        self.modelo.agregar_carretera("Potosí", "Tarija", 340)

    def _actualizar_combos(self):
        """Actualiza las listas desplegables con las ciudades del modelo."""
        ciudades = self.modelo.obtener_ciudades()
        ciudades.sort() # Orden alfabético
        
        self.vista.combo_origen['values'] = ciudades
        self.vista.combo_destino['values'] = ciudades
        
        if ciudades:
            self.vista.combo_origen.set(ciudades[0])
            self.vista.combo_destino.set(ciudades[1])

    def manejar_calculo(self):
        """
        Se ejecuta al presionar el botón 'Calcular'.
        Obtiene datos de la vista, llama al modelo y actualiza la vista.
        """
        origen = self.vista.combo_origen.get()
        destino = self.vista.combo_destino.get()
        tipo_ruta = self.vista.opcion_ruta.get()

        # Validación "no tan perfecta" (básica)
        if not origen or not destino:
            self.vista.label_resultado.config(text="Error: Debe seleccionar un origen y un destino.")
            return
        
        if origen == destino:
            self.vista.label_resultado.config(text="Error: El origen y el destino no pueden ser iguales.")
            return

        ruta = None
        costo = 0
        
        try:
            if tipo_ruta == "km":
                (ruta, costo) = self.modelo.encontrar_ruta_dijkstra(origen, destino)
                tipo_costo = "Kilómetros"
            else:
                (ruta, costo) = self.modelo.encontrar_ruta_bfs(origen, destino)
                tipo_costo = "Paradas"

            # Formatear el resultado
            if ruta:
                texto_ruta = " -> ".join(ruta)
                texto_resultado = f"Tipo de Cálculo: {tipo_costo}\n\n"
                texto_resultado += f"Ruta Óptima:\n{texto_ruta}\n\n"
                texto_resultado += f"Costo Total: {costo} {tipo_costo.lower()}"
            else:
                texto_resultado = f"No se encontró una ruta entre {origen} y {destino}."

            self.vista.label_resultado.config(text=texto_resultado)

        except Exception as e:
            # Manejo de error genérico
            self.vista.label_resultado.config(text=f"Ocurrió un error inesperado:\n{e}")

    def mostrar_mapa_interactivo(self):
        """
        Genera el mapa HTML y lo abre en el navegador.
        """
        # 1. Llama al nuevo método del modelo
        nombre_archivo = self.modelo.generar_mapa_interactivo()

        if nombre_archivo:
            # 2. Obtener la ruta absoluta del archivo
            # Esto es clave para que el navegador lo encuentre
            ruta_absoluta = f"file://{os.path.realpath(nombre_archivo)}"

            # 3. Abrir el archivo en el navegador web
            webbrowser.open(ruta_absoluta)

            # 4. (Opcional) Actualizar la UI
            self.vista.label_resultado.config(
                text=f"Mapa interactivo generado y abierto en tu navegador."
            )
        else:
            self.vista.label_resultado.config(
                text="Error: No se pudo generar el mapa interactivo."
            )