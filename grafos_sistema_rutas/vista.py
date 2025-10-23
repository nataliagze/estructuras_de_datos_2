import tkinter as tk
from tkinter import ttk, font

class VistaApp(tk.Tk):
    """
    La Vista (GUI) de la aplicación.
    Hereda de tk.Tk para ser la ventana principal.
    """
    def __init__(self):
        super().__init__()
        self.title("OptiRuta - Planificador")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # Fuente personalizada (para que no se vea tan 'perfecto' o default)
        self.default_font = font.Font(family="Helvetica", size=10)
        
        # --- Contenedor Principal ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Título ---
        titulo_label = ttk.Label(
            main_frame, 
            text="Calculadora de Rutas", 
            font=("Helvetica", 16, "bold")
        )
        titulo_label.pack(pady=10)

        # --- Frame de Selección ---
        seleccion_frame = ttk.Frame(main_frame, padding="10")
        seleccion_frame.pack(fill=tk.X)

        ttk.Label(seleccion_frame, text="Ciudad Origen:", font=self.default_font).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_origen = ttk.Combobox(seleccion_frame, state="readonly", width=20, font=self.default_font)
        self.combo_origen.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(seleccion_frame, text="Ciudad Destino:", font=self.default_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_destino = ttk.Combobox(seleccion_frame, state="readonly", width=20, font=self.default_font)
        self.combo_destino.grid(row=1, column=1, padx=5, pady=5)

        # --- Frame de Opciones ---
        opciones_frame = ttk.LabelFrame(main_frame, text="Tipo de Ruta", padding="10")
        opciones_frame.pack(fill=tk.X, pady=10)
        
        self.opcion_ruta = tk.StringVar(value="km") # Variable de control

        radio_km = ttk.Radiobutton(
            opciones_frame, 
            text="Ruta más económica (Menos Kilómetros)", 
            variable=self.opcion_ruta, 
            value="km"
        )
        radio_km.pack(anchor="w")

        radio_paradas = ttk.Radiobutton(
            opciones_frame, 
            text="Ruta más rápida (Menos Paradas)", 
            variable=self.opcion_ruta, 
            value="paradas"
        )
        radio_paradas.pack(anchor="w")

        # --- Botones ---
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill=tk.X, pady=10)
        
        self.boton_calcular = ttk.Button(botones_frame, text="Calcular Ruta")
        self.boton_calcular.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.boton_dot = ttk.Button(botones_frame, text="Ver Mapa Interactivo")
        self.boton_dot.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # --- Frame de Resultado ---
        resultado_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
        resultado_frame.pack(fill=tk.BOTH, expand=True)

        self.label_resultado = ttk.Label(
            resultado_frame, 
            text="Seleccione origen, destino y tipo de ruta...", 
            font=("Courier", 10),
            wraplength=400, # Para que el texto se ajuste
            justify=tk.LEFT
        )
        self.label_resultado.pack(anchor="nw", pady=5)