import pandas as pd
import matplotlib.pyplot as plt

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

# Erstellen des Scatterplots für die Preis pro Zimmer
plt.scatter(df['number_of_rooms'], df['price_per_room'])
plt.xlabel('Anzahl Zimmer')
plt.ylabel('Preis pro Zimmer (in CHF)')
plt.show()