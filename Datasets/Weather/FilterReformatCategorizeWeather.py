import pandas as pd

# === Paths ===
input_path = "Datasets/Original/london_weather.csv"
output_path = "Datasets/london_weather_categorized.csv"

# === Load dataset ===
df = pd.read_csv(input_path)

# === Convert 'date' to datetime and rename ===
df["Date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d")

# === Filter time period (same as restaurant-2-orders) ===
start_date = "2016-07-26"
end_date = "2019-08-3"
df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# === Fill missing values ===
df["cloud_cover"].fillna(7, inplace=True)           # modus
df["global_radiation"].fillna(95.0, inplace=True)   # median
df["max_temp"].fillna(15.0, inplace=True)           # median
df["mean_temp"].fillna(11.4, inplace=True)          # median
df["min_temp"].fillna(7.8, inplace=True)            # median
df["precipitation"].fillna(0.0, inplace=True)       # majority = 0
df["pressure"].fillna(101620.0, inplace=True)       # median
df["snow_depth"].fillna(0.0, inplace=True)          # majority = 0

# === Categorization functions ===

def categorize_cloud_cover(c):
    if pd.isna(c):
        return 'unknown'
    elif c == 0:
        return 'clear'
    elif c <= 2:
        return 'mostly clear'
    elif c <= 4:
        return 'partly cloudy'
    elif c <= 6:
        return 'mostly cloudy'
    elif c <= 8:
        return 'overcast'
    elif c == 9:
        return 'sky obscured'
    else:
        return 'unknown'

def categorize_sunshine(s):
    if pd.isna(s):
        return 'unknown'
    elif s == 0:
        return 'none'
    elif s <= 2:
        return 'very short'
    elif s <= 4:
        return 'short'
    elif s <= 6:
        return 'moderate'
    elif s <= 8:
        return 'long'
    else:
        return 'very long'

def categorize_global_radiation(r):
    if pd.isna(r):
        return 'unknown'
    elif r <= 50:
        return 'very low'
    elif r <= 100:
        return 'low'
    elif r <= 150:
        return 'moderate'
    elif r <= 250:
        return 'high'
    elif r <= 400:
        return 'very high'
    else:
        return 'extreme'

def categorize_mean_temp(t):
    if pd.isna(t):
        return 'unknown'
    elif t < -5:
        return 'hard freezing'
    elif t < 0:
        return 'freezing'
    elif t < 5:
        return 'very cold'
    elif t < 10:
        return 'cold'
    elif t < 15:
        return 'fresh'
    elif t < 20:
        return 'warm'
    elif t < 25:
        return 'very warm'
    else:
        return 'hot'

def categorize_precipitation(p):
    if pd.isna(p):
        return 'unknown'
    elif p == 0.0:
        return 'no rain'
    elif p < 1.0:
        return 'very light'
    elif p <= 10.0:
        return 'light'
    elif p <= 30.0:
        return 'medium'
    elif p <= 70.0:
        return 'strong'
    elif p <= 150.0:
        return 'very strong'
    else:
        return 'extremely strong'

def categorize_snow_depth(s):
    if pd.isna(s):
        return 'unknown'
    elif s == 0:
        return 'none'
    elif s <= 2:
        return 'trace'
    elif s <= 5:
        return 'shallow'
    elif s <= 10:
        return 'moderate'
    elif s <= 20:
        return 'deep'
    else:
        return 'very deep'

def categorize_pressure(p):
    if pd.isna(p):
        return 'unknown'
    p_hpa = p / 100.0
    if p_hpa < 995:
        return 'extremely low'
    elif p_hpa < 1000:
        return 'very low'
    elif p_hpa < 1005:
        return 'low'
    elif p_hpa < 1010:
        return 'normal'
    elif p_hpa < 1015:
        return 'high'
    elif p_hpa < 1020:
        return 'very high'
    else:
        return 'extremely high'

# === Apply categorizations ===
df["cloud_cover_cat"] = df["cloud_cover"].apply(categorize_cloud_cover)
df["sunshine_cat"] = df["sunshine"].apply(categorize_sunshine)
df["global_radiation_cat"] = df["global_radiation"].apply(categorize_global_radiation)
df["mean_temp_cat"] = df["mean_temp"].apply(categorize_mean_temp)
df["precipitation_cat"] = df["precipitation"].apply(categorize_precipitation)
df["snow_depth_cat"] = df["snow_depth"].apply(categorize_snow_depth)
df["pressure_cat"] = df["pressure"].apply(categorize_pressure)

# === Drop old 'date' column and reorder ===
df.drop(columns=["date"], inplace=True)
cols = ["Date"] + [c for c in df.columns if c != "Date"]
df = df[cols]

# === Save new dataset ===
df.to_csv(output_path, index=False, date_format="%Y-%m-%d")

print(f"✅ Categorized dataset saved to: {output_path}")
print(f"📆 Included date range: {start_date} → {end_date}")
print(f"📊 Total records: {len(df)}")
