# 📊 Dokumentace projektu: Analýza závislosti počasí na objednávky s sebou

**Předmět:** 4IZ503 Projektový seminář  
**Program:** Datové inženýrství FIS VŠE  
**Datum obhajoby:** Leden 2026

---

## 📋 Obsah

1. [Úvod](#úvod)
2. [Zdroje dat](#zdroje-dat)
3. [Struktura projektu](#struktura-projektu)
4. [Postup zpracování dat](#postup-zpracování-dat)
5. [Finální datasety pro Power BI](#finální-datasety-pro-power-bi)
6. [Návod k použití](#návod-k-použití)

---

## 🎯 Úvod

Cílem projektu je analyzovat závislost počasí v Londýně na objednávky s sebou ve vybrané indické restauraci. Projekt kombinuje dva datasety:

1. **Objednávky z restaurace** - detailní data o objednávkách jídel s sebou
2. **Počasí v Londýně** - denní meteorologická data

Výsledné zpracované datasety jsou připraveny pro import do Power BI s českým formátováním (čárka jako desetinný oddělovač).

---

## 📦 Zdroje dat

### 1. Takeaway Food Orders
- **Zdroj:** [Kaggle - 19560 Indian Takeaway Orders](https://www.kaggle.com/datasets/henslersoftware/19560-indian-takeaway-orders)
- **Popis:** Objednávky z indické restaurace obsahující informace o produktech, cenách, množství a časech objednávek
- **Období:** 2013-2019
- **Vybraná restaurace:** Restaurant 2 (lepší pokrytí dat)

### 2. London Weather Data
- **Zdroj:** [Kaggle - London Weather Data](https://www.kaggle.com/datasets/emmanuelfwerr/london-weather-data/data)
- **Popis:** Denní meteorologická data z Londýna včetně teploty, srážek, sluneční svit, oblačnosti, atd.
- **Období:** 1979-2020
- **Vyfiltrováno:** 2016-07-26 až 2019-08-03 (synchronizace s daty objednávek)

---

## 📁 Struktura projektu

```
4IZ503/
├── README.md
├── DOKUMENTACE.md (tento soubor)
├── Úvodní zpráva.pptx
└── Datasets/
    ├── Takeout/
    │   ├── DownloadTakeout.py          # Stažení dat z Kaggle
    │   ├── AnalyzeTakeoutDataset.py    # Explorační analýza
    │   ├── AnalyzeRestaurantOrderDates.py  # Analýza pokrytí dat
    │   ├── TrimChosenDataset.py        # Oříznutí a normalizace
    │   ├── WidenChosenDataset.py       # Transformace do wide formátu
    │   └── Datasets/
    │       ├── Original/               # Původní stažená data
    │       ├── restaurant-2-orders-trimmed.csv  # Očištěná data
    │       └── restaurant-2-orders-wide.csv     # Wide formát
    ├── Weather/
    │   ├── DownloadWeather.py          # Stažení dat z Kaggle
    │   ├── AnalyzeWeather.py           # Explorační analýza
    │   ├── FilterReformatCategorizeWeather.py  # Filtrace a kategorizace
    │   └── Datasets/
    │       ├── Original/               # Původní stažená data
    │       └── london_weather_categorized.csv  # Zpracovaná data
    ├── PreparePBIDatasets.py           # Příprava dat pro Power BI
    └── PBI/                            # Finální datasety pro Power BI
        ├── restaurant-2-orders-wide.csv
        ├── london_weather_categorized.csv
        ├── products.csv
        └── order-items.csv
```

---

## 🔄 Postup zpracování dat

### FÁZE 1: Stažení a explorační analýza

#### 1.1 Stažení dat (`DownloadTakeout.py`, `DownloadWeather.py`)

**Účel:** Stažení datasetů z Kaggle do lokální složky `Datasets/Original/`

**Proces:**
- Použití knihovny `kagglehub` pro automatické stažení
- Kopírování souborů do strukturované složky Original
- Zachování původních dat pro případnou referenci

**Výstupy:**
- `restaurant-1-orders.csv`, `restaurant-2-orders.csv`
- `restaurant-1-products-price.csv`, `restaurant-2-products-price.csv`
- `london_weather.csv`

---

#### 1.2 Analýza objednávek (`AnalyzeTakeoutDataset.py`)

**Účel:** Explorační analýza dat objednávek, zjištění typů proměnných a základních statistik

**Provedené analýzy:**
- Počet řádků a sloupců
- Unikátní hodnoty v jednotlivých sloupcích
- Chybějící hodnoty
- Min, Max, Průměr pro číselné proměnné
- Klasifikace typů proměnných:
  - **Časový:** Order Date
  - **Identifikátor:** Order ID
  - **Kategoriální:** Item Name
  - **Diskrétní:** Quantity, Total products
  - **Spojitý:** Product Price

---

#### 1.3 Analýza pokrytí dat (`AnalyzeRestaurantOrderDates.py`)

**Účel:** Zjistit časové pokrytí objednávek a identifikovat chybějící dny

**Zjištění:**
- **Restaurant 1:** Velké množství chybějících dnů, dlouhé období bez dat
- **Restaurant 2:** Výrazně lepší pokrytí, kontinuálnější data
- **Rozhodnutí:** Použít Restaurant 2 pro analýzu

**Identifikované problémy:**
- Výpadky v datech před 25.7.2016
- Několik chybějících dnů ve sledovaném období

---

#### 1.4 Analýza počasí (`AnalyzeWeather.py`)

**Účel:** Explorační analýza meteorologických dat

**Provedené analýzy:**
- Definice typů proměnných (časový, kategoriální, spojitý)
- Základní statistiky: Min, Max, Průměr, Medián, Modus
- Identifikace chybějících hodnot
- Zjištění rozsahu dat: 1979-2020

**Klíčové proměnné:**
- `cloud_cover` - oblačnost (0-9)
- `sunshine` - sluneční svit (hodiny)
- `global_radiation` - globální radiace (W/m²)
- `max_temp`, `mean_temp`, `min_temp` - teploty (°C)
- `precipitation` - srážky (mm)
- `pressure` - tlak (Pa)
- `snow_depth` - výška sněhu (cm)

---

### FÁZE 2: Čištění a transformace dat

#### 2.1 Oříznutí a normalizace objednávek (`TrimChosenDataset.py`)

**Účel:** Příprava čistých dat pro další zpracování

**Provedené kroky:**

1. **Načtení dat**
   - Restaurant-2 objednávky
   - Ceník produktů

2. **Normalizace názvů produktů**
   - **Problém:** Produkty v objednávkách měly různou velikost písmen než v ceníku
     - Objednávky: `"Korma - chicken"` (malé "c")
     - Ceník: `"Korma - Chicken"` (velké "C")
   - **Řešení:** Case-insensitive mapování názvů podle ceníku
   - **Výsledek:** 302 unikátních produktů normalizováno

3. **Parsování datumu**
   - Převod `Order Date` (formát: `dd/mm/YYYY HH:MM`) na datetime
   - Odstranění řádků s nevalidními daty

4. **Rozdělení datum/čas**
   - Rozdělení na samostatné sloupce `Date` a `Time`
   - Odstranění původního sloupce `Order Date`

5. **Oříznutí časového období**
   - Cutoff datum: **2016-07-25**
   - Důvod: Eliminace období s dlouhými výpadky v datech
   - Finální období: **26.7.2016 - 3.8.2019**

6. **Kontrola pokrytí**
   - 1104 dní v rozsahu
   - Chybějící dny: 4 (2018-04-12, 2018-04-13, 2018-04-14, 2018-12-25)
   - Pokrytí: 99.6%

**Výstup:**
- `restaurant-2-orders-trimmed.csv` - 116,984 řádků
- Sloupce: Order ID, Item Name, Quantity, Product Price, Total products, Date, Time

---

#### 2.2 Transformace do wide formátu (`WidenChosenDataset.py`)

**Účel:** Vytvoření agregovaného datasetu na úrovni objednávek s metrikami

**Provedené kroky:**

1. **Načtení a normalizace**
   - Načtení trimmed datasetu
   - Opětovná normalizace názvů produktů (double-check)

2. **Pivotování objednávek**
   - Transformace z long formátu (jeden řádek = jedna položka) na wide formát (jeden řádek = jedna objednávka)
   - Vytvoření sloupců pro každý produkt s hodnotami množství

3. **Doplnění všech produktů z ceníku**
   - Zajištění, že všechny produkty mají sloupec (i když nebyly v objednávkách)
   - Celkem: 302 produktových sloupců

4. **Přidání metadat objednávky**
   - Date, Time, Total products z původních dat

5. **Přidání temporálních dimenzí**
   
   **a) Den v týdnu:**
   - `Day of Week` - textový název (Monday, Tuesday, ...)
   - `Day of Week Number` - číselná hodnota (0=Monday, 6=Sunday)
   - Účel: Analýza podle dne v týdnu, identifikace vzorců pracovní dny vs. víkend
   
   **b) Časová hierarchie:**
   - `Hour` - hodina objednávky (0-23)
   - `Minute` - minuta objednávky (0-59)
   - `Second` - sekunda objednávky (0-59)
   - Účel: Detailní časová analýza, hierarchie pro Power BI

6. **Výpočet cenových metrik**
   
   **a) Total Price:**
   - Součet cen všech položek v objednávce
   - Kalkulace: Quantity × Product Price pro každý produkt
   
   **b) Average Item Price:**
   - Průměrná cena položky v objednávce
   - Vzorec: Total Price ÷ Total products
   
   **c) Median Item Price:** ⭐ *Nově přidáno*
   - Medián cen položek v objednávce
   - Důvod: Robustnější míra než průměr, odolnější vůči odlehlým hodnotám
   
   **d) Cheapest Item Price:**
   - Cena nejlevnější položky v objednávce
   
   **e) Most Expensive Item Price:**
   - Cena nejdražší položky v objednávce

7. **Výpočet množstevních metrik**
   
   **a) Average Item Quantity:**
   - Průměrné množství produktů na položku
   
   **b) Max Item Quantity:**
   - Maximální množství jedné položky
   
   **c) Min Item Quantity:**
   - Minimální množství jedné položky

8. **Přeskládání sloupců**
   - Metriky na začátku (17 sloupců)
   - Produkty na konci (302 sloupců)
   - Celkem: 319 sloupců

**Výstup:**
- `restaurant-2-orders-wide.csv` - 19,311 objednávek × 319 sloupců
- Formát: Jeden řádek = jedna objednávka

**Struktura sloupců:**
1. Date, Day of Week, Day of Week Number
2. Time, Hour, Minute, Second
3. Total products
4. Total Price, Average Item Price, Median Item Price
5. Cheapest Item Price, Most Expensive Item Price
6. Average Item Quantity, Max Item Quantity, Min Item Quantity
7. 302 produktových sloupců (množství jednotlivých produktů)

---

#### 2.3 Filtrace a kategorizace počasí (`FilterReformatCategorizeWeather.py`)

**Účel:** Přizpůsobení a obohacení dat o počasí pro analýzu

**Provedené kroky:**

1. **Načtení a reformatování**
   - Převod `date` (formát: YYYYMMDD) na datetime
   - Přejmenování na `Date` pro konzistenci

2. **Filtrace časového období**
   - Synchronizace s daty objednávek: **2016-07-26 až 2019-08-03**
   - Výsledek: 1,104 dní

3. **Doplnění chybějících hodnot**
   - `cloud_cover`: 7 (modus)
   - `global_radiation`: 95.0 (medián)
   - `max_temp`: 15.0 (medián)
   - `mean_temp`: 11.4 (medián)
   - `min_temp`: 7.8 (medián)
   - `precipitation`: 0.0 (většinová hodnota)
   - `pressure`: 101620.0 (medián)
   - `snow_depth`: 0.0 (většinová hodnota)

4. **Kategorizace proměnných**

   Každá číselná meteorologická proměnná byla kategorizována pro snadnější interpretaci:

   **a) Oblačnost (`cloud_cover_cat`):**
   - 0: clear
   - 1-2: mostly clear
   - 3-4: partly cloudy
   - 5-6: mostly cloudy
   - 7-8: overcast
   - 9: sky obscured

   **b) Sluneční svit (`sunshine_cat`):**
   - 0: none
   - ≤2: very short
   - ≤4: short
   - ≤6: moderate
   - ≤8: long
   - >8: very long

   **c) Globální radiace (`global_radiation_cat`):**
   - ≤50: very low
   - ≤100: low
   - ≤150: moderate
   - ≤250: high
   - ≤400: very high
   - >400: extreme

   **d) Průměrná teplota (`mean_temp_cat`):**
   - <-5°C: hard freezing
   - <0°C: freezing
   - <5°C: very cold
   - <10°C: cold
   - <15°C: fresh
   - <20°C: warm
   - <25°C: very warm
   - ≥25°C: hot

   **e) Srážky (`precipitation_cat`):**
   - 0: no rain
   - <1: very light
   - ≤10: light
   - ≤30: medium
   - ≤70: strong
   - ≤150: very strong
   - >150: extremely strong

   **f) Výška sněhu (`snow_depth_cat`):**
   - 0: none
   - ≤2: trace
   - ≤5: shallow
   - ≤10: moderate
   - ≤20: deep
   - >20: very deep

   **g) Tlak (`pressure_cat`):**
   - <995 hPa: extremely low
   - <1000 hPa: very low
   - <1005 hPa: low
   - <1010 hPa: normal
   - <1015 hPa: high
   - <1020 hPa: very high
   - ≥1020 hPa: extremely high

5. **Uspořádání sloupců**
   - Date na začátku
   - Číselné hodnoty + kategorie pro každou proměnnou

**Výstup:**
- `london_weather_categorized.csv` - 1,104 dní × 17 sloupců
- Obsahuje: surová data + kategorizované varianty

---

### FÁZE 3: Příprava pro Power BI

#### 3.1 Export a formátování (`PreparePBIDatasets.py`)

**Účel:** Vytvoření finálních datasetů optimalizovaných pro Power BI s českým formátováním

**Klíčové transformace:**

1. **České formátování čísel**
   - Všechny float hodnoty převedeny na string s **čárkou** místo tečky
   - Příklad: `45.55` → `45,55`
   - Důvod: Power BI v českém prostředí očekává čárku jako oddělovač

2. **Odstranění produktových sloupců z orders**
   - Z wide datasetu (319 sloupců) ponecháno pouze 17 metrik
   - Důvod: Vytvoření hvězdicového schématu (star schema)
   - Produkty budou v samostatné tabulce

3. **Vytvoření products tabulky**
   - Extrakce seznamu všech produktů z ceníku (302 produktů)
   - Přidání `Product ID` (1-302) pro propojení
   - Sloupce: Product ID, Item Name, Product Price

4. **Vytvoření order-items propojovací tabulky**
   - Transformace trimmed datasetu na bridge table
   - Mapování produktů pomocí Product ID
   - 116,984 záznamů (každý řádek = jeden produkt v objednávce)
   - Sloupce: Order ID, Product ID, Item Name, Quantity, Product Price

5. **Encoding**
   - Použití UTF-8 with BOM (utf-8-sig)
   - Důvod: Správné zobrazení českých znaků v Power BI

**Výstupy (složka PBI/):**

1. **restaurant-2-orders-wide.csv**
   - 19,311 objednávek × 17 sloupců
   - Pouze agregované metriky
   - České formátování čísel s čárkou

2. **london_weather_categorized.csv**
   - 1,104 dní × 17 sloupců
   - Surová data + kategorie
   - České formátování čísel s čárkou

3. **products.csv**
   - 302 produktů × 3 sloupce
   - Product ID, Item Name, Product Price
   - České formátování cen s čárkou

4. **order-items.csv**
   - 116,984 záznamů × 5 sloupců
   - Propojovací tabulka mezi orders a products
   - České formátování čísel s čárkou

---

## 📊 Finální datasety pro Power BI

### 1. restaurant-2-orders-wide.csv

**Účel:** Faktová tabulka objednávek s agregovanými metrikami

**Sloupce (17):**

| Sloupec | Typ | Popis |
|---------|-----|-------|
| Order ID | Integer | Unikátní ID objednávky |
| Date | Date | Datum objednávky (YYYY-MM-DD) |
| Day of Week | String | Den v týdnu (Monday, Tuesday, ...) |
| Day of Week Number | Integer | Číslo dne (0=Monday, 6=Sunday) |
| Time | Time | Čas objednávky (HH:MM:SS) |
| Hour | Integer | Hodina objednávky (0-23) |
| Minute | Integer | Minuta objednávky (0-59) |
| Second | Integer | Sekunda objednávky (0-59) |
| Total products | Integer | Celkový počet položek v objednávce |
| Total Price | String | Celková cena objednávky (s čárkou) |
| Average Item Price | String | Průměrná cena položky (s čárkou) |
| Median Item Price | String | Medián ceny položky (s čárkou) |
| Cheapest Item Price | String | Nejlevnější položka (s čárkou) |
| Most Expensive Item Price | String | Nejdražší položka (s čárkou) |
| Average Item Quantity | String | Průměrné množství položky (s čárkou) |
| Max Item Quantity | String | Maximální množství položky (s čárkou) |
| Min Item Quantity | String | Minimální množství položky (s čárkou) |

**Využití:**
- Časová analýza objednávek
- Analýza podle dne v týdnu
- Agregace podle hodin/minut
- Spojení s počasím pomocí Date

---

### 2. london_weather_categorized.csv

**Účel:** Dimenzní tabulka počasí s denními hodnotami

**Sloupce (17):**

| Sloupec | Typ | Popis |
|---------|-----|-------|
| Date | Date | Datum (YYYY-MM-DD) |
| cloud_cover | Integer | Oblačnost (0-9) |
| cloud_cover_cat | String | Kategorie oblačnosti |
| sunshine | String | Sluneční svit v hodinách (s čárkou) |
| sunshine_cat | String | Kategorie slunečního svitu |
| global_radiation | String | Globální radiace W/m² (s čárkou) |
| global_radiation_cat | String | Kategorie radiace |
| max_temp | String | Max teplota °C (s čárkou) |
| mean_temp | String | Průměrná teplota °C (s čárkou) |
| mean_temp_cat | String | Kategorie průměrné teploty |
| min_temp | String | Min teplota °C (s čárkou) |
| precipitation | String | Srážky mm (s čárkou) |
| precipitation_cat | String | Kategorie srážek |
| pressure | String | Tlak Pa (s čárkou) |
| pressure_cat | String | Kategorie tlaku |
| snow_depth | String | Výška sněhu cm (s čárkou) |
| snow_depth_cat | String | Kategorie sněhu |

**Využití:**
- Spojení s objednávkami pomocí Date
- Analýza vlivu počasí na objednávky
- Kategorizace pro snadnější interpretaci

---

### 3. products.csv

**Účel:** Dimenzní tabulka produktů/ingrediencí

**Sloupce (3):**

| Sloupec | Typ | Popis |
|---------|-----|-------|
| Product ID | Integer | Unikátní ID produktu (1-302) |
| Item Name | String | Název produktu |
| Product Price | String | Cena produktu £ (s čárkou) |

**Využití:**
- Referenční seznam všech produktů
- Spojení s order-items pomocí Product ID
- Analýza produktů podle ceny

---

### 4. order-items.csv

**Účel:** Propojovací tabulka (bridge table) mezi objednávkami a produkty

**Sloupce (5):**

| Sloupec | Typ | Popis |
|---------|-----|-------|
| Order ID | Integer | ID objednávky |
| Product ID | Integer | ID produktu |
| Item Name | String | Název produktu |
| Quantity | Integer | Množství |
| Product Price | String | Cena produktu £ (s čárkou) |

**Využití:**
- Propojení orders ↔ products
- Detailní analýza produktů v objednávkách
- Výpočet many-to-many metrik

---

## 🔗 Datový model pro Power BI

### Star Schema (hvězdicové schéma)

```
                    ┌─────────────────────────┐
                    │  london_weather_        │
                    │  categorized            │
                    │  (Weather Dimension)    │
                    │  • Date [PK]            │
                    │  • Počasí + kategorie   │
                    └──────────┬──────────────┘
                               │
                               │ 1:N
                         [Date]│
                               │
          ┌────────────────────▼────────────────────┐
          │  restaurant-2-orders-wide               │
          │  (Orders Fact Table)                    │
          │  • Order ID [PK] ◄──────────────┐       │
          │  • Date [FK]                    │       │
          │  • Day of Week, Time            │       │
          │  • Cenové a množstevní metriky  │       │
          └─────────────────────────────────┘       │
                                                    │
                                           1:N      │
                                      [Order ID]    │
                                                    │
                         ┌──────────────────────────┴──────┐
                         │      order-items                │
                         │   (Bridge Table)                │
                         │   • Order ID [FK]               │
                         │   • Product ID [FK] ◄────┐      │
                         │   • Quantity                    │
                         └─────────────────────────────────┘
                                                          │
                                                 N:1      │
                                          [Product ID]    │
                                                          │
                                   ┌──────────────────────▼──┐
                                   │     products            │
                                   │ (Product Dimension)     │
                                   │ • Product ID [PK]       │
                                   │ • Item Name             │
                                   │ • Product Price         │
                                   └─────────────────────────┘
```

### Vztahy

1. **orders ↔ weather** (Many-to-One)
   - `restaurant-2-orders-wide.Date` → `london_weather_categorized.Date`
   - Kardinalita: N:1
   - Cross-filter: Obousměrný

2. **orders ↔ order-items** (One-to-Many)
   - `restaurant-2-orders-wide.Order ID` → `order-items.Order ID`
   - Kardinalita: 1:N
   - Cross-filter: Obousměrný

3. **order-items ↔ products** (Many-to-One)
   - `order-items.Product ID` → `products.Product ID`
   - Kardinalita: N:1
   - Cross-filter: Obousměrný

---

## 🚀 Návod k použití

### 1. Příprava prostředí

```bash
# Instalace závislostí
pip install pandas kagglehub

# Konfigurace Kaggle API
# Stáhnout kaggle.json z Kaggle → Account → Create New API Token
# Umístit do ~/.kaggle/ (Linux/Mac) nebo C:\Users\<username>\.kaggle\ (Windows)
```

### 2. Stažení dat

```bash
cd Datasets/Takeout
python DownloadTakeout.py

cd ../Weather
python DownloadWeather.py
```

### 3. Analýza dat (volitelné)

```bash
# Analýza objednávek
python Datasets/Takeout/AnalyzeTakeoutDataset.py
python Datasets/Takeout/AnalyzeRestaurantOrderDates.py

# Analýza počasí
python Datasets/Weather/AnalyzeWeather.py
```

### 4. Zpracování dat

```bash
# Objednávky
python Datasets/Takeout/TrimChosenDataset.py
python Datasets/Takeout/WidenChosenDataset.py

# Počasí
python Datasets/Weather/FilterReformatCategorizeWeather.py
```

### 5. Export pro Power BI

```bash
python Datasets/PreparePBIDatasets.py
```

Výsledné soubory budou v `Datasets/PBI/`

### 6. Import do Power BI

1. **Otevřít Power BI Desktop**

2. **Importovat datasety:**
   - Home → Get Data → Text/CSV
   - Importovat všechny 4 soubory z `Datasets/PBI/`
   - Při importu: použít **Czech (Czech Republic)** locale pro správné rozpoznání čárek

3. **Nastavit datové typy:**
   - V Power Query Editoru zkontrolovat a upravit typy sloupců
   - Číselné sloupce s čárkou nastavit jako Decimal Number
   - Date sloupce nastavit jako Date
   - Time sloupce nastavit jako Time

4. **Vytvořit vztahy (Model View):**
   ```
   restaurant-2-orders-wide[Date] → london_weather_categorized[Date]
   restaurant-2-orders-wide[Order ID] → order-items[Order ID]
   order-items[Product ID] → products[Product ID]
   ```

5. **Vytvořit hierarchie (pro snadnější analýzu):**
   
   **Časová hierarchie:**
   - Název: "Time Hierarchy"
   - Úrovně: Hour → Minute → Second
   
   **Denní hierarchie:**
   - Název: "Day Hierarchy"
   - Úrovně: Day of Week Number → Day of Week

6. **Vytvořit měřítka (Measures):**
   
   ```DAX
   Total Orders = COUNTROWS('restaurant-2-orders-wide')
   
   Total Revenue = SUM('restaurant-2-orders-wide'[Total Price])
   
   Avg Order Value = AVERAGE('restaurant-2-orders-wide'[Total Price])
   
   Orders per Day = 
   DIVIDE(
       COUNTROWS('restaurant-2-orders-wide'),
       DISTINCTCOUNT('restaurant-2-orders-wide'[Date])
   )
   ```

---

## 📈 Možnosti analýzy

### Časové vzory

- **Analýza podle dne v týdnu:** Který den má nejvíce objednávek?
- **Analýza podle hodin:** Kdy je peak hour?
- **Sezónní trendy:** Měsíční/čtvrtletní vzory
- **Víkend vs. pracovní dny:** Rozdíly v chování

### Vliv počasí

- **Teplota vs. objednávky:** Jak teplota ovlivňuje počet objednávek?
- **Srážky vs. objednávky:** Objednává se více v dešti?
- **Sluneční svit:** Vliv počtu hodin slunečního svitu
- **Kategorizované analýzy:** Porovnání podle kategorií počasí

### Produktová analýza

- **Nejoblíbenější produkty:** Top 10 produktů podle množství/tržeb
- **Cenová analýza:** Rozdělení produktů podle cenových kategorií
- **Korelace produktů:** Které produkty se objednávají společně?
- **Produkty podle počasí:** Mění se preference produktů podle počasí?

### Metriky objednávek

- **Průměrná hodnota objednávky:** Trend v čase
- **Počet položek v objednávce:** Distribuce a trendy
- **Cenové rozpětí:** Analýza nejlevnějších a nejdražších položek
- **Medián vs. průměr:** Identifikace odlehlých hodnot

---

## 🔧 Technické poznámky

### Normalizace názvů produktů

**Problém:** V originálních datech byly produkty s různou velikostí písmen:
- Objednávky: `"Korma - chicken"`
- Ceník: `"Korma - Chicken"`

**Řešení:** Case-insensitive mapování v `TrimChosenDataset.py`:
```python
product_name_map = {}
for product_name in products['Item Name']:
    product_name_lower = product_name.lower()
    if product_name_lower not in product_name_map:
        product_name_map[product_name_lower] = product_name

df['Item Name'] = df['Item Name'].str.lower().map(product_name_map).fillna(df['Item Name'])
```

### České formátování

**Implementace převodu čárky:**
```python
def convert_decimals_to_comma(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].dtype == 'float64':
            df_copy[col] = df_copy[col].apply(
                lambda x: str(x).replace('.', ',') if pd.notna(x) else ''
            )
    return df_copy
```

### Temporal Features

**Extrakce dne v týdnu:**
```python
orders_meta['Date_dt'] = pd.to_datetime(orders_meta['Date'])
orders_meta['Day of Week'] = orders_meta['Date_dt'].dt.day_name()
orders_meta['Day of Week Number'] = orders_meta['Date_dt'].dt.dayofweek
```

**Extrakce časových komponent:**
```python
orders_meta['Time_dt'] = pd.to_datetime(orders_meta['Time'], format='%H:%M:%S')
orders_meta['Hour'] = orders_meta['Time_dt'].dt.hour
orders_meta['Minute'] = orders_meta['Time_dt'].dt.minute
orders_meta['Second'] = orders_meta['Time_dt'].dt.second
```

---

## 📝 Changelog

### 2026-01-14
- ✅ Přidán sloupec Median Item Price do objednávek
- ✅ Implementována normalizace názvů produktů (case-insensitive)
- ✅ Přidány sloupce Day of Week a Day of Week Number
- ✅ Přidána časová hierarchie (Hour, Minute, Second)
- ✅ Vytvořeno star schema s propojovacími tabulkami
- ✅ Implementováno české formátování s čárkou
- ✅ Vytvořena kompletní dokumentace

---

## 👥 Autor

Projekt vytvořen v rámci předmětu **4IZ503 Projektový seminář**  
Magisterský program **Datové inženýrství**  
Fakulta informatiky a statistiky, VŠE Praha

---

## 📚 Reference

1. **Takeaway Food Orders Dataset**  
   https://www.kaggle.com/datasets/henslersoftware/19560-indian-takeaway-orders

2. **London Weather Data**  
   https://www.kaggle.com/datasets/emmanuelfwerr/london-weather-data

3. **Power BI Documentation**  
   https://docs.microsoft.com/en-us/power-bi/

4. **Pandas Documentation**  
   https://pandas.pydata.org/docs/

---

*Poslední aktualizace: 14. ledna 2026*

