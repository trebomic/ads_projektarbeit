import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

# Laden des Excel-Files in ein Pandas DataFrame
df = pd.read_excel('output_for_plot.xlsx')

# Filtern des DataFrames mit einem regulären Ausdruck für "addr_zip" als erste Ziffer eine 8 oder 9
df_8 = df[df['addr_zip'].astype(str).str.startswith('8')]
df_9 = df[df['addr_zip'].astype(str).str.startswith('9')]

# Extrahieren der Merkmale (Features) und Zielvariablen (Targets)
x_8 = df_8[['flat_size', 'number_of_rooms']].values
y_8 = df_8['flat_price_chf'].values
x_9 = df_9[['flat_size', 'number_of_rooms']].values
y_9 = df_9['flat_price_chf'].values

# Normalisieren der Features
x_8 = (x_8 - x_8.mean()) / x_8.std()
x_9 = (x_9 - x_9.mean()) / x_9.std()

# Definition des Modells
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(1)
])

# Kompilieren des Modells
model.compile(optimizer='adam', loss='mse')

# Training des Modells auf den Daten der PLZ mit 8 beginnend
model.fit(x_8, y_8, epochs=100, verbose=0)

# Vorhersagen für die Daten der PLZ mit 8 beginnend
y_8_pred = model.predict(x_8)

# Training des Modells auf den Daten der PLZ mit 9 beginnend
model.fit(x_9, y_9, epochs=100, verbose=0)

# Vorhersagen für die Daten der PLZ mit 9 beginnend
y_9_pred = model.predict(x_9)


# Erstellen des Scatterplots für die ursprünglichen Daten mit unterschiedlicher Farbe für jede Gruppe
plt.scatter(df_8['flat_size'], df_8['flat_price_chf'], color='blue', label='Zürich')
plt.scatter(df_9['flat_size'], df_9['flat_price_chf'], color='red', label='St. Gallen')

# Hinzufügen der Vorhersagepunkte als grüne Dreiecke
plt.scatter(df_8['flat_size'], y_8_pred, color='yellow', marker='^', label='Vorhersage Zürich')
plt.scatter(df_9['flat_size'], y_9_pred, color='green', marker='^', label='Vorhersage St. Gallen')

plt.xlabel('Wohnungsgrösse (in m²)')
plt.ylabel('Preis (in CHF)')
plt.legend()
plt.show()