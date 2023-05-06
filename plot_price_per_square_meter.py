import pandas as pd
import matplotlib.pyplot as plt

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

# Erstellen des Scatterplots für die Preis pro Quadratmeter
plt.scatter(df['flat_size'], df['price_per_sqm'])
plt.xlabel('Grösse der Wohnung (in m²)')
plt.ylabel('Preis pro Quadratmeter (in CHF/m²)')
plt.show()