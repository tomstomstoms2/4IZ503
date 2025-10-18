import pandas as pd

# === 1️⃣ Načtení dat ===
orders = pd.read_csv("Datasets/restaurant-2-orders-trimmed.csv")
products = pd.read_csv("Datasets/Original/restaurant-2-products-price.csv")

# === 2️⃣ Seznam všech produktů z ceníku ===
all_items = products['Item Name'].unique()

# === 3️⃣ Pivotování objednávek ===
pivot = (
    orders
    .groupby(['Order ID', 'Item Name'])['Quantity']
    .sum()
    .unstack(fill_value=0)
)

# === 4️⃣ Doplnění všech produktů z ceníku ===
for item in all_items:
    if item not in pivot.columns:
        pivot[item] = 0
pivot = pivot[all_items]

# === 5️⃣ Přidání metadat o objednávce ===
orders_meta = (
    orders.groupby('Order ID')
    .agg({
        'Date': 'first',
        'Time': 'first',
        'Total products': 'first'
    })
)

# === 6️⃣ Spojení dohromady ===
final = orders_meta.join(pivot, on='Order ID')

# === 7️⃣ Ceník jako slovník {Item Name: Product Price} ===
price_map = products.set_index('Item Name')['Product Price'].to_dict()

# === 8️⃣ Výpočet celkové a průměrné ceny ===
price_df = pivot.copy()
for col in price_df.columns:
    price_df[col] = price_df[col] * price_map.get(col, 0)

final['Total Price'] = price_df.sum(axis=1)
final['Average Item Price'] = final['Total Price'] / final['Total products']

# === 9️⃣ Nejlevnější a nejdražší položka ===
def price_range_for_order(row):
    ordered_items = row[row > 0].index
    if not len(ordered_items):
        return pd.Series([None, None])
    prices = [price_map.get(item, 0) for item in ordered_items]
    return pd.Series([min(prices), max(prices)])

final[['Cheapest Item Price', 'Most Expensive Item Price']] = pivot.apply(price_range_for_order, axis=1)

# === 🔟 Průměrné, max a min množství ===
def quantity_stats(row):
    quantities = row[row > 0].values
    if len(quantities) == 0:
        return pd.Series([0, 0, 0])
    return pd.Series([quantities.mean(), quantities.max(), quantities.min()])

final[['Average Item Quantity', 'Max Item Quantity', 'Min Item Quantity']] = pivot.apply(quantity_stats, axis=1)

# === 11️⃣ Přeskládání sloupců: metriky vpředu, itemy vzadu ===
metric_columns = [
    'Date', 'Time', 'Total products',
    'Total Price', 'Average Item Price',
    'Cheapest Item Price', 'Most Expensive Item Price',
    'Average Item Quantity', 'Max Item Quantity', 'Min Item Quantity'
]
final = final[metric_columns + list(all_items)]

# === 12️⃣ Uložení ===
final.reset_index().to_csv("Datasets/restaurant-2-orders-wide.csv", index=False)
print("💾 Soubor uložen jako Datasets/restaurant-2-orders-wide.csv")

# === 13️⃣ Shrnutí ===
print(f"📊 Počet objednávek: {len(final)}")
print(f"📦 Počet produktových sloupců: {len(all_items)}")
print("📑 Pořadí sloupců: metriky → itemy")
