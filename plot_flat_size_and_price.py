import pandas as pd
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

# Laden des Excel-Files in ein Pandas DataFrame
df = pd.read_excel('output_for_plot.xlsx')

# Entfernen von Zeilen mit NaN-Werten in der Spalte "number_of_rooms"
df = df.dropna(subset=['number_of_rooms'])

# Entfernen von Zeilen mit 'None' in der Spalte "number_of_rooms"
df = df[df['number_of_rooms'] != 'None']

# Konvertieren der Spalten "flat_size" und "flat_price_chf" in Float-Datentypen
df['flat_size'] = df['flat_size'].astype(float)
df['flat_price_chf'] = df['flat_price_chf'].astype(float)

# Aufteilen der Daten in Trainings- und Testdaten
train_data = df.sample(frac=0.8, random_state=0)
test_data = df.drop(train_data.index)

# Definition des Modells
model = keras.Sequential([
    keras.layers.Dense(units=1, input_shape=[1])
])

# Kompilieren des Modells
model.compile(optimizer=tf.optimizers.Adam(1), loss='mean_squared_error')

# Training des Modells
history = model.fit(train_data['flat_size'], train_data['flat_price_chf'], epochs=100)

# Evaluieren des Modells
test_loss = model.evaluate(test_data['flat_size'], test_data['flat_price_chf'])
print('Test Loss:', test_loss)

# Plotten der Ergebnisse
plt.scatter(df['flat_size'], df['flat_price_chf'])
plt.plot(df['flat_size'], model.predict(df['flat_size']), color='red')
plt.xlabel('Wohnfläche')
plt.ylabel('Preis')
plt.title('Preis vs Wohnfläche')
plt.show()