import pandas as pd
from tkinter import *
from tkinter import ttk

# Crear la interfaz gráfica
root = Tk()
root.title("Detector de Anomalías")
control_frame = Frame(root)
control_frame.pack(pady=20)

table_label = Label(control_frame, text="Seleccionar tabla:")
table_label.grid(row=0, column=0, padx=10)

table_selector = ttk.Combobox(control_frame, values=['Todas', 'Oxigeno_Disuelto', 'pH', 'Conductividad', 'Temperatura'])
table_selector.current(0)
table_selector.grid(row=0, column=1, padx=10)

# Detectar anomalías
detect_button = Button(control_frame, text="Detectar Anomalías", command=detect_anomalies)
detect_button.grid(row=0, column=2, padx=10)

# Salida
output_frame = Frame(root)
output_frame.pack(pady=20)

# Texto de salida
text_output = Text(output_frame, width=200, height=30) 
text_output.pack(side=LEFT, fill=Y) 
scrollbar = Scrollbar(output_frame, command=text_output.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Configuración de la ventana final
text_output.config(yscrollcommand=scrollbar.set)
text_output.config(width=200, height=30)


root.mainloop()