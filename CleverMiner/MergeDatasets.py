import pandas as pd
import os

print("=" * 60)
print("🔗 SPOJENÍ DATASETŮ - Orders & Weather")
print("=" * 60)

# === 1️⃣ Cesty k datům ===
orders_path = "../Datasets/Takeout/Datasets/restaurant-2-orders-wide.csv"
weather_path = "../Datasets/Weather/Datasets/london_weather_categorized.csv"
output_path = "datasetMerged.csv"

# === 2️⃣ Načtení datasetů ===
print("\n📂 Načítám datasety...")

orders = pd.read_csv(orders_path)
print(f"   ✅ Orders načteno: {len(orders)} objednávek, {len(orders.columns)} sloupců")

weather = pd.read_csv(weather_path)
print(f"   ✅ Weather načteno: {len(weather)} dní, {len(weather.columns)} sloupců")

# === 3️⃣ Kontrola formátu datumu ===
print("\n📅 Kontrola formátu datumu...")

# Převod Date na datetime pro zajištění kompatibility
orders['Date'] = pd.to_datetime(orders['Date'])
weather['Date'] = pd.to_datetime(weather['Date'])

print(f"   Orders - Date rozsah: {orders['Date'].min()} → {orders['Date'].max()}")
print(f"   Weather - Date rozsah: {weather['Date'].min()} → {weather['Date'].max()}")

# === 4️⃣ Spojení datasetů ===
print("\n🔗 Spojujem datasety přes Date (LEFT JOIN)...")

# LEFT JOIN - ponechat všechny objednávky, přidat počasí kde je k dispozici
merged = pd.merge(
    orders,
    weather,
    on='Date',
    how='left'
)

print(f"   ✅ Spojeno: {len(merged)} řádků, {len(merged.columns)} sloupců")

# === 5️⃣ Kontrola chybějících hodnot počasí ===
missing_weather = merged['mean_temp'].isna().sum()
if missing_weather > 0:
    print(f"   ⚠️  Varování: {missing_weather} objednávek bez dat o počasí")
    # Zobrazit dny bez počasí
    missing_dates = merged[merged['mean_temp'].isna()]['Date'].unique()
    print(f"   Chybějící dny: {len(missing_dates)}")
else:
    print(f"   ✅ Všechny objednávky mají data o počasí")

# === 6️⃣ Přehled sloučeného datasetu ===
print("\n📊 Přehled sloučeného datasetu:")
print(f"   • Celkem řádků: {len(merged):,}")
print(f"   • Celkem sloupců: {len(merged.columns)}")
print(f"   • Období: {merged['Date'].min()} → {merged['Date'].max()}")
print(f"   • Unikátní dny: {merged['Date'].nunique()}")

# === 7️⃣ Kategorizace sloupců ===
print("\n📋 Kategorie sloupců:")

# Orders sloupce
order_cols = [col for col in merged.columns if col in orders.columns and col != 'Date']
print(f"   • Order metriky: {len(order_cols)} sloupců")

# Weather sloupce
weather_cols = [col for col in merged.columns if col in weather.columns and col != 'Date']
print(f"   • Weather metriky: {len(weather_cols)} sloupců")

# Produkty (pokud jsou ve wide formátu)
product_cols = [col for col in merged.columns if col not in order_cols and col not in weather_cols and col != 'Date']
if product_cols:
    print(f"   • Produktové sloupce: {len(product_cols)} sloupců")

# === 8️⃣ Uložení ===
print(f"\n💾 Ukládám sloučený dataset do: {output_path}")

merged.to_csv(output_path, index=False)

print(f"   ✅ Uloženo!")

# === 9️⃣ Ukázka dat ===
print("\n📝 Ukázka prvních 5 řádků:")
print("-" * 60)

# Výběr klíčových sloupců pro zobrazení
display_cols = [
    'Order ID', 'Date', 'Day of Week', 'Time', 'Total products',
    'Total Price', 'mean_temp', 'precipitation', 'cloud_cover_cat'
]

# Filtrovat pouze existující sloupce
display_cols = [col for col in display_cols if col in merged.columns]

print(merged[display_cols].head().to_string(index=False))

# === 🔟 Statistiky ===
print("\n" + "=" * 60)
print("📈 ZÁKLADNÍ STATISTIKY")
print("=" * 60)

print(f"\n🛍️  OBJEDNÁVKY:")
print(f"   • Celkem objednávek: {len(merged):,}")
print(f"   • Průměrná hodnota: £{merged['Total Price'].mean():.2f}")
print(f"   • Průměrný počet položek: {merged['Total products'].mean():.1f}")

if 'mean_temp' in merged.columns:
    print(f"\n🌡️  POČASÍ:")
    print(f"   • Průměrná teplota: {merged['mean_temp'].mean():.1f}°C")
    print(f"   • Min teplota: {merged['mean_temp'].min():.1f}°C")
    print(f"   • Max teplota: {merged['mean_temp'].max():.1f}°C")

    if 'precipitation' in merged.columns:
        print(f"   • Průměrné srážky: {merged['precipitation'].mean():.1f} mm")
        rainy_days = (merged['precipitation'] > 0).sum()
        print(f"   • Dny se srážkami: {rainy_days} ({rainy_days/len(merged)*100:.1f}%)")

print("\n" + "=" * 60)
print("✅ HOTOVO!")
print("=" * 60)
print(f"\n📁 Sloučený dataset: {os.path.abspath(output_path)}")
print(f"📊 Velikost souboru: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

