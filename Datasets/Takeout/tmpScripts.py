import pandas as pd

# Cesta k datasetu
file_path = "Datasets/restaurant-2-orders-wide.csv"

# Načtení CSV
df = pd.read_csv(file_path)

# Zkontrolujeme názvy sloupců
print(f"🧾 Columns: {list(df.columns)}")

# Ověříme, že máme správný název sloupce pro datum
date_column = None
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower() or "order" in col.lower():
        print(f"✅ Possible date column: {col}")
    if col.lower() in ["date", "order date", "order_date"]:
        date_column = col

# Pokud je třeba, ručně specifikuj správný sloupec
if date_column is None:
    date_column = "Order Date"  # přizpůsob podle skutečného názvu

# Převod na datetime
df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

# Získání rozsahu dat
min_date = df[date_column].min()
max_date = df[date_column].max()

print("\n📅 --- Date Range in Takeout Dataset ---")
print(f"🟢 Earliest date : {min_date.date()}")
print(f"🔴 Latest date   : {max_date.date()}")

# Volitelně: počet unikátních dní
unique_days = df[date_column].dt.date.nunique()
print(f"📊 Unique order days: {unique_days}")
