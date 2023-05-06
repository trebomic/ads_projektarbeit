import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# Laden des Excel-Files in ein Pandas DataFrame
df = pd.read_excel('output_for_plot.xlsx')

# Entfernen von Zeilen mit NaN-Werten in der Spalte "number_of_rooms"
df = df.dropna(subset=['number_of_rooms'])

# Entfernen von Zeilen mit 'None' in der Spalte "number_of_rooms"
df = df[df['number_of_rooms'] != 'None']

# Konvertieren der Spalten "flat_size" und "flat_price_chf" in Float-Datentypen
df['flat_size'] = df['flat_size'].astype(float)
df['flat_price_chf'] = df['flat_price_chf'].astype(float)

# Berechnen des Preises pro Quadratmeter
df['price_per_sqm'] = df['flat_price_chf'] / df['flat_size']

# Aufteilen der Daten in Trainings- und Testdaten
train_dataset = df.sample(frac=0.8, random_state=0)
test_dataset = df.drop(train_dataset.index)

# Definieren der Eingabe-Features (Wohnungsgröße)
train_features = train_dataset[['flat_size']]
test_features = test_dataset[['flat_size']]

# Definieren der Ausgabe-Labels (Preis pro Quadratmeter)
train_labels = train_dataset[['price_per_sqm']]
test_labels = test_dataset[['price_per_sqm']]

# Definition des Modells
model = keras.Sequential([
    keras.layers.Dense(1, input_shape=[1])
])

# Kompilieren des Modells
model.compile(loss='mean_squared_error',
              optimizer=tf.keras.optimizers.Adam(0.1))

# Trainieren des Modells
history = model.fit(train_features, train_labels, epochs=100)

# Vorhersagen treffen
train_predictions = model.predict(train_features).flatten()
test_predictions = model.predict(test_features).flatten()

# Erstellen des Scatterplots für Wohnungsgröße und Preis pro Quadratmeter
plt.scatter(train_features, train_labels, label='Daten')
plt.scatter(train_features, train_predictions, color='green', label='Vorhersage')
plt.scatter(test_features, test_labels, color='red', label='Test-Daten')
plt.scatter(test_features, test_predictions, color='yellow', label='Vorhersage Test-Daten')
plt.xlabel('Wohnungsgrösse')
plt.ylabel('Preis pro Quadratmeter')
plt.legend()
plt.show()