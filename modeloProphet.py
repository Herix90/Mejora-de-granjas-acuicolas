import pandas as pd
from tkinter import *
from tkinter import ttk
from sklearn.ensemble import IsolationForest
from prophet import Prophet
from matplotlib import pyplot as plt


def forecast_values():
    global data
    
    selected_table = table_selector.get()
    if selected_table != 'Todas':

        # Preparar DATA
        df_prophet = data[['created_at', selected_table]].rename(columns={'created_at': 'ds', selected_table: 'y'})
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds']) 

        # Crear nodelo Prophet
        model = Prophet()
        model.fit(df_prophet)

        # Hacer Dataframe de predicciones
        future = model.make_future_dataframe(periods=2) # Dias objetivo

        # Forecast y Plot
        forecast = model.predict(future)
        fig = model.plot(forecast)
        plt.title(f'Predicción para {selected_table}')
        plt.subplots_adjust(top=0.9, bottom=0.2)
        plt.show()
    else:
        text_output.delete(1.0, END)
        text_output.insert(END, "Por favor, seleccione una variable específica para la predicción.")


# Botón para predicción
predict_button = Button(control_frame, text="Predecir Valores Futuros", command=forecast_values)
predict_button.grid(row=0, column=3, padx=10)

root.mainloop()