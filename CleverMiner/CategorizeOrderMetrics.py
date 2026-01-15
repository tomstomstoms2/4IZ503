import pandas as pd
import numpy as np

print("="*70)
print("⚠️  TENTO SKRIPT JE DEPRECATED!")
print("="*70)
print("\n❌ Tento skript již není používán.")
print("✅ Použijte místo něj: CreateAnalyzedDataset.py")
print("\n📋 CreateAnalyzedDataset.py:")
print("   - Vytváří nový 'datasetAnalyzed.csv'")
print("   - Ponechává 'datasetMerged.csv' v původním stavu")
print("   - Odstraňuje redundantní číselné weather sloupce")
print("\n" + "="*70)
print("\nPokračování pro zpětnou kompatibilitu...\n")
print("="*70)
print("📊 KATEGORIZACE ORDER METRIK PRO CLEVERMINER")
print("="*70)

# === Načtení dat ===
df = pd.read_csv('datasetMerged.csv')
print(f"\n✅ Načteno: {len(df):,} řádků")

# ============================================================================
# 1️⃣ TOTAL PRICE KATEGORIZACE (celková cena objednávky)
# ============================================================================
print("\n🔹 Total Price kategorizace...")

def categorize_total_price(price):
    """
    Kategorizace celkové ceny objednávky
    Založeno na percentilech a business logice
    """
    if pd.isna(price):
        return 'unknown'
    elif price < 20:
        return 'very low'      # Bottom 15% - levné objednávky
    elif price < 25:
        return 'low'           # 15-30%
    elif price < 32:
        return 'medium-low'    # 30-50%
    elif price < 40:
        return 'medium'        # 50-70% - kolem mediánu
    elif price < 50:
        return 'medium-high'   # 70-85%
    elif price < 65:
        return 'high'          # 85-95%
    else:
        return 'very high'     # Top 5% - drahé objednávky

df['Total_Price_cat'] = df['Total Price'].apply(categorize_total_price)

# Kontrola distribuce
print("  Distribuce:")
for cat in ['very low', 'low', 'medium-low', 'medium', 'medium-high', 'high', 'very high']:
    count = (df['Total_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 2️⃣ AVERAGE ITEM PRICE KATEGORIZACE (průměrná cena položky)
# ============================================================================
print("\n🔹 Average Item Price kategorizace...")

def categorize_avg_item_price(price):
    """
    Kategorizace průměrné ceny položky v objednávce
    """
    if pd.isna(price):
        return 'unknown'
    elif price < 4.5:
        return 'budget'        # Levné položky (< 4.5£)
    elif price < 5.5:
        return 'economy'       # Ekonomické (4.5-5.5£)
    elif price < 6.5:
        return 'standard'      # Standardní (5.5-6.5£) - kolem mediánu
    elif price < 8:
        return 'premium'       # Prémiové (6.5-8£)
    else:
        return 'luxury'        # Luxusní (> 8£)

df['Avg_Item_Price_cat'] = df['Average Item Price'].apply(categorize_avg_item_price)

# Kontrola distribuce
print("  Distribuce:")
for cat in ['budget', 'economy', 'standard', 'premium', 'luxury']:
    count = (df['Avg_Item_Price_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 3️⃣ TOTAL PRODUCTS KATEGORIZACE (počet položek v objednávce)
# ============================================================================
print("\n🔹 Total products kategorizace...")

def categorize_total_products(count):
    """
    Kategorizace počtu položek v objednávce
    """
    if pd.isna(count):
        return 'unknown'
    elif count <= 2:
        return 'tiny'          # 1-2 položky - velmi malá objednávka
    elif count <= 4:
        return 'small'         # 3-4 položky - malá objednávka
    elif count <= 6:
        return 'medium'        # 5-6 položek - střední (kolem mediánu)
    elif count <= 8:
        return 'large'         # 7-8 položek - velká
    elif count <= 11:
        return 'very large'    # 9-11 položek - velmi velká
    else:
        return 'huge'          # 12+ položek - obrovská objednávka

df['Total_Products_cat'] = df['Total products'].apply(categorize_total_products)

# Kontrola distribuce
print("  Distribuce:")
for cat in ['tiny', 'small', 'medium', 'large', 'very large', 'huge']:
    count = (df['Total_Products_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 4️⃣ AVERAGE ITEM QUANTITY KATEGORIZACE (průměrné množství na položku)
# ============================================================================
print("\n🔹 Average Item Quantity kategorizace...")

def categorize_avg_quantity(qty):
    """
    Kategorizace průměrného množství na položku
    Většina objednávek má 1.0-1.5, takže jemnější rozdělení
    """
    if pd.isna(qty):
        return 'unknown'
    elif qty == 1.0:
        return 'single'        # Přesně 1 kus každé položky
    elif qty < 1.3:
        return 'mostly single' # Většinou 1, někdy 2
    elif qty < 1.6:
        return 'mixed'         # Mix 1 a 2 kusy
    elif qty < 2.0:
        return 'mostly double' # Většinou 2 kusy
    else:
        return 'bulk'          # 2+ kusy v průměru - nákup většího množství

df['Avg_Item_Quantity_cat'] = df['Average Item Quantity'].apply(categorize_avg_quantity)

# Kontrola distribuce
print("  Distribuce:")
for cat in ['single', 'mostly single', 'mixed', 'mostly double', 'bulk']:
    count = (df['Avg_Item_Quantity_cat'] == cat).sum()
    pct = count / len(df) * 100
    print(f"    {cat:15s}: {count:5,} ({pct:5.1f}%)")

# ============================================================================
# 💾 ULOŽENÍ
# ============================================================================
print("\n" + "="*70)
print("💾 Ukládám kategorizovaný dataset...")

output_path = 'datasetMerged.csv'
df.to_csv(output_path, index=False)

print(f"✅ Uloženo do: {output_path}")

# ============================================================================
# 📊 SHRNUTÍ
# ============================================================================
print("\n" + "="*70)
print("📊 PŘIDANÉ KATEGORIZOVANÉ SLOUPCE:")
print("="*70)

new_columns = [
    'Total_Price_cat',
    'Avg_Item_Price_cat',
    'Total_Products_cat',
    'Avg_Item_Quantity_cat'
]

for col in new_columns:
    unique_vals = df[col].unique()
    print(f"\n🔹 {col}:")
    print(f"   Kategorie: {list(unique_vals)}")
    print(f"   Počet kategorií: {len(unique_vals)}")

print("\n" + "="*70)
print("✅ HOTOVO!")
print("="*70)
print("\n📋 Návod pro CleverMiner:")
print("   - Použijte sloupce končící '_cat' pro analýzu")
print("   - Např: 'Total_Price_cat', 'Avg_Item_Price_cat', atd.")
print("   - Všechny kategorie jsou vybalancované pro lepší analýzu")
print("\n" + "="*70)

# ============================================================================
# 📈 UKÁZKA DAT
# ============================================================================
print("\n📝 Ukázka kategorizovaných dat (prvních 10 řádků):")
print("-"*70)

display_cols = [
    'Order ID', 'Total Price', 'Total_Price_cat',
    'Average Item Price', 'Avg_Item_Price_cat',
    'Total products', 'Total_Products_cat'
]

print(df[display_cols].head(10).to_string(index=False))
print("\n" + "="*70)

