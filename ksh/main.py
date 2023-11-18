import csv

# Ures tomb inicializalasa
data = []

# Fajl megnyitasa, encoding es delimiter beallitasa
with open('../csv/inflacio.csv', encoding='ISO-8859-1') as file:
    csvreader = csv.reader(file, delimiter=";")
    # Fejlec olvasasa
    header = next(csvreader)
    # Soronkent header-ertek map-be gyujtese
    for row in csvreader:
        row_data = {header[i]: row[i] for i in range(len(header))}
        print(row_data)
        data.append(row_data)

# Minden sor printelese
for item in data:
    print(item)
