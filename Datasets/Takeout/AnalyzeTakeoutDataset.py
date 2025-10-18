import pandas as pd
import math

# === 1️⃣ Načtení dat ===
df = pd.read_csv("Datasets/Original/restaurant-2-orders.csv")

# === 2️⃣ Nastavení formátu čísel ===
pd.options.display.float_format = '{:.5f}'.format

# === 3️⃣ Přehled ===
print(f"📊 Dataset obsahuje {len(df)} řádků a {len(df.columns)} sloupců.\n")

# === 4️⃣ Statistická analýza ===
summary = []
for col in df.columns:
    unique_count = df[col].nunique(dropna=True)
    missing_count = df[col].isna().sum()

    if pd.api.types.is_numeric_dtype(df[col]):
        col_min = round(df[col].min(), 1) if not math.isnan(df[col].min()) else None
        col_max = round(df[col].max(), 1) if not math.isnan(df[col].max()) else None
        col_avg = df[col].mean()
    else:
        col_min = col_max = col_avg = None

    # === Typ proměnné podle charakteru ===
    if col in ['Order Date']:
        col_type = "Časový"
    elif col in ['Order ID']:
        col_type = "Identifikátor"
    elif col in ['Item Name']:
        col_type = "Kategoriální"
    elif col in ['Quantity', 'Total products']:
        col_type = "Diskrétní"
    elif col in ['Product Price']:
        col_type = "Spojitý"
    else:
        col_type = ""

    summary.append({
        "Sloupec": col,
        "Typ": col_type,
        "Unikátní hodnoty": unique_count,
        "Chybějící hodnoty": missing_count,
        "Min": col_min,
        "Max": col_max,
        "Průměr": col_avg
    })

# === 5️⃣ Výstup ===
summary_df = pd.DataFrame(summary)
print(summary_df.to_string(index=False))
