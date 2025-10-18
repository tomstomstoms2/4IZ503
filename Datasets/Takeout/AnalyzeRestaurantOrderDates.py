import pandas as pd

# Načtení CSV
df = pd.read_csv("Datasets/Original/restaurant-1-orders.csv")  # uprav název souboru podle potřeby

# Parsování datumu
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y %H:%M')

# Vytažení pouze data (bez času)
df['Date'] = df['Order Date'].dt.date

# Zjištění rozsahu dat
first_date = df['Date'].min()
last_date = df['Date'].max()

# Vytvoření úplného rozsahu dat
full_range = pd.date_range(start=first_date, end=last_date).date

# Nalezení chybějících dnů
existing_days = set(df['Date'])
missing_days = sorted(set(full_range) - existing_days)

print(f"📅 První datum: {first_date}")
print(f"📅 Poslední datum: {last_date}")
print(f"📊 Počet dní pokrytí: {len(existing_days)} z {len(full_range)}")
print()

if missing_days:
    print("❌ Chybějící dny:")
    for d in missing_days:
        print(" -", d)
else:
    print("✅ Žádné chybějící dny — pokrytí je kompletní.")


# Načtení CSV
df = pd.read_csv("Datasets/Original/restaurant-2-orders.csv")  # uprav název souboru podle potřeby

# Parsování datumu
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y %H:%M')

# Vytažení pouze data (bez času)
df['Date'] = df['Order Date'].dt.date

# Zjištění rozsahu dat
first_date = df['Date'].min()
last_date = df['Date'].max()

# Vytvoření úplného rozsahu dat
full_range = pd.date_range(start=first_date, end=last_date).date

# Nalezení chybějících dnů
existing_days = set(df['Date'])
missing_days = sorted(set(full_range) - existing_days)

print(f"📅 První datum: {first_date}")
print(f"📅 Poslední datum: {last_date}")
print(f"📊 Počet dní pokrytí: {len(existing_days)} z {len(full_range)}")
print()

if missing_days:
    print("❌ Chybějící dny:")
    for d in missing_days:
        print(" -", d)
else:
    print("✅ Žádné chybějící dny — pokrytí je kompletní.")
