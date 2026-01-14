import pandas as pd
import os

# === 1️⃣ Vytvoření PBI složky ===
pbi_folder = "PBI"
os.makedirs(pbi_folder, exist_ok=True)

# === 2️⃣ Cesty k souborům ===
datasets = {
    "restaurant-2-orders-wide.csv": "Takeout/Datasets/restaurant-2-orders-wide.csv",
    "london_weather_categorized.csv": "Weather/Datasets/london_weather_categorized.csv"
}

# === 2️⃣.1️⃣ Produkty/Ingredience ===
products_path = "Takeout/Datasets/Original/restaurant-2-products-price.csv"

# === 2️⃣.2️⃣ Propojovací tabulka (Order-Items) ===
order_items_path = "Takeout/Datasets/restaurant-2-orders-trimmed.csv"

# === 3️⃣ Funkce pro převod čísel s čárkou ===
def convert_decimals_to_comma(df):
    """Převede všechny float sloupce na string s čárkou místo tečky"""
    df_copy = df.copy()

    for col in df_copy.columns:
        if df_copy[col].dtype == 'float64':
            # Převod na string s čárkou místo tečky
            df_copy[col] = df_copy[col].apply(lambda x: str(x).replace('.', ',') if pd.notna(x) else '')
        elif df_copy[col].dtype == 'int64':
            # Zachovat integery jako jsou (Power BI je správně přečte)
            pass

    return df_copy

# === 4️⃣ Zpracování datasetů ===
for output_name, input_path in datasets.items():
    print(f"\n📂 Zpracovávám: {input_path}")

    # Načtení
    df = pd.read_csv(input_path)
    print(f"   ✅ Načteno: {len(df)} řádků, {len(df.columns)} sloupců")

    # Speciální zpracování pro orders dataset - odstranit sloupce produktů
    if output_name == "restaurant-2-orders-wide.csv":
        metric_columns = [
            'Order ID', 'Date', 'Time', 'Total products',
            'Total Price', 'Average Item Price', 'Median Item Price',
            'Cheapest Item Price', 'Most Expensive Item Price',
            'Average Item Quantity', 'Max Item Quantity', 'Min Item Quantity'
        ]
        # Ponechat pouze metriky
        df = df[metric_columns]
        print(f"   🔧 Odstraněny sloupce produktů, ponechány pouze metriky: {len(df.columns)} sloupců")

    # Převod desetinných čísel
    df_converted = convert_decimals_to_comma(df)

    # Uložení do PBI složky
    output_path = os.path.join(pbi_folder, output_name)
    df_converted.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"   💾 Uloženo do: {output_path}")

# === 4️⃣.1️⃣ Zpracování produktů/ingrediencí ===
print(f"\n📂 Zpracovávám: {products_path}")

# Načtení produktů
products_df = pd.read_csv(products_path)
print(f"   ✅ Načteno: {len(products_df)} produktů")

# Převod cen s čárkou
products_df['Product Price'] = products_df['Product Price'].apply(
    lambda x: str(x).replace('.', ',') if pd.notna(x) else ''
)

# Přidání ID sloupce pro Power BI vztahy
products_df.insert(0, 'Product ID', list(range(1, len(products_df) + 1)))

# Uložení
products_output = os.path.join(pbi_folder, "products.csv")
products_df.to_csv(products_output, index=False, encoding='utf-8-sig')
print(f"   💾 Uloženo do: {products_output}")

# === 4️⃣.2️⃣ Zpracování Order-Items propojovací tabulky ===
print(f"\n📂 Zpracovávám: {order_items_path}")

# Načtení order-items
order_items_df = pd.read_csv(order_items_path)
print(f"   ✅ Načteno: {len(order_items_df)} řádků")

# Přidání Product ID pro propojení s products tabulkou
# Vytvoření mapování Item Name -> Product ID
product_id_map = dict(zip(products_df['Item Name'], products_df['Product ID']))
order_items_df['Product ID'] = order_items_df['Item Name'].map(product_id_map)

# Kontrola chybějících mapování
missing_products = order_items_df[order_items_df['Product ID'].isna()]['Item Name'].unique()
if len(missing_products) > 0:
    print(f"   ⚠️  Varování: {len(missing_products)} produktů nemá Product ID v ceníku")
    # Odstranit řádky s chybějícími produkty
    order_items_df = order_items_df.dropna(subset=['Product ID'])

# Převod Product ID na integer
order_items_df['Product ID'] = order_items_df['Product ID'].astype(int)

# Výběr pouze potřebných sloupců pro propojovací tabulku
order_items_df = order_items_df[['Order ID', 'Product ID', 'Item Name', 'Quantity', 'Product Price']]

# Převod číselných hodnot s čárkou
order_items_df['Product Price'] = order_items_df['Product Price'].apply(
    lambda x: str(x).replace('.', ',') if pd.notna(x) else ''
)

# Uložení
order_items_output = os.path.join(pbi_folder, "order-items.csv")
order_items_df.to_csv(order_items_output, index=False, encoding='utf-8-sig')
print(f"   💾 Uloženo do: {order_items_output}")

# === 5️⃣ Shrnutí ===
print("\n" + "="*60)
print("✅ HOTOVO! Datasety připraveny pro Power BI")
print("="*60)
print(f"📁 Složka: {os.path.abspath(pbi_folder)}")
print(f"📊 Počet souborů: {len(datasets) + 2}")
print("\n📋 Soubory:")
for filename in datasets.keys():
    print(f"   • {filename}")
print(f"   • products.csv ({len(products_df)} produktů)")
print(f"   • order-items.csv ({len(order_items_df)} záznamů)")
print("\n💡 Poznámka: Všechna desetinná čísla používají ČÁRKU (,) místo tečky (.)")
print("\n🔗 Vztahy v Power BI:")
print("   1. restaurant-2-orders-wide.csv [Order ID] ↔ order-items.csv [Order ID]")
print("   2. order-items.csv [Product ID] ↔ products.csv [Product ID]")
print("   3. restaurant-2-orders-wide.csv [Date] ↔ london_weather_categorized.csv [Date]")

