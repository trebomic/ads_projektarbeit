import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

# Laden des Excel-Files in ein Pandas DataFrame
df = pd.read_excel('output_for_plot.xlsx')

# Entfernen von Zeilen mit NaN-Werten in der Spalte "number_of_rooms"
df = df.dropna(subset=['number_of_rooms'])

# Entfernen von Zeilen mit 'None' in der Spalte "number_of_rooms"
df = df[df['number_of_rooms'] != 'None']

# Konvertieren der Spalten "number_of_rooms" und "flat_price_chf" in Float-Datentypen
df['number_of_rooms'] = df['number_of_rooms'].astype(float)
df['flat_price_chf'] = df['flat_price_chf'].astype(float)

# Berechnen des Preises pro Zimmer
df['price_per_room'] = df['flat_price_chf'] / df['number_of_rooms']

# Aufteilung in Trainings- und Testdaten
train_df = df.sample(frac=0.8, random_state=42)
test_df = df.drop(train_df.index)

# Extrahieren der Merkmale (Features) und Zielvariablen (Targets)
train_features = train_df[['number_of_rooms']].values
train_labels = train_df['price_per_room'].values
test_features = test_df[['number_of_rooms']].values
test_labels = test_df['price_per_room'].values

# Normalisieren der Features
train_mean = train_features.mean()
train_std = train_features.std()
train_features = (train_features - train_mean) / train_std
test_features = (test_features - train_mean) / train_std

# Definition des Modells
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(1)
])

# Kompilieren des Modells
model.compile(optimizer='adam', loss='mse')

# Training des Modells
history = model.fit(train_features, train_labels, epochs=100, verbose=0, validation_split=0.2)

# Vorhersagen für Trainings- und Testdaten
train_predictions = model.predict(train_features)
test_predictions = model.predict(test_features)

# Erstellen des Scatterplots für die Daten und Vorhersagen
plt.scatter(train_df['number_of_rooms'], train_df['price_per_room'], color='blue', label='Trainingsdaten')
plt.scatter(test_df['number_of_rooms'], test_df['price_per_room'], color='red', label='Testdaten')
plt.scatter(train_df['number_of_rooms'], train_predictions, color='green', label='Trainingsvorhersagen')
plt.scatter(test_df['number_of_rooms'], test_predictions, color='yellow', label='Testvorhersagen')
plt.xlabel('Anzahl Zimmer')
plt.ylabel('Preis pro Zimmer (in CHF)')
plt.legend()
plt.show()