import pandas as pd
import matplotlib.pyplot as plt

# Laden des Excel-Files in ein Pandas DataFrame
df = pd.read_excel('output_for_plot.xlsx')

# Filtern des DataFrames mit einem regulären Ausdruck für "addr_zip" als erste Ziffer eine 8 oder 9
df_8 = df[df['addr_zip'].astype(str).str.startswith('8')]
df_9 = df[df['addr_zip'].astype(str).str.startswith('9')]

# Erstellen des Scatterplots für flat_size und flat_price_chf mit unterschiedlicher Farbe für jede Gruppe
plt.scatter(df_8['flat_size'], df_8['flat_price_chf'], color='blue', label='Zürich')
plt.scatter(df_9['flat_size'], df_9['flat_price_chf'], color='red', label='St. Gallen')
plt.xlabel('Wohnungsgrösse (in m²)')
plt.ylabel('Preis (in CHF)')
plt.legend()
plt.show()