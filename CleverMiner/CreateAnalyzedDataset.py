import pandas as pd
import numpy as np

print("="*70)
print("VYTVORENI ANALYZED DATASETU PRO CLEVERMINER")
print("="*70)

# === Načtení dat ===
df = pd.read_csv('datasetMerged.csv')
print(f"\n[OK] Načteno: {len(df):,} řádků, {len(df.columns)} sloupců")

# ============================================================================
# 1️⃣ KATEGORIZACE ORDER METRIK
# ============================================================================
print("\n" + "="*70)
print("[#] KATEGORIZACE ORDER METRIK")
print("="*70)

# --- Total Price ---
print("\n[-] Total Price kategorizace...")

def categorize_total_price(price):
    """Kategorizace celkové ceny objednávky"""
    if pd.isna(price):
        return 'unknown'
    elif price < 20:
        return 'very low'
    elif price < 25:
        return 'low'
    elif price < 32:
        return 'medium-low'
    elif price < 40:
        return 'medium'
    elif price < 50:
        return 'medium-high'
    elif price < 65:
        return 'high'
    else:
        return 'very high'

df['Total_Price_cat'] = df['Total Price'].apply(categorize_total_price)

# Číselné mapování pro sekvence
total_price_map = {
    'very low': 1,
    'low': 2,
    'medium-low': 3,
    'medium': 4,
    'medium-high': 5,
    'high': 6,
    'very high': 7,
    'unknown': 0
}
df['Total_Price_cat_seq'] = df['Total_Price_cat'].map(total_price_map)

print("  Distribuce:")
for cat in ['very low', 'low', 'medium-low', 'medium', 'medium-high', 'high', 'very high']:
    count = (df['Total_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Average Item Price ---
print("\n[-] Average Item Price kategorizace...")

def categorize_avg_item_price(price):
    """Kategorizace průměrné ceny položky"""
    if pd.isna(price):
        return 'unknown'
    elif price < 4.5:
        return 'budget'
    elif price < 5.5:
        return 'economy'
    elif price < 6.5:
        return 'standard'
    elif price < 8:
        return 'premium'
    else:
        return 'luxury'

df['Avg_Item_Price_cat'] = df['Average Item Price'].apply(categorize_avg_item_price)

# Číselné mapování pro sekvence
avg_item_price_map = {
    'budget': 1,
    'economy': 2,
    'standard': 3,
    'premium': 4,
    'luxury': 5,
    'unknown': 0
}
df['Avg_Item_Price_cat_seq'] = df['Avg_Item_Price_cat'].map(avg_item_price_map)

print("  Distribuce:")
for cat in ['budget', 'economy', 'standard', 'premium', 'luxury']:
    count = (df['Avg_Item_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Total Products ---
print("\n[-] Total Products kategorizace...")

def categorize_total_products(count):
    """Kategorizace počtu položek"""
    if pd.isna(count):
        return 'unknown'
    elif count <= 2:
        return 'tiny'
    elif count <= 4:
        return 'small'
    elif count <= 6:
        return 'medium'
    elif count <= 8:
        return 'large'
    elif count <= 11:
        return 'very large'
    else:
        return 'huge'

df['Total_Products_cat'] = df['Total products'].apply(categorize_total_products)

# Číselné mapování pro sekvence
total_products_map = {
    'tiny': 1,
    'small': 2,
    'medium': 3,
    'large': 4,
    'very large': 5,
    'huge': 6,
    'unknown': 0
}
df['Total_Products_cat_seq'] = df['Total_Products_cat'].map(total_products_map)

print("  Distribuce:")
for cat in ['tiny', 'small', 'medium', 'large', 'very large', 'huge']:
    count = (df['Total_Products_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Average Item Quantity ---
print("\n[-] Average Item Quantity kategorizace...")

def categorize_avg_quantity(qty):
    """Kategorizace průměrného množství"""
    if pd.isna(qty):
        return 'unknown'
    elif qty == 1.0:
        return 'single'
    elif qty < 1.3:
        return 'mostly single'
    elif qty < 1.6:
        return 'mixed'
    elif qty < 2.0:
        return 'mostly double'
    else:
        return 'bulk'

df['Avg_Item_Quantity_cat'] = df['Average Item Quantity'].apply(categorize_avg_quantity)

# Číselné mapování pro sekvence
avg_item_quantity_map = {
    'single': 1,
    'mostly single': 2,
    'mixed': 3,
    'mostly double': 4,
    'bulk': 5,
    'unknown': 0
}
df['Avg_Item_Quantity_cat_seq'] = df['Avg_Item_Quantity_cat'].map(avg_item_quantity_map)

print("  Distribuce:")
for cat in ['single', 'mostly single', 'mixed', 'mostly double', 'bulk']:
    count = (df['Avg_Item_Quantity_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 2️⃣ ČÍSELNÉ SEKVENCE PRO WEATHER KATEGORIE
# ============================================================================
print("\n" + "="*70)
print("[*]  ČÍSELNÉ SEKVENCE PRO WEATHER KATEGORIE")
print("="*70)

# --- Cloud Cover ---
cloud_cover_map = {
    'clear': 1,
    'mostly clear': 2,
    'partly cloudy': 3,
    'mostly cloudy': 4,
    'overcast': 5,
    'sky obscured': 6,
    'unknown': 0
}
if 'cloud_cover_cat' in df.columns:
    df['cloud_cover_cat_seq'] = df['cloud_cover_cat'].map(cloud_cover_map)
    print("[OK] cloud_cover_cat_seq")

# --- Sunshine ---
sunshine_map = {
    'none': 1,
    'very short': 2,
    'short': 3,
    'moderate': 4,
    'long': 5,
    'very long': 6,
    'unknown': 0
}
if 'sunshine_cat' in df.columns:
    df['sunshine_cat_seq'] = df['sunshine_cat'].map(sunshine_map)
    print("[OK] sunshine_cat_seq")

# --- Global Radiation ---
global_radiation_map = {
    'very low': 1,
    'low': 2,
    'moderate': 3,
    'high': 4,
    'very high': 5,
    'extreme': 6,
    'unknown': 0
}
if 'global_radiation_cat' in df.columns:
    df['global_radiation_cat_seq'] = df['global_radiation_cat'].map(global_radiation_map)
    print("[OK] global_radiation_cat_seq")

# --- Mean Temperature ---
mean_temp_map = {
    'hard freezing': 1,
    'freezing': 2,
    'very cold': 3,
    'cold': 4,
    'fresh': 5,
    'warm': 6,
    'very warm': 7,
    'hot': 8,
    'unknown': 0
}
if 'mean_temp_cat' in df.columns:
    df['mean_temp_cat_seq'] = df['mean_temp_cat'].map(mean_temp_map)
    print("[OK] mean_temp_cat_seq")

# --- Precipitation ---
precipitation_map = {
    'no rain': 1,
    'very light': 2,
    'light': 3,
    'medium': 4,
    'strong': 5,
    'very strong': 6,
    'extremely strong': 7,
    'unknown': 0
}
if 'precipitation_cat' in df.columns:
    df['precipitation_cat_seq'] = df['precipitation_cat'].map(precipitation_map)
    print("[OK] precipitation_cat_seq")

# --- Snow Depth ---
snow_depth_map = {
    'none': 1,
    'trace': 2,
    'shallow': 3,
    'moderate': 4,
    'deep': 5,
    'very deep': 6,
    'unknown': 0
}
if 'snow_depth_cat' in df.columns:
    df['snow_depth_cat_seq'] = df['snow_depth_cat'].map(snow_depth_map)
    print("[OK] snow_depth_cat_seq")

# --- Pressure ---
pressure_map = {
    'extremely low': 1,
    'very low': 2,
    'low': 3,
    'normal': 4,
    'high': 5,
    'very high': 6,
    'extremely high': 7,
    'unknown': 0
}
if 'pressure_cat' in df.columns:
    df['pressure_cat_seq'] = df['pressure_cat'].map(pressure_map)
    print("[OK] pressure_cat_seq")

# ============================================================================
# 3️⃣ ODSTRANĚNÍ ZBYTEČNÝCH SLOUPCŮ
# ============================================================================
print("\n" + "="*70)
print("[X]  ODSTRANĚNÍ REDUNDANTNÍCH ČÍSELNÝCH SLOUPCŮ")
print("="*70)

# Sloupce k odstranění - mají kategorizované ekvivalenty
columns_to_remove = [
    # Weather sloupce (mají _cat verze)
    'cloud_cover',
    'sunshine',
    'global_radiation',
    'max_temp',
    'mean_temp',
    'min_temp',
    'precipitation',
    'snow_depth',
    'pressure',
    
    # Order metriky (ponecháme pro numerickou analýzu)
    # 'Total Price',  # PONECHÁME
    # 'Average Item Price',  # PONECHÁME
    # 'Total products',  # PONECHÁME
    # 'Average Item Quantity',  # PONECHÁME
]

# Najdeme sloupce, které skutečně existují
existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]

print(f"\n📋 Odstraňuji {len(existing_columns_to_remove)} sloupců:")
for col in existing_columns_to_remove:
    print(f"   [!] {col}")

df_analyzed = df.drop(columns=existing_columns_to_remove)

print(f"\n[OK] Původní: {len(df.columns)} sloupců")
print(f"[OK] Analyzed: {len(df_analyzed.columns)} sloupců")
print(f"[OK] Odstraněno: {len(existing_columns_to_remove)} sloupců")

# ============================================================================
# 4️⃣ ULOŽENÍ ANALYZED DATASETU
# ============================================================================
print("\n" + "="*70)
print("[S] UKLÁDÁNÍ DATASETŮ")
print("="*70)

output_analyzed = 'datasetAnalyzed.csv'
df_analyzed.to_csv(output_analyzed, index=False)
print(f"[OK] Analyzed dataset uložen: {output_analyzed}")
print(f"   [#] {len(df_analyzed):,} řádků × {len(df_analyzed.columns)} sloupců")

# ============================================================================
# 5️⃣ SHRNUTÍ KATEGORIZOVANÝCH SLOUPCŮ
# ============================================================================
print("\n" + "="*70)
print("[#] KATEGORIZOVANÉ SLOUPCE V ANALYZED DATASETU")
print("="*70)

categorized_cols = [col for col in df_analyzed.columns if '_cat' in col]
print(f"\n[OK] Celkem {len(categorized_cols)} kategorizovaných sloupců:\n")

# Order metriky
order_cats = ['Total_Price_cat', 'Avg_Item_Price_cat', 'Total_Products_cat', 'Avg_Item_Quantity_cat']
print("[$] ORDER METRIKY:")
for col in order_cats:
    if col in df_analyzed.columns:
        unique = df_analyzed[col].nunique()
        print(f"   • {col:30s} ({unique} kategorií)")

# Weather metriky
weather_cats = [col for col in categorized_cols if col not in order_cats]
print("\n[*]  WEATHER METRIKY:")
for col in sorted(weather_cats):
    unique = df_analyzed[col].nunique()
    print(f"   • {col:30s} ({unique} kategorií)")

# ============================================================================
# 6️⃣ UKÁZKA DAT
# ============================================================================
print("\n" + "="*70)
print("[!] UKÁZKA ANALYZED DATASETU (prvních 5 řádků)")
print("="*70)

display_cols = [
    'Order ID', 'Date', 'Day of Week',
    'Total Price', 'Total_Price_cat',
    'Average Item Price', 'Avg_Item_Price_cat',
    'Total products', 'Total_Products_cat',
    'mean_temp_cat', 'precipitation_cat'
]

# Zkontrolujeme, které sloupce existují
existing_display_cols = [col for col in display_cols if col in df_analyzed.columns]

print(df_analyzed[existing_display_cols].head(5).to_string(index=False))

# ============================================================================
# [OK] HOTOVO
# ============================================================================
print("\n" + "="*70)
print("[OK] ANALYZED DATASET VYTVOŘEN!")
print("="*70)
print("\n📋 Co dál:")
print("   1️⃣  Použijte 'datasetAnalyzed.csv' pro CleverMiner analýzu")
print("   2️⃣  Všechny kategorizované sloupce končí '_cat'")
print("   3️⃣  Původní číselné weather sloupce odstraněny")
print("   4️⃣  Order metriky ponechány v číselné i kategorizované formě")
print("\n" + "="*70)

