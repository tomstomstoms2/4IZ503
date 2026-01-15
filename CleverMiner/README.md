# 🔬 CleverMiner Analýza

Tato složka obsahuje skripty a datasety pro analýzu v CleverMiner.

## 📁 Datasety

### `datasetMerged.csv`
**Spojený dataset** - výsledek `MergeDatasets.py` (merge weather a order dat).

- ✅ **Obsahuje:**
  - Weather kategorie (cloud_cover_cat, sunshine_cat, mean_temp_cat, precipitation_cat, atd.)
  - Číselné weather metriky (cloud_cover, sunshine, mean_temp, precipitation, pressure, atd.)
  - Číselné order metriky (Total Price, Average Item Price, Total products, atd.)
  - Produkty (všechny produktové sloupce)
- ❌ **Neobsahuje:** Order metriky kategorie
- 📊 **Rozměry:** ~19,311 řádků × ~335 sloupců
- 🎯 **Použití:** Základ pro vytvoření analyzed datasetu

### `datasetAnalyzed.csv`
**Optimalizovaný dataset pro CleverMiner** - doporučený pro analýzu!

- ✅ **Obsahuje:**
  - Weather kategorie (cloud_cover_cat, sunshine_cat, mean_temp_cat, precipitation_cat, atd.)
  - Weather číselné sekvence (*_cat_seq pro ordinální analýzu)
  - Order kategorie (Total_Price_cat, Avg_Item_Price_cat, Total_Products_cat, Avg_Item_Quantity_cat)
  - Order číselné sekvence (*_cat_seq pro ordinální analýzu)
  - Číselné order metriky (Total Price, Average Item Price, Total products, atd.)
  - Produkty (všechny produktové sloupce)
- ❌ **Neobsahuje:** Redundantní číselné weather sloupce (sunshine, mean_temp, precipitation, pressure, atd.)
- 📊 **Rozměry:** 19,311 řádků × 341 sloupců
- 🎯 **Použití:** Hlavní dataset pro CleverMiner analýzu

**💡 Číselné sekvence (_seq):**
Každá kategorie má číselný ekvivalent (např. `mean_temp_cat_seq`) pro použití s `'type': 'seq'` v CleverMiner dotazech. Umožňuje analýzu ordinálních vztahů (cold < warm < hot).

**Odstraněné sloupce:**
- `sunshine` → použijte `sunshine_cat`
- `mean_temp` → použijte `mean_temp_cat`
- `precipitation` → použijte `precipitation_cat`
- `snow_depth` → použijte `snow_depth_cat`
- `pressure` → použijte `pressure_cat`
- `global_radiation` → použijte `global_radiation_cat`

**Přidané kategorie:**
- `Total_Price_cat` (7 kategorií: very low → very high)
- `Avg_Item_Price_cat` (5 kategorií: budget → luxury)
- `Total_Products_cat` (6 kategorií: tiny → huge)
- `Avg_Item_Quantity_cat` (5 kategorií: single → bulk)

---

## 🔄 Skripty

### Hlavní skripty (používejte tyto!)

#### `CreateAnalyzedDataset.py`
Vytváří optimalizovaný `datasetAnalyzed.csv` z `datasetMerged.csv`.

```bash
python CreateAnalyzedDataset.py
```

**Co dělá:**
1. Načte `datasetMerged.csv`
2. Přidá kategorizované order metriky
3. Vytvoří číselné _seq sloupce pro všechny kategorie (pro ordinální analýzu)
4. Odstraní redundantní číselné weather sloupce
5. Uloží jako `datasetAnalyzed.csv`

#### `MergeDatasets.py`
Spojuje weather a order data do `datasetMerged.csv`.

```bash
python MergeDatasets.py
```

**Co dělá:**
1. Načte `london_weather_categorized.csv` (weather data s kategoriemi)
2. Načte `restaurant-2-orders-wide.csv` (order data)
3. Spojí je podle data
4. Uloží jako `datasetMerged.csv`

---

## 📊 Kategorizované sloupce v analyzed datasetu

### 🛒 Order metriky (4 sloupce)

| Sloupec | Kategorie | Popis |
|---------|-----------|-------|
| `Total_Price_cat` | 7 | very low, low, medium-low, medium, medium-high, high, very high |
| `Avg_Item_Price_cat` | 5 | budget, economy, standard, premium, luxury |
| `Total_Products_cat` | 6 | tiny, small, medium, large, very large, huge |
| `Avg_Item_Quantity_cat` | 5 | single, mostly single, mixed, mostly double, bulk |

### 🌤️ Weather metriky (7 sloupců)

| Sloupec | Kategorie | Popis |
|---------|-----------|-------|
| `mean_temp_cat` | 7 | freezing, very cold, cold, cool, mild, warm, hot |
| `precipitation_cat` | 5 | none, light, moderate, heavy, very heavy |
| `sunshine_cat` | 6 | none, minimal, some, moderate, sunny, very sunny |
| `cloud_cover_cat` | 6 | clear, mostly clear, partly cloudy, mostly cloudy, cloudy, overcast |
| `pressure_cat` | 7 | very low, low, medium-low, medium, medium-high, high, very high |
| `snow_depth_cat` | 2 | no snow, snow present |
| `global_radiation_cat` | 5 | very low, low, medium, high, very high |

---

## 📚 Dokumentace

### `CATEGORIZACE.md`
Detailní popis kategorizace včetně:
- Metodologie (jak byly stanoveny hranice kategorií)
- Distribuce jednotlivých kategorií
- Příklady použití v CleverMiner
- Doporučení pro analýzu

---

## 🚀 Quick Start

1. **Vytvoř analyzed dataset:**
   ```bash
   python CreateAnalyzedDataset.py
   ```

2. **Načti do CleverMiner:**
   ```python
   import pandas as pd
   df = pd.read_csv('datasetAnalyzed.csv')
   ```

3. **Analyzuj s kategoriemi:**
   ```python
   # Příklad: Vliv počasí na hodnotu objednávky
   clm = cleverminer(
       df=df,
       proc='4ftMiner',
       quantifiers={'conf': 0.5, 'Base': 500},
       ante={
           'attributes': [
               {'name': 'mean_temp_cat', 'type': 'subset'},
               {'name': 'precipitation_cat', 'type': 'subset'}
           ]
       },
       succ={
           'attributes': [
               {'name': 'Total_Price_cat', 'type': 'subset'}
           ]
       }
   )
   ```

3. **Pro ordinální analýzu (sekvence):**
   ```python
   # Použij *_cat_seq sloupce
   cleverminer(
       df=df,
       proc='4ftMiner',
       quantifiers={'conf': 0.3, 'Base': 100},
       ante={
           'attributes': [
               {'name': 'mean_temp_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
           ]
       },
       succ={
           'attributes': [
               {'name': 'Total_Products_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 1}
           ]
       }
   )
   
   # Dekóduj výstup zpět na text
   from DecodeCleverMinerOutput import decode_cleverminer_output
   decoded = decode_cleverminer_output(output)
   print(decoded)
   ```

### `DecodeCleverMinerOutput.py`
Převádí číselné kódy z CleverMiner výstupu zpět na textové kategorie.

```bash
# Ze souboru
python DecodeCleverMinerOutput.py output.txt

# V kódu
from DecodeCleverMinerOutput import decode_cleverminer_output
decoded = decode_cleverminer_output("mean_temp_cat_seq(6) => Total_Products_cat_seq(2)")
# Výstup: "mean_temp_cat(warm) => Total_Products_cat(small)"
```

---

## ✅ Checklist

- [x] MergeDatasets.py vytvořil datasetMerged.csv
- [x] CreateAnalyzedDataset.py vytvořil datasetAnalyzed.csv
- [x] Všechny kategorie mají >5% podporu
- [x] Číselné sekvence vytvořeny pro ordinální analýzu
- [ ] CleverMiner pravidla definována
- [ ] Analýza spuštěna
- [ ] Výsledky interpretovány

---

*Pro detaily o metodologii kategorizace viz `CATEGORIZACE.md`*

