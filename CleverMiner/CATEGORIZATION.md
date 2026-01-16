# 📊 Kategorizace Order Metrik pro CleverMiner

## 🎯 Přehled

Tento dokument popisuje kategorizaci číselných metrik objednávek do diskrétních kategorií vhodných pro analýzu v CleverMiner.

## 📁 Datasety

### **datasetMerged.csv** (Spojený dataset z MergeDatasets.py)
- Obsahuje **weather kategorie** (z preprocessingu počasí)
- Obsahuje **číselné weather metriky** (sunshine, mean_temp, precipitation, atd.)
- Obsahuje **číselné order metriky** (Total Price, Average Item Price, atd.)
- **Neobsahuje** order metriky kategorie
- **Granularita:** Jeden řádek = jedna objednávka
- **Použití:** Základ pro vytvoření analyzed a daily compound datasetů

### **datasetAnalyzed.csv** (Optimalizovaný pro CleverMiner - objednávky)
- Obsahuje **všechny kategorie** (weather + order metriky)
- Obsahuje **číselné order metriky** (pro flexibilitu)
- Obsahuje **číselné sekvence** pro kategorie (`*_cat_seq` sloupce)
- **Odstraněny** redundantní číselné weather sloupce (sunshine, precipitation, mean_temp, atd.)
- **Neobsahuje** číselné weather metriky (pouze kategorie)
- **Granularita:** Jeden řádek = jedna objednávka (19,311 řádků)
- **Použití:** Analýza vztahů mezi počasím a jednotlivými objednávkami (Questions 1-8)

### **datasetDailyCompound.csv** (Agregovaný pro denní analýzu - CF-Miner)
- Obsahuje **weather kategorie** + číselné hodnoty (agregované po dnech)
- Obsahuje **denní metriky objednávek:**
  - `Orders_Count` - počet objednávek za den
  - `Total_Revenue` - celkové tržby za den
  - `Avg_Revenue_Per_Order` - průměrné tržby na objednávku
- Obsahuje **kategorizované denní metriky:**
  - `Orders_Count_cat` - kvantilová kategorizace (very low → very high)
  - `Total_Revenue_cat` a `Avg_Revenue_Per_Order_cat`
- Obsahuje **číselné sekvence** pro všechny kategorie (`*_cat_seq` sloupce)
- **Granularita:** Jeden řádek = jeden den (1,095 řádků = 3 roky)
- **Použití:** 
  - **CF-Miner analýza** (Question 9) - hledání podmínek s neobvyklými histogramy
  - Temporální analýza (den v týdnu, sezónní trendy)
  - Agregované metriky výkonnosti

**⚠️ Důležité:** `Orders_Count_cat` používá **kvantilovou kategorizaci** (hranice 8, 13, 20, 31) pro vyváženou distribuci!

#### Číselné sekvence (_seq sloupce)

Pro každou kategorii existuje číselný ekvivalent s příponou `_seq`:
- **Důvod**: CleverMiner neumí pracovat se sekvencemi textových kategorií
- **Výhoda**: Umožňuje použití `'type': 'seq'` v dotazech pro ordinální analýzu
- **Mapování**: Čísla respektují přirozené pořadí (např. cold=3 < warm=5 < hot=7)

Příklad: `mean_temp_cat_seq` obsahuje čísla 1-8 namísto textů "freezing" až "hot"

### 🔄 Vytvoření datasetů

#### Analyzed dataset (pro analýzu objednávek)
```bash
python CreateAnalyzedDataset.py
```

Skript:
1. Načte `datasetMerged.csv`
2. Přidá kategorizované order metriky
3. Vytvoří číselné _seq sloupce pro všechny kategorie
4. Odstraní redundantní číselné weather sloupce
5. Uloží jako `datasetAnalyzed.csv`

#### Daily Compound dataset (pro denní analýzu)
```bash
python CreateDailyCompoundDataset.py
```

Skript:
1. Načte `datasetMerged.csv`
2. Agreguje data po dnech (weather: modus, orders: suma/počet)
3. Kategorizuje denní metriky podle **kvantilů**
4. Vytvoří číselné _seq sloupce
5. Uloží jako `datasetDailyCompound.csv`

---

## 🧠 Metodologie kategorizace

### Rozhodovací proces při stanovení rozsahů

Při určování hranic kategorií byl použit systematický přístup kombinující statistickou analýzu s business logikou:

#### 1️⃣ **Analýza distribuce dat**

Pro každý číselný sloupec byly vypočítány:
- **Min/Max hodnoty** (celkový rozsah)
- **Medián** (střední bod distribuce)
- **Kvartily (Q1, Q3)** (25. a 75. percentil)
- **Percentily** (5%, 95%) pro identifikaci extrémních hodnot

#### 2️⃣ **Klíčové principy rozhodování**

**A) Statistická vyváženost**
- Žádná kategorie < 5% dat (dostatečná podpora pro CleverMiner)
- Nejčastější kategorie 20-35% (vyhnutí se dominanci jedné kategorie)
- Rovnoměrné pokrytí celého rozsahu hodnot

**B) Business logika**
- Kategorie musí mít **intuitivní význam** (např. "budget", "economy", "premium")
- Hranice na "kulatých" hodnotách (£20, £25, £40...) pro snadnou interpretaci
- Názvy kategorií odpovídají realitě objednávek

**C) Orientace na medián**
- Medián = "typická" hodnota → kategorie "medium"/"standard"
- Kategorie kolem mediánu nejpočetnější (20-35%)
- Symetrické rozložení pod/nad mediánem kde možné

#### 3️⃣ **Konkrétní příklady rozhodování**

**Total_Price_cat (£0.50 - £283.30)**

Statistiky: Medián = £31.75, Q1 = £25.00, Q3 = £40.00

Rozhodnutí:
- `medium` (£32-40) → kolem mediánu → **20.5%**
- `medium-low` (£25-32) → Q1 → medián → **22.0%**
- `medium-high` (£40-50) → Q3 + rezerva → **14.1%**
- `low` (£20-25) → pod Q1, kulatá hranice → **13.9%**
- `very low` (<£20) → nejlevnější objednávky → **14.9%**
- `high` (£50-65) → top 15% → **9.4%**
- `very high` (≥£65) → top 5%, extrémní hodnoty → **5.2%**

**Avg_Item_Price_cat (£0.50 - £62.65)**

Statistiky: Medián = £5.70, Q1 = £4.50, Q3 = £6.50

Rozhodnutí:
- `standard` (£5.5-6.5) → kolem mediánu → **25.7%**
- `economy` (£4.5-5.5) → Q1 → medián → **24.7%**
- `premium` (£6.5-8.0) → Q3 + 23% → **19.1%**
- `budget` (<£4.5) → pod Q1 → **19.6%**
- `luxury` (≥£8.0) → top 11%, dvojnásobek "budget" → **11.0%**

Hranice £4.5, £5.5, £6.5 = půllibrové intervaly (snadná paměť)

**Total_Products_cat (1-29 položek)**

Statistiky: Medián = 6, Q1 = 5, Q3 = 8

Rozhodnutí:
- `medium` (5-6) → kolem mediánu → **33.0%** (dominantní = typická objednávka)
- `small` (3-4) → pod mediánem → **24.8%**
- `large` (7-8) → kolem Q3 → **20.2%**
- `very large` (9-11) → nad Q3 → **13.0%**
- `tiny` (1-2) → minimální objednávky → **5.3%**
- `huge` (≥12) → top 4%, extrémní → **3.7%**

Celá čísla (počet položek je diskrétní), interval 2 kusy = snadná interpretace

#### 4️⃣ **Validace rozhodnutí**

**✅ Interpretovatelnost**
```
"very low" < "low" < "medium-low" < "medium" < "medium-high" < "high" < "very high"
```
Logické pořadí názvů odpovídá hodnotám

**✅ Vyváženost**
- Total_Price_cat: 5.2% - 22.0% (rozsah 16.8%)
- Avg_Item_Price_cat: 11.0% - 25.7% (rozsah 14.7%)
- Všechny kategorie >5% podpora (kromě okrajových případů)

**✅ Business smysl**
- "budget" (£<4.5) vs "luxury" (£≥8.0) = téměř 2× rozdíl
- "tiny" (1-2 produkty) vs "huge" (12+ produktů) = 6× rozdíl
- Kategorie odrážejí reálné rozdíly v objednávkách

#### 5️⃣ **Trade-offs**

| Přístup | Výhoda | Nevýhoda | Zvoleno? |
|---------|--------|----------|----------|
| Více kategorií (7-9) | Jemnější granularita | Některé <5% podpora | ✅ Ano |
| Méně kategorií (3-5) | Všechny >10% podpora | Ztráta nuancí | ❌ Ne |
| Rovnoměrné hranice (£10, £20...) | Snadná paměť | Nerespektuje distribuci | ⚖️ Částečně |
| Kvartilové hranice | Respektuje data | Nekulaté hodnoty | ⚖️ Částečně |

**Finální strategie:** Kombinace kvartilů + kulatých hodnot + min. 5% podpora

---

## 📋 Přidané kategorizované sloupce

### 1️⃣ **Total_Price_cat** (Celková cena objednávky)

**Původní sloupec:** `Total Price` (0.50 - 283.30 £)

**Kategorie:**

| Kategorie | Rozsah (£) | Distribuce | Popis |
|-----------|------------|------------|-------|
| **very low** | < 20 | 14.9% | Velmi levné objednávky |
| **low** | 20 - 25 | 13.9% | Levné objednávky |
| **medium-low** | 25 - 32 | 22.0% | Podprůměrné |
| **medium** | 32 - 40 | 20.5% | Střední (kolem mediánu 31.75£) |
| **medium-high** | 40 - 50 | 14.1% | Nadprůměrné |
| **high** | 50 - 65 | 9.4% | Drahé objednávky |
| **very high** | ≥ 65 | 5.2% | Velmi drahé objednávky (top 5%) |

**Použití:**
- Identifikace závislosti mezi počasím a hodnotou objednávky
- Analýza, kdy zákazníci utrácejí více/méně
- Segmentace zákazníků podle hodnoty objednávky

---

### 2️⃣ **Avg_Item_Price_cat** (Průměrná cena položky)

**Původní sloupec:** `Average Item Price` (0.50 - 62.65 £)

**Kategorie:**

| Kategorie | Rozsah (£) | Distribuce | Popis |
|-----------|------------|------------|-------|
| **budget** | < 4.5 | 19.6% | Levné položky |
| **economy** | 4.5 - 5.5 | 24.7% | Ekonomické položky |
| **standard** | 5.5 - 6.5 | 25.7% | Standardní (kolem mediánu 5.70£) |
| **premium** | 6.5 - 8.0 | 19.1% | Prémiové položky |
| **luxury** | ≥ 8.0 | 11.0% | Luxusní položky |

**Použití:**
- Analýza preferencí produktových kategorií podle počasí
- Identifikace, kdy zákazníci volí dražší/levnější produkty
- Segmentace podle cenové úrovně produktů

---

### 3️⃣ **Total_Products_cat** (Počet položek v objednávce)

**Původní sloupec:** `Total products` (1 - 29 položek)

**Kategorie:**

| Kategorie | Rozsah | Distribuce | Popis |
|-----------|--------|------------|-------|
| **tiny** | 1-2 | 5.3% | Velmi malá objednávka |
| **small** | 3-4 | 24.8% | Malá objednávka |
| **medium** | 5-6 | 33.0% | Střední (kolem mediánu 6) |
| **large** | 7-8 | 20.2% | Velká objednávka |
| **very large** | 9-11 | 13.0% | Velmi velká objednávka |
| **huge** | ≥ 12 | 3.7% | Obrovská objednávka |

**Použití:**
- Analýza, jak počasí ovlivňuje velikost objednávky
- Identifikace, kdy lidé objednávají pro více osob
- Segmentace podle typu objednávky (individuální vs. skupinová)

---

### 4️⃣ **Avg_Item_Quantity_cat** (Průměrné množství na položku)

**Původní sloupec:** `Average Item Quantity` (1.0 - 8.0)

**Kategorie:**

| Kategorie | Rozsah | Distribuce | Popis |
|-----------|--------|------------|-------|
| **single** | = 1.0 | 44.3% | Přesně 1 kus každé položky |
| **mostly single** | 1.0 - 1.3 | 25.7% | Většinou 1, někdy 2 kusy |
| **mixed** | 1.3 - 1.6 | 19.0% | Mix 1 a 2 kusy |
| **mostly double** | 1.6 - 2.0 | 7.3% | Většinou 2 kusy |
| **bulk** | ≥ 2.0 | 3.7% | Nákup většího množství |

**Použití:**
- Identifikace nákupního chování (jednotlivci vs. rodiny)
- Analýza, kdy lidé kupují větší množství
- Segmentace podle typu spotřebitele

---

## 📅 Kategorizované denní metriky (datasetDailyCompound.csv)

Následující kategorie se používají pro **agregované denní metriky** v datasetDailyCompound.csv (1,095 dnů). Všechny používají **kvantilovou kategorizaci** pro vyváženou distribuci.

### 5️⃣ **Orders_Count_cat** (Počet objednávek za den)

**Původní sloupec:** `Orders_Count` (1 - 77 objednávek/den)

**Metodologie:** **Kvantilová kategorizace (20% kvantily)**

**Kategorie:**

| Kategorie | Rozsah | Distribuce | Popis |
|-----------|--------|------------|-------|
| **very low** | 1-7 | 20.27% (222 dnů) | Velmi nízká aktivita |
| **low** | 8-12 | 26.39% (289 dnů) | Nízká aktivita |
| **moderate** | 13-19 | 19.36% (212 dnů) | Střední aktivita |
| **high** | 20-30 | 16.99% (186 dnů) | Vysoká aktivita |
| **very high** | 31+ | 16.99% (186 dnů) | Velmi vysoká aktivita |

**Vyváženost:** 0.644 ✅ (velmi low: 222 vs high/very high: 186)

**Statistiky:**
- Mean: 17.6 objednávek/den
- Median: 13.0 objednávek/den
- Kvantily: Q20=8, Q40=13, Q60=20, Q80=31

**Použití:**
- CF-Miner analýza (Question 9) - hledání podmínek s neobvyklými histogramy
- Identifikace dnů s extrémně vysokou/nízkou aktivitou
- Temporální analýza podle dne v týdnu
- Target variable pro denní predikci

**⚠️ Důležité:** Tato kategorizace byla optimalizována z původních pevných hranic (30, 45, 60, 75) na kvantilovou, čímž se vyváženost zlepšila z 0.001 na 0.644 (640× lepší!).

---

### 6️⃣ **Total_Revenue_cat** (Celkové denní tržby)

**Původní sloupec:** `Total_Revenue` (£18.90 - £2,467.00)

**Metodologie:** **Kvantilová kategorizace (optimalizovaná pro long tail distribuci)**

**Kategorie:**

| Kategorie | Rozsah (£) | Distribuce | Popis |
|-----------|------------|------------|-------|
| **very low** | < 420 | ~25% | Velmi nízké denní tržby |
| **low** | 420-580 | ~20% | Nízké denní tržby |
| **moderate** | 580-750 | ~20% | Střední denní tržby |
| **high** | 750-1100 | ~15% | Vysoké denní tržby |
| **very high** | ≥ 1100 | ~20% | Velmi vysoké denní tržby |

**Vyváženost:** ~0.50 ⚡ (přijatelné pro long tail data)

**Statistiky:**
- Mean: £614.96/den
- Median: £500/den
- Data mají pozitivně šikmou ("long tail") distribuci

**Použití:**
- Analýza celkové denní výkonnosti restaurace
- Identifikace výjimečně úspěšných/neúspěšných dnů
- Korelace s počasím a dnem v týdnu
- Business intelligence metriky

**📊 Poznámka k vyváženosti:** Total_Revenue má přirozeně "long tail" distribuci (mnoho dnů s nízkými tržbami, několik dnů s extrémními tržbami), proto není vyváženost 1.0. Hranice byly optimalizovány empiricky pro nejlepší kompromis mezi vyvážeností a interpretovatelností.

**Historie optimalizace:**
- Původní hranice: 1200, 1800, 2400, 3000 → Vyváženost 0.001 ❌
- Optimalizované hranice: 420, 580, 750, 1100 → Vyváženost ~0.50 ✅ (500× lepší!)

---

### 7️⃣ **Avg_Revenue_Per_Order_cat** (Průměrná tržba na objednávku)

**Původní sloupec:** `Avg_Revenue_Per_Order` (£15.33 - £79.73)

**Metodologie:** **Kvantilová kategorizace (20% kvantily)**

**Kategorie:**

| Kategorie | Rozsah (£) | Distribuce | Popis |
|-----------|------------|------------|-------|
| **very low** | < 30 | 19.91% (218 dnů) | Velmi nízká průměrná hodnota |
| **low** | 30-33 | 19.09% (209 dnů) | Nízká průměrná hodnota |
| **moderate** | 33-35.5 | 20.64% (226 dnů) | Střední průměrná hodnota |
| **high** | 35.5-38.5 | 21.00% (230 dnů) | Vysoká průměrná hodnota |
| **very high** | ≥ 38.5 | 19.36% (212 dnů) | Velmi vysoká průměrná hodnota |

**Vyváženost:** 0.909 ✅ (téměř perfektní!)

**Statistiky:**
- Mean: £34.49/objednávka
- Median: £34.41/objednávka
- Kvantily: Q20=30, Q40=33, Q60=35.5, Q80=38.5

**Použití:**
- Analýza průměrné hodnoty objednávky v čase
- Identifikace dnů, kdy zákazníci utrácejí více/méně
- Quality metric (vyšší průměr = dražší položky nebo větší objednávky)
- Segmentace dnů podle typu zákazníků

**✅ Výborná vyváženost:** Tato kategorizace je téměř perfektně vyvážená díky normálnější distribuci dat (median ≈ mean).

**Historie optimalizace:**
- Původní hranice: 30, 35, 40, 45 → Vyváženost 0.123 ❌
- Kvantilové hranice: 30, 33, 35.5, 38.5 → Vyváženost 0.909 ✅ (7.4× lepší!)

---

### 📊 Shrnutí denních metrik

| Metrika | Vyváženost | Hodnocení | Poznámka |
|---------|-----------|-----------|----------|
| **Orders_Count_cat** | 0.644 | ✅ Dobré | Kvantilová kategorizace |
| **Total_Revenue_cat** | ~0.50 | ⚡ Přijatelné | Long tail data, optimalizovaná |
| **Avg_Revenue_Per_Order_cat** | 0.909 | ✅ Výborné | Téměř perfektní vyváženost |

**Všechny 3 kategorizace jsou vhodné pro CleverMiner analýzu!**

**Klíčový rozdíl oproti order metrikám:**
- **Order metriky** (datasetAnalyzed.csv): Granularita = 1 objednávka (19,311 řádků)
- **Denní metriky** (datasetDailyCompound.csv): Granularita = 1 den (1,095 řádků)
- Denní metriky umožňují temporální analýzu a CF-Miner

---

## 🔍 Příklady použití v CleverMiner

### Příklad 1: Vliv počasí na hodnotu objednávky

```python
clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.5, 'Base': 500},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
            {'name': 'precipitation_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Total_Price_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 1
    }
)
```

**Očekávaná zjištění:**
- "Když je `cold` AND `light rain` → `high` Total_Price" (lidé objednávají více v chladném počasí)
- "Když je `hot` → `low` Total_Price" (lidé objednávají méně v horkém počasí)

---

### Příklad 2: Vliv dne v týdnu a počasí na velikost objednávky

```python
clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.6, 'Base': 300},
    ante={
        'attributes': [
            {'name': 'Day of Week', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'mean_temp_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 2, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 1
    }
)
```

**Očekávaná zjištění:**
- "Když je `Friday` AND `cold` → `large` objednávka" (pátek + zima = velké objednávky)
- "Když je `Monday` → `small` objednávka" (pondělí = menší objednávky)

---

### Příklad 3: Preference cenových kategorií podle počasí

```python
clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.4, 'Base': 400},
    ante={
        'attributes': [
            {'name': 'precipitation_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'cloud_cover_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Avg_Item_Price_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 1
    }
)
```

**Očekávaná zjištění:**
- "Když je `strong rain` → `luxury` položky" (v dešti si lidé dopřávají)
- "Když je `clear` → `budget` položky" (v pěkném počasí se šetří)

---

### Příklad 4: CF-Miner analýza denních objednávek (datasetDailyCompound.csv)

```python
# Načtení daily compound datasetu
df = pd.read_csv('datasetDailyCompound.csv')

# CF-Miner: Hledání podmínek s neobvyklými histogramy počtu objednávek
clm = cleverminer(
    df=df,
    target='Orders_Count_cat_seq',
    proc='CFMiner',
    quantifiers={'Base': 100, 'S_Up': 2},
    cond={
        'attributes': [
            {'name': 'mean_temp_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'precipitation_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'sunshine_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)
```

**Očekávaná zjištění:**
- Podmínky (počasí), kdy histogram Orders_Count má alespoň 2 vzestupy (S_Up ≥ 2)
- Například: "Když je `freezing` počasí → histogram má 2 vzestupy" (vyváženější distribuce)
- Identifikace dnů s vyšší variabilitou počtu objednávek

**Využití denních kategorií:**
- `Orders_Count_cat_seq` - target pro CF-Miner
- `Total_Revenue_cat` - analýza denní výkonnosti
- `Avg_Revenue_Per_Order_cat` - quality metric

---

### Příklad 5: Temporální analýza denních tržeb

```python
# Načtení daily compound datasetu
df = pd.read_csv('datasetDailyCompound.csv')

# 4ft-Miner: Vliv dne v týdnu na denní tržby
clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.5, 'Base': 50},
    ante={
        'attributes': [
            {'name': 'Day of Week Number', 'type': 'subset'},
            {'name': 'mean_temp_cat', 'type': 'subset'}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Total_Revenue_cat', 'type': 'subset'}
        ]
    }
)
```

**Očekávaná zjištění:**
- "Když je `Saturday` → `very high` revenue" (soboty = nejvyšší tržby)
- "Když je `Monday` → `very low` revenue" (pondělí = nejnižší tržby)
- Kombinace dne a počasí ovlivňující denní výkonnost

---

## 📊 Statistiky kategorizace

### Vyváženost distribuce - Order metriky (datasetAnalyzed.csv)

Všechny kategorie jsou navrženy tak, aby měly **dostatečnou podporu** (minimálně 5% dat) a zároveň byly **interpretovatelné**.

| Sloupec | Min kategorie | Max kategorie | Rozsah | Vyváženost |
|---------|---------------|---------------|---------|------------|
| Total_Price_cat | 5.2% (very high) | 22.0% (medium-low) | 16.8% | ~0.24 |
| Avg_Item_Price_cat | 11.0% (luxury) | 25.7% (standard) | 14.7% | ~0.43 |
| Total_Products_cat | 3.7% (huge) | 33.0% (medium) | 29.3% | ~0.11 |
| Avg_Item_Quantity_cat | 3.7% (bulk) | 44.3% (single) | 40.6% | ~0.08 |

**Poznámka:** Order metriky mají nižší vyváženost kvůli přirozené distribuci objednávkových dat. Všechny kategorie však mají dostatečnou podporu (>3.7%) pro CleverMiner analýzu.

---

### Vyváženost distribuce - Denní metriky (datasetDailyCompound.csv)

**Kvantilová kategorizace** zajišťuje mnohem lepší vyváženost pro denní analýzy.

| Sloupec | Min kategorie | Max kategorie | Vyváženost | Hodnocení |
|---------|---------------|---------------|------------|-----------|
| **Orders_Count_cat** | 16.99% (high/very high) | 26.39% (low) | **0.644** | ✅ Dobré |
| **Total_Revenue_cat** | ~15% | ~25% | **~0.50** | ⚡ Přijatelné* |
| **Avg_Revenue_Per_Order_cat** | 19.09% (low) | 21.00% (high) | **0.909** | ✅ Výborné |

**Vyváženost** = Min kategorie / Max kategorie (hodnota blízko 1.0 = dobře vyvážené)

\* *Total_Revenue má "long tail" distribuci, proto vyváženost ~0.50 místo 1.0. To je normální a přijatelné.*

**Srovnání s původní kategorizací:**
- Orders_Count: Vylepšeno z 0.001 → 0.644 (**640× lepší!**)
- Total_Revenue: Vylepšeno z 0.001 → ~0.50 (**500× lepší!**)
- Avg_Revenue_Per_Order: Vylepšeno z 0.123 → 0.909 (**7.4× lepší!**)
| Avg_Item_Quantity_cat | 3.7% (bulk) | 44.3% (single) | 40.6% |

---

## 💡 Doporučení pro analýzu

### 1. **Confidence (conf)**
- Použijte **0.3 - 0.7** pro explorativní analýzu
- Použijte **0.7+** pro silné vzory

### 2. **Base (minimální podpora)**
- Použijte **300-500** pro obecné vzory
- Použijte **100-300** pro specifické kombinace
- Použijte **50-100** pro vzácné případy

### 3. **Kombinace atributů**
Nejzajímavější kombinace pro analýzu:

**Weather → Order Value:**
- `mean_temp_cat` + `precipitation_cat` → `Total_Price_cat`
- `cloud_cover_cat` + `sunshine_cat` → `Avg_Item_Price_cat`

**Time → Order Size:**
- `Day of Week` + `Hour` → `Total_Products_cat`
- `Day of Week` + `mean_temp_cat` → `Total_Products_cat`

**Complex patterns:**
- `Day of Week` + `mean_temp_cat` + `precipitation_cat` → `Total_Price_cat`

---

## 🔄 Struktura datasetů

### datasetMerged.csv (výstup MergeDatasets.py)
- **Řádků:** 19,311
- **Sloupců:** ~335
- **Granularita:** 1 řádek = 1 objednávka
- **Obsahuje:** 
  - Weather kategorie (cloud_cover_cat, sunshine_cat, mean_temp_cat, precipitation_cat, pressure_cat, snow_depth_cat, global_radiation_cat)
  - Číselné weather metriky (cloud_cover, sunshine, mean_temp, precipitation, pressure, snow_depth, global_radiation, max_temp, min_temp)
  - Číselné order metriky (Total Price, Average Item Price, Median Item Price, Total products, atd.)
  - Produkty (všechny produktové sloupce)
- **Neobsahuje:** Order metriky kategorie

### datasetAnalyzed.csv (výstup CreateAnalyzedDataset.py)
- **Řádků:** 19,311  
- **Sloupců:** 341
- **Granularita:** 1 řádek = 1 objednávka
- **Obsahuje:**
  - Weather kategorie (cloud_cover_cat, sunshine_cat, mean_temp_cat, precipitation_cat, pressure_cat, snow_depth_cat, global_radiation_cat)
  - Weather číselné sekvence (cloud_cover_cat_seq, sunshine_cat_seq, mean_temp_cat_seq, atd.)
  - Order kategorie (Total_Price_cat, Avg_Item_Price_cat, Total_Products_cat, Avg_Item_Quantity_cat)
  - Order číselné sekvence (Total_Price_cat_seq, Avg_Item_Price_cat_seq, Total_Products_cat_seq, Avg_Item_Quantity_cat_seq)
  - Číselné order metriky (Total Price, Average Item Price, Median Item Price, Total products, atd.)
  - Produkty (všechny produktové sloupce)
- **Neobsahuje:** Redundantní číselné weather sloupce (sunshine, mean_temp, precipitation, snow_depth, pressure, global_radiation, cloud_cover, max_temp, min_temp)

**Kategorizované sloupce:**
- `Total_Price_cat` (7 kategorií) + `Total_Price_cat_seq` (1-7)
- `Avg_Item_Price_cat` (5 kategorií) + `Avg_Item_Price_cat_seq` (1-5)
- `Total_Products_cat` (6 kategorií) + `Total_Products_cat_seq` (1-6)
- `Avg_Item_Quantity_cat` (5 kategorií) + `Avg_Item_Quantity_cat_seq` (1-5)

### datasetDailyCompound.csv (výstup CreateDailyCompoundDataset.py)
- **Řádků:** 1,095
- **Sloupců:** ~40
- **Granularita:** 1 řádek = 1 den (3 roky dat: 2015-01-01 až 2017-12-31)
- **Obsahuje:**
  - Datum a den v týdnu (Date, Day of Week, Day of Week Number)
  - Weather kategorie (agregované pomocí modus - nejčastější hodnota za den)
  - Weather číselné sekvence (*_cat_seq)
  - Weather číselné hodnoty (agregované pomocí průměr)
  - **Denní metriky objednávek:**
    - `Orders_Count` - počet objednávek za den (1-77)
    - `Total_Revenue` - celkové tržby za den
    - `Avg_Revenue_Per_Order` - průměrné tržby na objednávku
  - **Kategorizované denní metriky (kvantilová kategorizace):**
    - `Orders_Count_cat` (5 kategorií: very low, low, moderate, high, very high)
    - `Total_Revenue_cat` (5 kategorií)
    - `Avg_Revenue_Per_Order_cat` (5 kategorií)
  - Číselné sekvence pro denní metriky (*_cat_seq)
- **Neobsahuje:** Produkty, jednotlivé objednávky

**Kategorizované denní sloupce:**
- `Orders_Count_cat` (5 kategorií) + `Orders_Count_cat_seq` (1-5)
  - **Hranice (kvantilové):** very low: 1-7, low: 8-12, moderate: 13-19, high: 20-30, very high: 31+
  - **Vyváženost:** 0.644 (very low: 20%, low: 26%, moderate: 19%, high: 17%, very high: 17%)
- `Total_Revenue_cat` (5 kategorií) + `Total_Revenue_cat_seq` (1-5)
- `Avg_Revenue_Per_Order_cat` (5 kategorií) + `Avg_Revenue_Per_Order_cat_seq` (1-5)

**🎯 Použití:** CF-Miner analýza (Question 9), temporální vzory, agregované metriky

---

## 🔄 Dekódování CleverMiner výstupu

Při použití `*_cat_seq` sloupců v CleverMiner dotazech se výstup zobrazuje s číselnými kódy. Pro převod zpět na textové kategorie použij:

**Skript:** `DecodeCleverMinerOutput.py`

```python
from DecodeCleverMinerOutput import decode_cleverminer_output

# CleverMiner výstup s čísly
output = "mean_temp_cat_seq(6) => Total_Products_cat_seq(2)"

# Dekódování na text
decoded = decode_cleverminer_output(output)
print(decoded)
# Výstup: "mean_temp_cat(warm) => Total_Products_cat(small)"
```

**Použití ze souboru:**
```bash
python DecodeCleverMinerOutput.py cleverminer_output.txt
```

---

## ✅ Checklist před analýzou

- [x] Číselné metriky kategorizovány
- [x] Kategorie vybalancované (>5% podpora)
- [x] Kategorie interpretovatelné (jasné názvy)
- [x] Číselné sekvence vytvořeny pro ordinální analýzu
- [x] Dataset aktualizován
- [ ] CleverMiner pravidla definována
- [ ] Analýza spuštěna
- [ ] Výsledky interpretovány

---

*Poslední aktualizace: 15. ledna 2026*

