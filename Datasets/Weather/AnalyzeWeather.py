import pandas as pd
import numpy as np

# === Načtení dat ===
df = pd.read_csv("Datasets/Original/london_weather.csv")

# === Definice typů proměnných ===
column_types = {
    "date": "časový",
    "cloud_cover": "kategoriální",
    "sunshine": "spojitý",
    "global_radiation": "spojitý",
    "max_temp": "spojitý",
    "mean_temp": "spojitý",
    "min_temp": "spojitý",
    "precipitation": "spojitý",
    "pressure": "spojitý",
    "snow_depth": "spojitý"
}

# === Funkce pro výpočet metrik ===
def column_summary(col):
    data = df[col].dropna()
    summary = {
        "Typ": column_types.get(col, ""),
        "Unikátní hodnoty": data.nunique(),
        "Chybějící hodnoty": df[col].isna().sum(),
    }

    # Pro číselné sloupce vypočítáme základní statistiky
    if np.issubdtype(df[col].dtype, np.number):
        summary["Min"] = round(data.min(), 1) if not data.empty else np.nan
        summary["Max"] = round(data.max(), 1) if not data.empty else np.nan
        summary["Průměr"] = round(data.mean(), 1) if not data.empty else np.nan
        summary["Medián"] = round(data.median(), 1) if not data.empty else np.nan
        summary["Modus"] = round(data.mode().iloc[0], 1) if not data.mode().empty else np.nan
    else:
        summary["Min"] = summary["Max"] = summary["Průměr"] = summary["Medián"] = summary["Modus"] = np.nan

    return summary

# === Sestavení tabulky ===
summary_df = pd.DataFrame([column_summary(col) for col in df.columns], index=df.columns)

# === Výpis ===
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 2000)
print("\n=== Přehledová analýza datasetu london_weather.csv ===\n")
print(summary_df)
