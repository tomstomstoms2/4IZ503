import pandas as pd

# === 1️⃣ Načtení dat ===
df = pd.read_csv("Datasets/Original/restaurant-2-orders.csv")

# === 2️⃣ Parsování datumu ===
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y %H:%M', errors='coerce')
df = df.dropna(subset=['Order Date'])

# === 3️⃣ Rozdělení Order Date na Date a Time ===
df['Date'] = df['Order Date'].dt.date
df['Time'] = df['Order Date'].dt.time

# === 4️⃣ Zrušení původního Order Date ===
df = df.drop(columns=['Order Date'])

# === 5️⃣ Oříznutí po posledním výpadku (od 25. července 2016 dál) ===
cutoff_date = pd.Timestamp("2016-07-25")
df = df[df['Date'] >= cutoff_date.date()].copy()

# === 6️⃣ Výpočet pokrytí ===
first_date = df['Date'].min()
last_date = df['Date'].max()

full_range = pd.date_range(start=first_date, end=last_date).date
existing_days = set(df['Date'])
missing_days = sorted(set(full_range) - existing_days)

# === 7️⃣ Výpis výsledků ===
print("📅 První datum:", first_date)
print("📅 Poslední datum:", last_date)
print(f"📊 Počet dní s daty: {len(existing_days)} z {len(full_range)} ({len(existing_days)/len(full_range)*100:.1f} %)")

if missing_days:
    print("\n❌ Chybějící dny:")
    for d in missing_days:
        print(" -", d)
else:
    print("\n✅ Žádné chybějící dny – pokrytí je kompletní.")

# === 8️⃣ Uložení očištěného datasetu ===
df.to_csv("Datasets/restaurant-2-orders-trimmed.csv", index=False)
print("\n💾 Dataset uložen jako restaurant-2-orders-trimmed.csv")
