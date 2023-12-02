import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import openpyxl
from openpyxl.workbook import Workbook
from sklearn.linear_model import LinearRegression


# Ures tomb inicializalasa, amiben a sorok adatait fogjuk kulcs-ertekben tarolni
data = []

# Fajl megnyitasa, encoding es delimiter beallitasa
with open('../csv/inflacio.csv', encoding='ISO-8859-1') as file:
    csvreader = csv.reader(file, delimiter=";")
    # Fejlec olvasasa
    header = next(csvreader)
    # Soronkent header-ertek map-be gyujtese
    for row in csvreader:
        row_data = {header[i]: row[i] for i in range(len(header))}
        data.append(row_data)

years = []
food_prices = []
total_values = []

for entry in data:
    year = int(entry['Év'])
    # Az ertekek atalakitasa float-ra, a tizedesvesszo helyettesitese ponttal
    price = float(entry['Élelmiszerek'].replace(',', '.'))
    value = float(entry['Összesen'].replace(',', '.'))
    years.append(year)
    food_prices.append(price)
    total_values.append(value)

# Az éves változások kiszámítása
price_changes = [food_prices[i + 1] - food_prices[i] for i in range(len(food_prices) - 1)]

# Eves valtozas az elelmiszerek araban vonal diagram
plt.figure(figsize=(10, 6))
# years[1:]: Mivel az elso ev elott nincs mihez viszonyitani, igy kiszedjuk a listabol
plt.plot(years[1:], price_changes, marker='o')
plt.title("Éves változás az élelmiszerek árában")
plt.xlabel("Év")
plt.ylabel("Árváltozás (százalékban)")
plt.grid(True)
plt.show()

# Az adott ev teljes inflaciojanak szazalekos megjelenitese
plt.figure(figsize=(10, 6))
plt.plot(years, total_values, marker='o', linestyle='None')
plt.title("Adott év teljes inflációs változása")
plt.xlabel("Év")
plt.ylabel("Érték (százalékban)")
plt.grid(True)
plt.show()

# Az openpyxl munkafüzet létrehozása
wb = Workbook()
ws = wb.active

# Adatok felvitele az Excel fájlba
# Először a fejléc
ws.append(header)

# Majd az adatok soronként
for entry in data:
    row = [entry[h] for h in header]
    ws.append(row)

# Excel fájl mentése
excel_filename = "../xls/inflacio.xlsx"
wb.save(excel_filename)

# Évek és élelmiszerárak (vagy összes infláció) konvertálása numpy tömbbé
x = np.array(total_values).reshape(-1, 1)
y = np.array(food_prices)  # Vagy y = np.array(total_values)

# Lineáris regresszió végrehajtása
slope, intercept, r_value, p_value, std_err = stats.linregress(x.squeeze(), y)

# Lineáris regressziós egyenes létrehozása
y_pred = intercept + slope * x.squeeze()

# Ábra megjelenítése
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue')  # Adatpontok
plt.plot(x, y_pred, color='red')  # Regressziós egyenes
plt.title("Lineáris regresszió az élelmiszerárakra vonatkozó és a teljes inflációs százalék között")
plt.xlabel("Teljes infláció (százalékban)")
plt.ylabel("Élelmiszerár (százalékban)")
plt.grid(True)
plt.show()
