import pandas as pd
from tkinter import *
from tkinter import ttk
from sklearn.ensemble import IsolationForest


def detect_anomalies():
    global data
    global anomalies_df
    
    # Lista de características
    features = ['Oxigeno_Disuelto', 'pH', 'Conductividad', 'Temperatura']
    
    selected_table = table_selector.get()
    
    if selected_table == 'Todas':
        anomalies_df = pd.DataFrame()
        for feature in features:
            # Seleccionar la característica actual
            X = data[[feature]]

            # Entrenar el modelo Isolation Forest
            model = IsolationForest(contamination=0.05)  # Contaminación esperada del 5%
            model.fit(X)

            # Detectar anomalías
            anomalies = model.predict(X)

            # Agregar la columna de anomalías al DataFrame original
            data[f'{feature}_Anomalia'] = anomalies

            # Filtrar las filas que son anomalías para esta característica y agregarlas al DataFrame de anomalías
            anomalies_df = pd.concat([anomalies_df, data[data[f'{feature}_Anomalia'] == -1]])

            if 'entry_id' in anomalies_df.columns:
                anomalies_df.drop(columns=['entry_id'], inplace=True)
    else:
        # Seleccionar la característica actual
        X = data[[selected_table]]

        # Entrenar el modelo Isolation Forest
        model = IsolationForest(contamination=0.05)  # Contaminación esperada del 5%
        model.fit(X)

        # Detectar anomalías
        anomalies = model.predict(X)

        # Agregar la columna de anomalías al DataFrame original
        data[f'{selected_table}_Anomalia'] = anomalies

        # Filtrar las filas que son anomalías
        anomalies_df = data[data[f'{selected_table}_Anomalia'] == -1]

    text_output.delete(1.0, END)
    pd.set_option('display.max_columns', None)
    text_output.insert(END, anomalies_df.to_string(index=False))

# Cargar los datos desde el archivo CSV
data = pd.read_csv('feeds.csv')
anomalies_df = pd.DataFrame()

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