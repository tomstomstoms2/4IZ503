# 🔍 CleverMiner Otázky a Výsledky

Tento dokument popisuje jednotlivé výzkumné otázky analyzované pomocí CleverMiner.

---

## Question 1: Vliv slunečního svitu na velikost a cenu objednávek

### 🎯 Výzkumná otázka
**Ovlivňuje intenzita slunečního svitu chování zákazníků?**

Konkrétně: Objednávají lidé méně/jinak při dlouhém slunečním svitu (krásné počasí)?

### ⚙️ Konfigurace

**Soubor:** `Question1.py`

**Antecedent (příčina):**
- `sunshine_cat_seq` - sekvence délky slunečního svitu (1-3 prvky)
- Kategorie: none, very short, short, moderate, long, very long
- Typ: ordinální sekvence

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` - velikost objednávky (1-2 prvky)
- `Total_Price_cat_seq` - cena objednávky (1-2 prvky)
- Typ: ordinální sekvence

**Kvantifikátory:**
- Confidence: ≥ 0.1 (10%)
- Base: ≥ 100 objednávek
- AAD: ≥ 0.1 (významný rozdíl)

### 📊 Výsledky

**Celkově nalezeno:** 8 pravidel (z 1,581 ověření)

#### ☀️ Klíčová zjištění:

**1. Dlouhý sluneční svit → malé levné objednávky**
```
sunshine_cat(long) => Total_Products_cat(tiny, small) & Total_Price_cat(very low)
Base: 330 | Confidence: 14.6% | AAD: +0.136
```
**Interpretace:** Při dlouhém slunečním svitu (6-8h) lidé objednávají **malé porce za velmi nízké ceny**.

**2. Velmi dlouhý svit → velmi nízké ceny dominují**
```
sunshine_cat(very long) => Total_Price_cat(very low)
Base: 591 | Confidence: 16.4% | AAD: +0.101
```
**Interpretace:** Při velmi dlouhém slunečním svitu (>8h) převažují **nejlevnější objednávky**.

**3. Střední sluneční svit → větší dražší objednávky**
```
sunshine_cat(moderate) => Total_Products_cat(medium, large) & Total_Price_cat(medium-high, high)
Base: 389 | Confidence: 15.0% | AAD: +0.122
```
**Interpretace:** Při středním slunečním svitu (4-6h) lidé objednávají **větší množství za vyšší ceny**.

**4. Dlouhý nebo velmi dlouhý sluneční svit → malé levné objednávky**
```
sunshine_cat(long, very long) => Total_Products_cat(tiny, small) & Total_Price_cat(very low)
Base: 847 | Confidence: 14.5% | AAD: +0.125
```
**Interpretace:** Při dlouhém NEBO velmi dlouhém slunečním svitu (6-8h nebo >8h) lidé preferují **malé levné svačinky**. Toto pravidlo kombinuje obě kategorie.

#### 📈 Trendy:

| Sluneční svit | Velikost objednávek | Cena objednávek | Confidence | AAD |
|---------------|---------------------|-----------------|------------|-----|
| **Moderate** (4-6h) | Medium-Large | Medium-high/High | 15.0% | +0.122 |
| **Long** (6-8h) | Tiny-Small | Very low | 14.6% | **+0.136** |
| **Very long** (>8h) | Tiny-Small | Very low | 16.4% | +0.101 |

### 💡 Závěry

1. **Inverzní korelace:** Sluneční svit ↑ → Velikost a cena objednávek ↓
2. **Jasný pattern:** Krásné počasí = malé levné objednávky
3. **Střední svit = výjimka:** Při 4-6h slunce jsou větší a dražší objednávky
4. **Highest AAD:** Long sunshine → very low price (AAD +0.136)
5. **Business insight:** 
   - Při krásném počasí lidé **jdí ven** → méně objednávají
   - Pouze **rychlé svačinky** místo velkých obědů/večeří
   - Střední svit (možná polojasno) → normální chování

### 🔥 Srovnání s ostatními faktory

| Faktor | Efekt | AAD range | Confidence |
|--------|-------|-----------|------------|
| **Sluneční svit** | Dlouhý svit → malé levné | **0.10-0.14** | 14-16% |
| **Teplota** (Q2) | Horko → malé levné | 0.11-0.15 | 10-17% |
| **Srážky** (Q3) | Déšť → větší střední | 0.10-0.24 | 15-47% |

**Srážky mají stále NEJSILNĚJŠÍ efekt!** (nejvyšší AAD a confidence)

### 🌤️ Zajímavé pozorování

**Moderate sunshine ≠ Long sunshine:**
- **Moderate** (4-6h) → větší dražší objednávky
- **Long** (6-8h) → malé levné objednávky

**Možné vysvětlení:** Střední sluneční svit = **proměnlivé počasí** → lidé zůstávají doma a objednávají normálně. Dlouhý svit = **stabilně krásně** → lidé venku.

### ⚠️ Limitace

- Pouze 8 pravidel = vzory nejsou velmi časté
- Confidence 14-16% = většina objednávek se neřídí pravidlem
- AAD 0.10-0.14 = střední síla vztahů
- Sluneční svit je korelován s teplotou → částečně redundantní informace

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Číselné sekvence:** Použity `sunshine_cat_seq` sloupce pro ordinální analýzu
- **Procesor:** 4ft-Miner

---

## Question 2: Vliv sekvencí teplot na velikost a cenu objednávek

### 🎯 Výzkumná otázka
**Existují ordinální vztahy mezi teplotními sekvencemi a parametry objednávek?**

Konkrétně: Ovlivňuje postupná změna teploty (např. freezing → very cold → cold) velikost nebo cenu objednávek?

### ⚙️ Konfigurace

**Soubor:** `Question2.py`

**Antecedent (příčina):**
- `mean_temp_cat_seq` - sekvence teplot (1-3 prvky)
- Typ: ordinální sekvence

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` - velikost objednávky (1-2 prvky)
- `Total_Price_cat_seq` - cena objednávky (1-2 prvky)
- Typ: ordinální sekvence

**Kvantifikátory:**
- Confidence: ≥ 0.1 (10%)
- Base: ≥ 100 objednávek
- AAD: ≥ 0.1 (významný rozdíl)

### 📊 Výsledky

**Celkově nalezeno:** 8 pravidel (z 1,681 ověření)

#### 🔥 Klíčová zjištění:

**1. Mrazivé počasí → větší objednávky**
```
mean_temp_cat(freezing, very cold) => Total_Products_cat(large) & Total_Price_cat(medium, medium-high)
Base: 315 | Confidence: 13.7% | AAD: +0.130
```
**Interpretace:** Při velmi chladném počasí (freezing NEBO very cold) lidé objednávají větší množství jídla za střední až vyšší ceny.

**2. Velmi teplé počasí → malé levné objednávky**
```
mean_temp_cat(very warm) => Total_Products_cat(tiny, small) & Total_Price_cat(very low)
Base: 230 | Confidence: 14.3% | AAD: +0.114
```
**Interpretace:** Při vysokých teplotách lidé objednávají malé a levné porce.

**3. Horko a velmi horko → velmi nízké ceny**
```
mean_temp_cat(very warm, hot) => Total_Price_cat(very low)
Base: 303 | Confidence: 17.0% | AAD: +0.142
```
**Interpretace:** Při extrémně horkém počasí (very warm NEBO hot) dominují velmi levné objednávky.

#### 📈 Trendy:

| Teplota | Velikost objednávek | Cena objednávek | AAD |
|---------|---------------------|-----------------|-----|
| Freezing/Very cold | Large | Medium-high | +0.13-0.15 |
| Very warm/Hot | Tiny/Small | Very low | +0.11-0.14 |

### 💡 Závěry

1. **Jasná inverzní korelace:** Teplota ↑ → Velikost objednávek ↓ a Cena ↓
2. **Strongest pattern:** Horké počasí → velmi nízké ceny (AAD +0.142)
3. **Business význam:** 
   - V zimě lidé objednávají více a dražší jídlo (možná více kalorií, rodinné objednávky)
   - V létě převažují malé levné svačinky (nižší chuť k jídlu v horku)
4. **Sekvence fungují:** CleverMiner úspěšně detekoval ordinální vztahy mezi teplotními kategoriemi

### ⚠️ Limitace

- Pouze 8 pravidel = vzory nejsou velmi časté
- AAD 0.10-0.15 = středně silné vztahy (ne extrémně silné)
- Confidence 10-17% = platí v menšině případů (ale s vysokým AAD = významné)

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Číselné sekvence:** Použity `*_cat_seq` sloupce pro ordinální analýzu
- **Procesor:** 4ft-Miner

---

## Question 3: Vliv srážek na velikost a cenu objednávek

### 🎯 Výzkumná otázka
**Ovlivňuje intenzita srážek (déšť) parametry objednávek?**

Konkrétně: Mění se chování zákazníků při různých úrovních deště (light, medium, strong)?

### ⚙️ Konfigurace

**Soubor:** `Question3.py`

**Antecedent (příčina):**
- `precipitation_cat_seq` - sekvence intenzity srážek (1-3 prvky)
- Typ: ordinální sekvence

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` - velikost objednávky (1-2 prvky)
- `Total_Price_cat_seq` - cena objednávky (1-2 prvky)
- Typ: ordinální sekvence

**Kvantifikátory:**
- Confidence: ≥ 0.1 (10%)
- Base: ≥ 100 objednávek
- AAD: ≥ 0.1 (významný rozdíl)

### 📊 Výsledky

**Celkově nalezeno:** 10 pravidel (z 1,089 ověření)

#### 🌧️ Klíčová zjištění:

**1. Střední déšť → střední ceny DOMINUJÍ**
```
precipitation_cat(medium) => Total_Price_cat(medium-low, medium)
Base: 367 | Confidence: 47.3% | AAD: +0.113
```
**Interpretace:** Při středním dešti **téměř polovina objednávek** má střední cenu (£25-40). To je **nejsilnější pravidlo** v celé analýze!

**2. Střední až silný déšť → větší objednávky se střední cenou**
```
precipitation_cat(medium, strong) => Total_Products_cat(large, very large) & Total_Price_cat(medium-low, medium)
Base: 126 | Confidence: 15.5% | AAD: +0.236
```
**Interpretace:** Při středním NEBO silném dešti lidé objednávají **výrazně větší množství** jídla za střední ceny. **Highest AAD (+0.236)** = nejsilnější vzor!

**3. Déšť zvyšuje cenu kolem £25-32**
```
precipitation_cat(medium) => Total_Price_cat(medium-low)
Base: 193 | Confidence: 24.9% | AAD: +0.130
```
**Interpretace:** Čtvrtina objednávek při dešti je v kategorii "medium-low" (£25-32).

#### 📈 Trendy:

| Intenzita srážek | Velikost objednávek | Cena objednávek | Confidence | AAD |
|------------------|---------------------|-----------------|------------|-----|
| Medium | Small-Medium | Medium-low | 19.8% | +0.12 |
| Medium | Large-Very large | Medium-low/Medium | 15.3% | +0.23 |
| Medium + Strong | Large-Very large | Medium-low/Medium | 15.5% | **+0.24** |

### 💡 Závěry

1. **Déšť = vyšší utrata:** Střední až silný déšť výrazně zvyšuje pravděpodobnost středních až vyšších cen
2. **Největší efekt:** Střední nebo silný déšť → větší objednávky (AAD +0.236)
3. **Confidence až 47%:** Střední déšť velmi spolehlivě predikuje střední ceny
4. **Business insight:** 
   - Lidé se při dešti "zásobují" (větší objednávky)
   - Ochota utratit více (rozvoz v dešti má hodnotu)
   - Možná rodinné objednávky místo chození ven

### 🔥 Srovnání s Question 2 (teplota)

| Faktor | Silnější efekt | AAD range |
|--------|----------------|-----------|
| **Teplota** | Horko → malé levné objednávky | 0.11-0.15 |
| **Srážky** | Déšť → větší střední objednávky | **0.10-0.24** |

**Srážky mají SILNĚJŠÍ efekt než teplota!** (vyšší AAD)

### ⚠️ Limitace

- Pouze 10 pravidel = specifické vzory
- Pravidla se zaměřují pouze na medium/strong déšť (light není zajímavý)
- Nejvyšší confidence 47% = stále polovina případů se neřídí pravidlem

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Číselné sekvence:** Použity `*_cat_seq` sloupce pro ordinální analýzu
- **Procesor:** 4ft-Miner

---

*Další otázky budou přidány podle potřeby analýzy.*

