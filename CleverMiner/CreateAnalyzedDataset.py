import pandas as pd
import numpy as np

print("="*70)
print("🔬 VYTVOŘENÍ ANALYZED DATASETU PRO CLEVERMINER")
print("="*70)

# === Načtení dat ===
df = pd.read_csv('datasetMerged.csv')
print(f"\n✅ Načteno: {len(df):,} řádků, {len(df.columns)} sloupců")

# ============================================================================
# 1️⃣ KATEGORIZACE ORDER METRIK
# ============================================================================
print("\n" + "="*70)
print("📊 KATEGORIZACE ORDER METRIK")
print("="*70)

# --- Total Price ---
print("\n🔹 Total Price kategorizace...")

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

print("  Distribuce:")
for cat in ['very low', 'low', 'medium-low', 'medium', 'medium-high', 'high', 'very high']:
    count = (df['Total_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Average Item Price ---
print("\n🔹 Average Item Price kategorizace...")

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

print("  Distribuce:")
for cat in ['budget', 'economy', 'standard', 'premium', 'luxury']:
    count = (df['Avg_Item_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Total Products ---
print("\n🔹 Total Products kategorizace...")

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

print("  Distribuce:")
for cat in ['tiny', 'small', 'medium', 'large', 'very large', 'huge']:
    count = (df['Total_Products_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# --- Average Item Quantity ---
print("\n🔹 Average Item Quantity kategorizace...")

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

print("  Distribuce:")
for cat in ['single', 'mostly single', 'mixed', 'mostly double', 'bulk']:
    count = (df['Avg_Item_Quantity_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 2️⃣ ODSTRANĚNÍ ZBYTEČNÝCH SLOUPCŮ
# ============================================================================
print("\n" + "="*70)
print("🗑️  ODSTRANĚNÍ REDUNDANTNÍCH ČÍSELNÝCH SLOUPCŮ")
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
    print(f"   ❌ {col}")

df_analyzed = df.drop(columns=existing_columns_to_remove)

print(f"\n✅ Původní: {len(df.columns)} sloupců")
print(f"✅ Analyzed: {len(df_analyzed.columns)} sloupců")
print(f"✅ Odstraněno: {len(existing_columns_to_remove)} sloupců")

# ============================================================================
# 3️⃣ ULOŽENÍ ANALYZED DATASETU
# ============================================================================
print("\n" + "="*70)
print("💾 UKLÁDÁNÍ DATASETŮ")
print("="*70)

output_analyzed = 'datasetAnalyzed.csv'
df_analyzed.to_csv(output_analyzed, index=False)
print(f"✅ Analyzed dataset uložen: {output_analyzed}")
print(f"   📊 {len(df_analyzed):,} řádků × {len(df_analyzed.columns)} sloupců")

# ============================================================================
# 4️⃣ SHRNUTÍ KATEGORIZOVANÝCH SLOUPCŮ
# ============================================================================
print("\n" + "="*70)
print("📊 KATEGORIZOVANÉ SLOUPCE V ANALYZED DATASETU")
print("="*70)

categorized_cols = [col for col in df_analyzed.columns if '_cat' in col]
print(f"\n✅ Celkem {len(categorized_cols)} kategorizovaných sloupců:\n")

# Order metriky
order_cats = ['Total_Price_cat', 'Avg_Item_Price_cat', 'Total_Products_cat', 'Avg_Item_Quantity_cat']
print("🛒 ORDER METRIKY:")
for col in order_cats:
    if col in df_analyzed.columns:
        unique = df_analyzed[col].nunique()
        print(f"   • {col:30s} ({unique} kategorií)")

# Weather metriky
weather_cats = [col for col in categorized_cols if col not in order_cats]
print("\n🌤️  WEATHER METRIKY:")
for col in sorted(weather_cats):
    unique = df_analyzed[col].nunique()
    print(f"   • {col:30s} ({unique} kategorií)")

# ============================================================================
# 5️⃣ UKÁZKA DAT
# ============================================================================
print("\n" + "="*70)
print("📝 UKÁZKA ANALYZED DATASETU (prvních 5 řádků)")
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
# ✅ HOTOVO
# ============================================================================
print("\n" + "="*70)
print("✅ ANALYZED DATASET VYTVOŘEN!")
print("="*70)
print("\n📋 Co dál:")
print("   1️⃣  Použijte 'datasetAnalyzed.csv' pro CleverMiner analýzu")
print("   2️⃣  Všechny kategorizované sloupce končí '_cat'")
print("   3️⃣  Původní číselné weather sloupce odstraněny")
print("   4️⃣  Order metriky ponechány v číselné i kategorizované formě")
print("\n" + "="*70)

