import pandas as pd
import numpy as np

print("="*70)
print("VYTVORENI DAILY COMPOUND DATASETU")
print("="*70)

# Načtení merged datasetu
df = pd.read_csv('datasetMerged.csv')
print(f"\n[OK] Načteno: {len(df):,} objednávek z {df['Date'].nunique()} dnů")

# ============================================================================
# AGREGACE DAT PO DNECH
# ============================================================================
print("\n" + "="*70)
print("[#] AGREGACE DAT PO DNECH")
print("="*70)

# Převod Date na datetime
df['Date'] = pd.to_datetime(df['Date'])

# Agregace podle data
print("\n[-] Agregace objednávek podle data...")
daily_data = df.groupby('Date').agg({
    # Časové údaje (použijeme první hodnotu, protože jsou stejné pro celý den)
    'Day of Week': 'first',
    'Day of Week Number': 'first',

    # Počasí (použijeme průměr pro číselné hodnoty)
    'cloud_cover': 'mean',
    'sunshine': 'mean',
    'global_radiation': 'mean',
    'max_temp': 'mean',
    'mean_temp': 'mean',
    'min_temp': 'mean',
    'precipitation': 'mean',
    'pressure': 'mean',
    'snow_depth': 'mean',

    # Kategorizované počasí (použijeme modus - nejčastější hodnotu)
    'cloud_cover_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'sunshine_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'global_radiation_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'mean_temp_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'precipitation_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'snow_depth_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
    'pressure_cat': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],

    # Metriky objednávek
    'Order ID': 'count',  # Počet objednávek
    'Total Price': 'sum'   # Celkové tržby
}).reset_index()

# Přejmenování sloupců
daily_data = daily_data.rename(columns={
    'Order ID': 'Orders_Count',
    'Total Price': 'Total_Revenue'
})

# Výpočet průměrných tržeb na objednávku
daily_data['Avg_Revenue_Per_Order'] = daily_data['Total_Revenue'] / daily_data['Orders_Count']

print(f"[OK] Vytvořeno {len(daily_data)} denních záznamů")

# ============================================================================
# VYTVORENI NUMERICKE VERZE KATEGORII PRO SEKVENCE
# ============================================================================
print("\n" + "="*70)
print("[#] VYTVORENI NUMERICKE VERZE KATEGORII")
print("="*70)

# Mapování kategorií na čísla (podle CreateAnalyzedDataset.py)
print("\n[-] Mapování kategorizovaných sloupců na číselné hodnoty...")

# Cloud cover
cloud_cover_map = {'clear': 1, 'partly cloudy': 2, 'mostly cloudy': 3, 'overcast': 4, 'unknown': 5}
daily_data['cloud_cover_cat_seq'] = daily_data['cloud_cover_cat'].map(cloud_cover_map)

# Sunshine
sunshine_map = {'none': 1, 'very short': 2, 'short': 3, 'moderate': 4, 'long': 5, 'very long': 6, 'unknown': 7}
daily_data['sunshine_cat_seq'] = daily_data['sunshine_cat'].map(sunshine_map)

# Global radiation
global_radiation_map = {'very low': 1, 'low': 2, 'moderate': 3, 'high': 4, 'very high': 5, 'unknown': 6}
daily_data['global_radiation_cat_seq'] = daily_data['global_radiation_cat'].map(global_radiation_map)

# Mean temperature
mean_temp_map = {'freezing': 1, 'very cold': 2, 'cold': 3, 'fresh': 4, 'warm': 5, 'very warm': 6, 'hot': 7, 'unknown': 8}
daily_data['mean_temp_cat_seq'] = daily_data['mean_temp_cat'].map(mean_temp_map)

# Precipitation
precipitation_map = {'no rain': 1, 'very light': 2, 'light': 3, 'medium': 4, 'strong': 5, 'very strong': 6, 'unknown': 7}
daily_data['precipitation_cat_seq'] = daily_data['precipitation_cat'].map(precipitation_map)

# Snow depth
snow_depth_map = {'none': 1, 'light': 2, 'moderate': 3, 'heavy': 4, 'very heavy': 5, 'unknown': 6}
daily_data['snow_depth_cat_seq'] = daily_data['snow_depth_cat'].map(snow_depth_map)

# Pressure
pressure_map = {'very low': 1, 'low': 2, 'moderate': 3, 'high': 4, 'very high': 5, 'extremely high': 6, 'unknown': 7}
daily_data['pressure_cat_seq'] = daily_data['pressure_cat'].map(pressure_map)

print("[OK] Číselné sekvence vytvořeny")

# ============================================================================
# KATEGORIZACE DENNICH METRIK
# ============================================================================
print("\n" + "="*70)
print("[#] KATEGORIZACE DENNICH METRIK")
print("="*70)

# Kategorizace počtu objednávek
print("\n[-] Kategorizace Orders_Count...")

def categorize_orders_count(count):
    """Kategorizace počtu objednávek za den - pomocí kvantilů"""
    if pd.isna(count):
        return 'unknown'
    elif count < 8:
        return 'very low'
    elif count < 13:
        return 'low'
    elif count < 20:
        return 'moderate'
    elif count < 31:
        return 'high'
    else:
        return 'very high'

daily_data['Orders_Count_cat'] = daily_data['Orders_Count'].apply(categorize_orders_count)

orders_count_map = {'very low': 1, 'low': 2, 'moderate': 3, 'high': 4, 'very high': 5, 'unknown': 6}
daily_data['Orders_Count_cat_seq'] = daily_data['Orders_Count_cat'].map(orders_count_map)

print(f"[OK] Orders_Count kategorie: {daily_data['Orders_Count_cat'].value_counts().to_dict()}")

# Kategorizace celkových tržeb
print("\n[-] Kategorizace Total_Revenue...")

def categorize_total_revenue(revenue):
    """Kategorizace celkových denních tržeb - pomocí kvantilů (optimalizováno)

    Kvantilové hranice optimalizované pro vyvážené rozdělení:
    - very low: 0-25% (£0-420)
    - low: 25-45% (£420-580)
    - moderate: 45-65% (£580-750)
    - high: 65-85% (£750-1100)
    - very high: 85-100% (£1100+)

    Poznámka: Data mají "long tail" distribuci, proto nejsou kvantily rovnoměrné po 20%.
    """
    if pd.isna(revenue):
        return 'unknown'
    elif revenue < 420:
        return 'very low'
    elif revenue < 580:
        return 'low'
    elif revenue < 750:
        return 'moderate'
    elif revenue < 1100:
        return 'high'
    else:
        return 'very high'

daily_data['Total_Revenue_cat'] = daily_data['Total_Revenue'].apply(categorize_total_revenue)

total_revenue_map = {'very low': 1, 'low': 2, 'moderate': 3, 'high': 4, 'very high': 5, 'unknown': 6}
daily_data['Total_Revenue_cat_seq'] = daily_data['Total_Revenue_cat'].map(total_revenue_map)

print(f"[OK] Total_Revenue kategorie: {daily_data['Total_Revenue_cat'].value_counts().to_dict()}")

# Kategorizace průměrných tržeb na objednávku
print("\n[-] Kategorizace Avg_Revenue_Per_Order...")

def categorize_avg_revenue(revenue):
    """Kategorizace průměrných tržeb na objednávku - pomocí kvantilů (20%)

    Kvantilové hranice pro vyvážené rozdělení:
    - very low: 0-20% (£0-30)
    - low: 20-40% (£30-33)
    - moderate: 40-60% (£33-35.5)
    - high: 60-80% (£35.5-38.5)
    - very high: 80-100% (£38.5+)
    """
    if pd.isna(revenue):
        return 'unknown'
    elif revenue < 30:
        return 'very low'
    elif revenue < 33:
        return 'low'
    elif revenue < 35.5:
        return 'moderate'
    elif revenue < 38.5:
        return 'high'
    else:
        return 'very high'

daily_data['Avg_Revenue_Per_Order_cat'] = daily_data['Avg_Revenue_Per_Order'].apply(categorize_avg_revenue)

avg_revenue_map = {'very low': 1, 'low': 2, 'moderate': 3, 'high': 4, 'very high': 5, 'unknown': 6}
daily_data['Avg_Revenue_Per_Order_cat_seq'] = daily_data['Avg_Revenue_Per_Order_cat'].map(avg_revenue_map)

print(f"[OK] Avg_Revenue_Per_Order kategorie: {daily_data['Avg_Revenue_Per_Order_cat'].value_counts().to_dict()}")

# ============================================================================
# SERAZENI SLOUPCU A ULOZENI
# ============================================================================
print("\n" + "="*70)
print("[#] ULOZENI DATASETU")
print("="*70)

# Výběr a seřazení sloupců
columns_order = [
    # Datum a den
    'Date', 'Day of Week', 'Day of Week Number',

    # Počasí - číselné hodnoty
    'cloud_cover', 'sunshine', 'global_radiation',
    'max_temp', 'mean_temp', 'min_temp',
    'precipitation', 'pressure', 'snow_depth',

    # Počasí - kategorické (slovní)
    'cloud_cover_cat', 'sunshine_cat', 'global_radiation_cat',
    'mean_temp_cat', 'precipitation_cat', 'snow_depth_cat', 'pressure_cat',

    # Počasí - kategorické (číselné pro sekvence)
    'cloud_cover_cat_seq', 'sunshine_cat_seq', 'global_radiation_cat_seq',
    'mean_temp_cat_seq', 'precipitation_cat_seq', 'snow_depth_cat_seq', 'pressure_cat_seq',

    # Metriky objednávek - číselné hodnoty
    'Orders_Count', 'Total_Revenue', 'Avg_Revenue_Per_Order',

    # Metriky objednávek - kategorické (slovní)
    'Orders_Count_cat', 'Total_Revenue_cat', 'Avg_Revenue_Per_Order_cat',

    # Metriky objednávek - kategorické (číselné pro sekvence)
    'Orders_Count_cat_seq', 'Total_Revenue_cat_seq', 'Avg_Revenue_Per_Order_cat_seq'
]

daily_data = daily_data[columns_order]

# Uložení
output_file = 'datasetDailyCompound.csv'
daily_data.to_csv(output_file, index=False)
print(f"\n[OK] Dataset uložen: {output_file}")
print(f"[OK] Celkem řádků: {len(daily_data)}")
print(f"[OK] Celkem sloupců: {len(daily_data.columns)}")

# ============================================================================
# STATISTIKY
# ============================================================================
print("\n" + "="*70)
print("[#] STATISTIKY DATASETU")
print("="*70)

print(f"\nDatum od: {daily_data['Date'].min()}")
print(f"Datum do: {daily_data['Date'].max()}")
print(f"Celkem dnů: {len(daily_data)}")

print(f"\nObjednávky:")
print(f"  Průměrně za den: {daily_data['Orders_Count'].mean():.1f}")
print(f"  Minimum za den: {daily_data['Orders_Count'].min()}")
print(f"  Maximum za den: {daily_data['Orders_Count'].max()}")

print(f"\nTržby:")
print(f"  Průměrné denní tržby: GBP{daily_data['Total_Revenue'].mean():.2f}")
print(f"  Minimální denní tržby: GBP{daily_data['Total_Revenue'].min():.2f}")
print(f"  Maximální denní tržby: GBP{daily_data['Total_Revenue'].max():.2f}")

print(f"\nPrůměrná tržba na objednávku:")
print(f"  Průměr: GBP{daily_data['Avg_Revenue_Per_Order'].mean():.2f}")
print(f"  Minimum: GBP{daily_data['Avg_Revenue_Per_Order'].min():.2f}")
print(f"  Maximum: GBP{daily_data['Avg_Revenue_Per_Order'].max():.2f}")

print("\n" + "="*70)
print("HOTOVO!")
print("="*70)

