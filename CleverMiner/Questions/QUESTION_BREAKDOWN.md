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
4. **Business insight:** 
   - Při krásném počasí lidé **jdí ven** → méně objednávají
   - Pouze **rychlé svačinky** místo velkých obědů/večeří
   - Střední svit (možná polojasno) → normální chování

### 🌤️ Zajímavé pozorování

**Moderate sunshine ≠ Long sunshine:**
- **Moderate** (4-6h) → větší dražší objednávky
- **Long** (6-8h) → malé levné objednávky

**Možné vysvětlení:** Střední sluneční svit = **proměnlivé počasí** → lidé zůstávají doma a objednávají normálně. Dlouhý svit = **stabilně krásně** → lidé venku.

### ⚠️ Limitace

- Detekováno pouze 8 pravidel z 1,581 ověření
- Nízká confidence (14-16%) indikuje omezenou aplikovatelnost
- AAD 0.10-0.14 představuje středně silné vztahy
- Možná korelace se sloupcem mean_temp_cat

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
2. **Business význam:** 
   - V zimě lidé objednávají více a dražší jídlo (možná více kalorií, rodinné objednávky)
   - V létě převažují malé levné svačinky (nižší chuť k jídlu v horku)
3. **Sekvence fungují:** CleverMiner úspěšně detekoval ordinální vztahy mezi teplotními kategoriemi

### ⚠️ Limitace

- Pouze 8 pravidel detekováno
- AAD 0.10-0.15 indikuje středně silné vztahy
- Confidence 10-17% znamená, že pravidla platí v menšině případů

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
**Interpretace:** Při středním dešti **téměř polovina objednávek** má střední cenu (£25-40).

**2. Střední až silný déšť → větší objednávky se střední cenou**
```
precipitation_cat(medium, strong) => Total_Products_cat(large, very large) & Total_Price_cat(medium-low, medium)
Base: 126 | Confidence: 15.5% | AAD: +0.236
```
**Interpretace:** Při středním NEBO silném dešti lidé objednávají **výrazně větší množství** jídla za střední ceny.

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

### ⚠️ Limitace

- Detekováno 10 pravidel z 1,089 ověření
- Pravidla se zaměřují primárně na střední a silný déšť
- Maximální confidence 47.3% - 52.7% případů nevysvětleno

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Číselné sekvence:** Použity `*_cat_seq` sloupce pro ordinální analýzu
- **Procesor:** 4ft-Miner

---

## Question 4: Kombinovaný vliv teploty a slunečního svitu

### 🎯 Výzkumná otázka
**Jaký je synergický efekt kombinace teploty a slunečního svitu na objednávky?**

Konkrétně: Zesilují se vzájemně efekty teploty a slunce? Jsou některé kombinace obzvlášť silné?

### ⚙️ Konfigurace

**Soubor:** `Question4.py`

**Antecedent (příčina):**
- `mean_temp_cat_seq` - teplota (1-2 prvky) **+**
- `sunshine_cat_seq` - sluneční svit (1-2 prvky)
- **Kombinace obou faktorů!**
- Celkově: min 1, max 3 prvky v antecedentu

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` - velikost objednávky (1-2 prvky)
- `Total_Price_cat_seq` - cena objednávky (1-2 prvky)
- Celkově: min 1, max 2 prvky v sukcedentu

**Kvantifikátory:**
- Confidence: ≥ 0.3
- Base: ≥ 100
- AAD: ≥ 0.15

### 📊 Výsledky

**Celkově nalezeno:** 11 pravidel (z 7,990 ověření)


#### 🔥 TOP pravidla (seřazeno podle AAD):

**1. VERY WARM/HOT + LONG SUNSHINE → Tiny/Small objednávky**
```
mean_temp_cat(very warm, hot) & sunshine_cat(long) => Total_Products_cat(tiny, small)
Base: 106 | Confidence: 37.6% | AAD: +0.248
```
**Interpretace:** Při horkém počasí s dlouhým slunečním svitem objednává 37.6% zákazníků malé porce.

**2. VERY WARM/HOT + LONG SUNSHINE → Very low cena**
```
mean_temp_cat(very warm, hot) & sunshine_cat(long) => Total_Price_cat(very low, low)
Base: 101 | Confidence: 35.8% | AAD: +0.244
```
**Interpretace:** Při horku a slunci dominují nejlevnější objednávky.

**3. VERY WARM + MODERATE/LONG SUNSHINE → Tiny/Small**
```
mean_temp_cat(very warm) & sunshine_cat(moderate, long) => Total_Products_cat(tiny, small)
Base: 163 | Confidence: 35.7% | AAD: +0.186
```

**4. VERY WARM/HOT + MODERATE/LONG SUNSHINE → Very low cena**
```
mean_temp_cat(very warm, hot) & sunshine_cat(moderate, long) => Total_Price_cat(very low, low)
Base: 166 | Confidence: 34.7% | AAD: +0.203
```

**5. FRESH + VERY LONG SUNSHINE → Very low/Low cena**
```
mean_temp_cat(fresh) & sunshine_cat(very long) => Total_Price_cat(very low, low)
Base: 329 | Confidence: 33.8% | AAD: +0.174
```
**Interpretace:** I při mírné teplotě s velmi dlouhým sluncem převažují levné objednávky.

#### 📈 Synergické efekty:

| Kombinace | Efekt | Confidence | AAD |
|-----------|-------|------------|-----|
| Very warm/hot + Long sun | Tiny/small | 37.6% | +0.248 |
| Very warm + Moderate/long sun | Tiny/small | 35.7% | +0.186 |
| Fresh + Very long sun | Very low price | 33.8% | +0.174 |

### 💡 Závěry

1. **Synergický efekt kombinace faktorů:** Kombinace teploty a slunečního svitu vykazuje silnější efekt (AAD 0.15-0.25) než jednotlivé faktory samostatně (AAD 0.10-0.15).

2. **Dominance slunečního svitu:** I při mírné teplotě (fresh) vede dlouhý sluneční svit k levným objednávkám, což naznačuje významnější roli slunečního svitu než teploty.

3. **Business aplikace:**
   - Kombinace horkého počasí a dlouhého slunečního svitu predikuje malé a levné objednávky
   - Více než třetina objednávek (35-38% confidence) odpovídá těmto vzorům
   - Pravděpodobný důvod: Zákazníci venku, preferují malé svačinky

### ⚠️ Limitace

- Detekováno pouze 11 pravidel z 7,990 ověření
- Pravidla se koncentrují výhradně na teplé/horké počasí s různým slunečním svitem
- Absence pravidel pro chladné počasí se sluncem (nedostatečná podpora při aplikovaných kvantifikátorech)
- Vyšší prahové hodnoty (conf 0.3, AAD 0.15) eliminovaly slabší asociace

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Číselné sekvence:** Použity `*_cat_seq` sloupce pro ordinální analýzu
- **Procesor:** 4ft-Miner
- **Ověření:** 7,990 kombinací testováno

---

## Question 5: Vliv dne v týdnu a hodiny na objednávky

### 🎯 Výzkumná otázka
**Existují specifické časové vzory v objednávkách podle dne v týdnu a hodiny?**

Konkrétně: Objednávají lidé jinak v různé dny týdne a časy?

### ⚙️ Konfigurace

**Soubor:** `Question5.py`

**Dvě samostatné analýzy:**

#### Analýza A: Extrémy (velmi levné a malé objednávky)
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 100, AAD ≥ 0.5

**Antecedent:**
- `Day of Week Number` (0=Monday, 6=Sunday)
- `Hour` (hodina objednávky)

**Sukcedent:**
- `Total_Products_cat_seq` = tiny, small
- `Total_Price_cat_seq` = very low, low

#### Analýza B: Střední/velké objednávky
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 1000, AAD ≥ 0.1

**Antecedent:**
- `Day of Week Number`
- `Hour` (3 hodiny v sekvenci)

**Sukcedent:**
- `Total_Products_cat_seq` = medium, large

### 📊 Výsledky

#### 🌙 Analýza A: Večerní extrémy (7 pravidel)

**TOP zjištění - Pondělí a středa večer:**

```
Day of Week(Monday) & Hour(20-22) => Tiny/Small & Very low/Low price
Base: 176 | Confidence: 56.1% | AAD: +0.946 ⭐⭐⭐
```

```
Day of Week(Wednesday) & Hour(20-21) => Tiny/Small
Base: 186 | Confidence: 54.5% | AAD: +0.810
```

**Interpretace:** 
- Pondělí a středa večer (20-22h): více než polovina objednávek je malých a levných
- AAD +0.946 představuje extrémně silný efekt
- 94.6% nárůst pravděpodobnosti malých levných objednávek oproti baseline

#### 📅 Analýza B: Sobotní odpoledne/večer (8 pravidel)

**Konzistentní vzor:**

```
Day of Week(Saturday) & Hour(16-19) => Medium/Large objednávky
Confidence: 58.8-59.9% | AAD: +0.106-0.126
```

**Všech 8 pravidel ukazuje stejné:**
- Sobota 16:00-21:00: téměř 60% objednávek je středních nebo velkých
- Base 1,134-2,799 představuje silnou podporu (až 14% všech objednávek)
- Konzistentní napříč různými časovými okny

### 💡 Závěry

1. **Extrémně silný efekt:**
   - Pondělí 20-22h vykazuje AAD +0.946, což představuje 94.6% nárůst pravděpodobnosti malých a levných objednávek

2. **Dva identifikované vzory:**
   - Pondělí a středa večer: malé levné objednávky
   - Sobota odpoledne a večer: velké objednávky

3. **Časová závislost:**
   - 20-22h: preference malých a levných objednávek
   - 16-20h (sobota): preference středních a velkých objednávek

4. **Praktické implikace:**
   - Sobota 17-19h představuje peak pro velké objednávky (confidence 60%, base 2,799)
   - Pondělí večer vykazuje koncentraci malých objednávek (confidence 56%, AAD +0.95)
   - Jasná segmentace zákazníků podle dne a času

### 📈 Klíčové časové vzory:

| Den | Čas | Efekt | Confidence | AAD |
|-----|-----|-------|------------|-----|
| Monday | 20-22h | Tiny/Small + Very low price | 56% | +0.95 |
| Wednesday | 20-21h | Tiny/Small + Very low price | 54% | +0.81 |
| Saturday | 17-19h | Medium/Large | 60% | +0.12 |

### 🎯 Praktické využití:

1. **Optimalizace skladových zásob:**
   - Sobota večer → připravit více surovin
   - Pondělí večer → menší porce, nižší ceny

2. **Dynamické ceny:**
   - Sobota 17-19h → premium pricing (velké objednávky)
   - Pondělí večer → akce na malé porce

3. **Personál:**
   - Sobota odpoledne/večer → více kuchařů (velké objednávky)

### ⚠️ Limitace

- Pouze specifické dny/časy nalezeny (ne všechny kombinace)
- Pondělí/Středa večer = malá absolútní čísla (Base 146-210)
- Sobota = velká podpora, ale nižší AAD

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Dvě analýzy:** Extrémy (conf 0.5, aad 0.5) + Střední (conf 0.5, base 1000)
- **Procesor:** 4ft-Miner (2× spuštěno)

---

## Question 6: Vliv kombinace hodiny a srážek na objednávky

### 🎯 Výzkumná otázka
**Jaký je synergický efekt času a počasí (srážek) na objednávky?**

Konkrétně: Mění se efekt srážek v různou denní dobu?

### ⚙️ Konfigurace

**Soubor:** `Question6.py`

**Dvě samostatné analýzy:**

#### Analýza A: Extrémy (velmi malé a levné objednávky)
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 100, AAD ≥ 1.0

**Antecedent:**
- `Hour` (hodina objednávky, 1-3 prvky)
- `precipitation_cat_seq` (srážky, 1-2 prvky)
- Celkově: min 2, max 5 prvků

**Sukcedent:**
- `Total_Products_cat_seq` = tiny, small
- `Total_Price_cat_seq` = very low, low

#### Analýza B: Běžné objednávky
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 1000, AAD ≥ 0.1

**Antecedent:**
- `Hour` (hodina, 1-3 prvky)
- `precipitation_cat_seq` (srážky, 1-2 prvky)
- Celkově: min 2, max 5 prvků

**Sukcedent:**
- `Total_Products_cat_seq` = small, medium
- `Total_Price_cat_seq`

### 📊 Výsledky

#### 🌅 Analýza A: Polední extrémy (8 pravidel)

**Jasný vzor - Poledne bez deště:**

```
Hour(10-12) & precipitation(no rain) => Tiny/Small & Very low/Low price
Base: 100 | Confidence: 55.2% | AAD: +1.579 🔥
```

```
Hour(10-12) & precipitation(no rain, very light) => Tiny/Small
Base: 130 | Confidence: 62.8% | AAD: +1.085
```

**Interpretace:**
- Dopoledne/poledne (10-12h) bez deště: více než polovina objednávek je malých a levných
- AAD +1.579 představuje extrémně silný efekt (158% nárůst pravděpodobnosti)
- Vzor platí i s velmi mírným deštěm (very light)

#### 🌙 Analýza B: Večerní objednávky (5 pravidel)

**Konzistentní vzor - Večer bez deště:**

```
Hour(20-22) & precipitation(no rain, very light) => Small/Medium
Base: 1,889 | Confidence: 65.4% | AAD: +0.133
```

```
Hour(20-21) & precipitation(no rain) => Small/Medium
Base: 1,359 | Confidence: 65.3% | AAD: +0.130
```

**Interpretace:**
- Večer (20-22h) bez deště: 65% objednávek je malých nebo středních
- Base 1,889 představuje 10% všech objednávek v datasetu
- Konzistentní napříč různými časovými okny

### 💡 Závěry

1. **Extrémní synergický efekt:**
   - Poledne + absence srážek vykazuje AAD +1.579 (158% nárůst)
   - Kombinace času a počasí má dramatický efekt

2. **Dva časové vzory:**
   - Poledne (10-12h) + sucho: tiny/small + very low price (confidence 55-63%)
   - Večer (20-22h) + sucho: small/medium (confidence 65%)

3. **Vliv srážek:**
   - Všechna pravidla vyžadují no rain nebo very light rain
   - Při výraznějších srážkách se chování významně mění

4. **Praktické aplikace:**
   - Poledne bez deště: zákazníci pravděpodobně venku, preference malých objednávek
   - Večer bez deště: stále převaha menších objednávek
   - Absence deště má silnější prediktivní hodnotu než přítomnost srážek

### 📈 Klíčové vzory:

| Čas | Počasí | Efekt | Confidence | AAD | Base |
|-----|--------|-------|------------|-----|------|
| 10-12h | No rain | Tiny/Small + Very low | 55% | +1.58 | 100 |
| 10-12h | No/Very light | Tiny/Small | 63% | +1.09 | 130 |
| 20-22h | No/Very light | Small/Medium | 65% | +0.13 | 1,889 |

### ⚠️ Limitace

- Analýza A: Malá podpora (Base 100-130) = specifický vzor
- Všechna pravidla pouze pro "no rain" nebo "very light" rain
- Chybí pravidla pro silný déšť (nedostatečná podpora/efekt s conf 0.5)

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Dvě analýzy:** Extrémy (aad 1.0) + Běžné (base 1000)
- **Procesor:** 4ft-Miner (2× spuštěno)
- **Ověření:** 7,760 + 677 kombinací

---

## Question 7: Vliv silného deště v kombinaci s časem

### 🎯 Výzkumná otázka
**Jak se projevuje silný déšť v různou denní dobu a jak se liší chování při dešti oproti suchu?**

Konkrétně: 
- Komplement Question 6: zaměření na výraznější srážky (medium, strong) namísto absence deště
- Využití SD4ft-Miner: přímé porovnání pravděpodobností při dešti vs bez deště

### ⚙️ Konfigurace

**Soubor:** `Question7.py`

**Dvě analýzy:**

#### Analýza A: 4ft-Miner (základní asociační pravidla)

**Antecedent (příčina):**
- `Hour` (hodina objednávky, 1-3 prvky)
- `precipitation_cat_seq` (srážky, 1-2 prvky, typ: rcut)
- Celkově: min 2, max 6 prvky

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` (velikost objednávky, 1-2 prvky)
- `Total_Price_cat_seq` (cena objednávky, 1-2 prvky)
- Celkově: min 1, max 2 prvky

**Kvantifikátory:**
- Confidence: ≥ 0.3
- Base: ≥ 100
- AAD: ≥ 0.2

#### Analýza B: SD4ft-Miner (porovnání podmínek)

**Antecedent:** `Hour` (1-3 prvky)

**Sukcedent:** 
- `Total_Products_cat_seq` (1-2 prvky)
- `Total_Price_cat_seq` (1-2 prvky)

**First set (podmínka 1):** `precipitation_cat_seq` (rcut, 1-2 prvky) = medium/strong rain

**Second set (podmínka 2):** `precipitation_cat_seq` (lcut, 1-2 prvky) = no rain/very light rain

**Kvantifikátory:**
- RatioConf: ≥ 1.1
- Base1: ≥ 200
- Base2: ≥ 2,000

### 📊 Výsledky

#### Analýza A: 4ft-Miner (základní asociační pravidla)

**Celkově nalezeno:** 4 pravidla (z 125 ověření)

##### 🌧️ Večerní silný déšť:

**1. Odpolední/večerní hodiny + silný déšť → střední ceny**
```
Hour(17-18) & precipitation(strong, medium) => Total_Price_cat(medium, medium-high)
Base: 165 | Confidence: 41.6% | AAD: +0.203
```
**Interpretace:** V odpoledních hodinách při silném nebo středním dešti 41.6% objednávek spadá do střední až vyšší cenové kategorie (£32-50).

**2. 18h + silný déšť → velké objednávky**
```
Hour(18) & precipitation(strong, medium) => Total_Products_cat(large, very large)
Base: 104 | Confidence: 43.9% | AAD: +0.320
```
**Interpretace:** V 18 hodin při výrazných srážkách 43.9% objednávek obsahuje velké množství položek. AAD +0.320 představuje silný efekt (32% nárůst pravděpodobnosti).

**3. 18h + silný déšť → střední ceny**
```
Hour(18) & precipitation(strong, medium) => Total_Price_cat(medium, medium-high)
Base: 100 | Confidence: 42.2% | AAD: +0.221
```

**4. Večer 18-19h + silný déšť → velké objednávky**
```
Hour(18-19) & precipitation(strong, medium) => Total_Products_cat(large, very large)
Base: 175 | Confidence: 40.0% | AAD: +0.205
```

#### Analýza B: SD4ft-Miner (porovnání chování při různých srážkách)

**Celkově nalezeno:** 10 pravidel (z 652 ověření)

**Procedura:** SD4ft-Miner hledá změny v pravděpodobnosti (confidence) mezi dvěma podmínkami (frst vs scnd).

**Porovnání:**
- **First set:** precipitation_cat(strong, medium) - silný nebo střední déšť
- **Second set:** precipitation_cat(no rain) nebo precipitation_cat(no rain, very light) - bez deště nebo velmi slabý

##### TOP pravidla (podle RatioConf):

**1. Nejvyšší relativní změna confidence:**
```
Hour(18-19) => Total_Price_cat(medium-low, medium) | strong/medium rain vs no rain
Base1: 214 | Base2: 2,431 | RatioConf: 1.168 | DeltaConf: +0.070
```
**Interpretace:** V 18-19h je pravděpodobnost středních cen při silném dešti 16.8% vyšší než bez deště.

**2. Odpolední hodiny - změna cen:**
```
Hour(17-18-19) => Total_Price_cat(medium-low, medium) | strong/medium rain vs no rain
Base1: 296 | Base2: 3,324 | RatioConf: 1.152 | DeltaConf: +0.065
```

**3. Kombinace velikosti a ceny:**
```
Hour(17-18-19) => Total_Products_cat(medium, large) & Total_Price_cat(medium-low, medium) | strong/medium rain vs no rain
Base1: 216 | Base2: 2,520 | RatioConf: 1.108 | DeltaConf: +0.035
```

##### Klíčové poznatky z SD4ft-Miner:

| Pravidlo | Čas | RatioConf | DeltaConf | Base1 | Base2 |
|----------|-----|-----------|-----------|-------|-------|
| 1 | 18-19h | 1.168 | +0.070 | 214 | 2,431 |
| 2 | 17-18-19h | 1.152 | +0.065 | 296 | 3,324 |
| 3 | 16-17-18h | 1.145 | +0.063 | 214 | 2,342 |

**Interpretace SD4ft výsledků:**
- **RatioConf 1.10-1.17:** Při silném dešti je pravděpodobnost středních cen 10-17% vyšší než bez deště
- **Všechna pravidla:** Odpolední/večerní hodiny (16-20h)
- **Konzistentní pattern:** Silný déšť zvyšuje pravděpodobnost středních cen oproti absenci deště

### 💡 Závěry

1. **Opačný vzor k Question 6 (potvrzeno oběma analýzami):**
   - Q6 (absence deště): tiny/small objednávky
   - Q7 (silný déšť): large/very large objednávky
   - SD4ft-Miner kvantifikoval rozdíl: 10-17% vyšší pravděpodobnost středních cen při dešti

2. **Časová koncentrace:**
   - 4ft-Miner: Všechna 4 pravidla se týkají 17-19h
   - SD4ft-Miner: Všech 10 pravidel se týká 16-20h
   - Nejsilnější efekt v 18-19h

3. **Efekt silného deště:**
   - 4ft-Miner: Confidence 40-44%, AAD 0.20-0.32
   - SD4ft-Miner: RatioConf 1.10-1.17 (10-17% relativní nárůst)
   - Obě analýzy ukazují silný a konzistentní efekt

4. **SD4ft-Miner přidaná hodnota:**
   - Umožňuje přímé porovnání chování při dešti vs bez deště
   - Kvantifikuje relativní změnu pravděpodobnosti (RatioConf)
   - Base2 (bez deště) 2,000-4,000 poskytuje robustní baseline

5. **Praktické implikace:**
   - Silný déšť v 18h výrazně zvyšuje pravděpodobnost velkých objednávek
   - Střední až vyšší cenové kategorie dominují
   - Relativní nárůst 10-17% oproti běžnému stavu bez deště

### 📈 Klíčové vzory:

#### 4ft-Miner (asociační pravidla):

| Čas | Počasí | Efekt | Confidence | AAD | Base |
|-----|--------|-------|------------|-----|------|
| 18h | Medium/Strong | Large/Very large | 43.9% | +0.320 | 104 |
| 18-19h | Medium/Strong | Large/Very large | 40.0% | +0.205 | 175 |
| 17-18h | Medium/Strong | Medium/Medium-high price | 41.6% | +0.203 | 165 |
| 18h | Medium/Strong | Medium/Medium-high price | 42.2% | +0.221 | 100 |

#### SD4ft-Miner (porovnání déšť vs bez deště):

| Čas | Efekt | RatioConf | DeltaConf | Base1 (déšť) | Base2 (bez deště) |
|-----|-------|-----------|-----------|--------------|-------------------|
| 18-19h | Medium-low/Medium price | 1.168 | +0.070 | 214 | 2,431 |
| 17-18-19h | Medium-low/Medium price | 1.152 | +0.065 | 296 | 3,324 |
| 16-17-18h | Medium-low/Medium price | 1.145 | +0.063 | 214 | 2,342 |

### ⚠️ Limitace

#### 4ft-Miner:
- Pouze 4 pravidla z 125 ověření
- Všechna pravidla koncentrována v úzkém časovém okně (17-19h)
- Nižší Base (100-175)

#### SD4ft-Miner:
- 10 pravidel z 652 ověření
- Širší časové pokrytí (16-20h)
- Vyšší Base2 (2,000-4,000) pro baseline bez deště poskytuje robustní srovnání
- Absence pravidel pro jiné denní doby

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Procedury:** 
  - 4ft-Miner: Základní asociační pravidla
  - SD4ft-Miner: Porovnání pravděpodobností mezi podmínkami
- **SD4ft-Miner kvantifikátory:**
  - RatioConf: ≥ 1.1 (minimálně 10% relativní změna)
  - Base1: ≥ 200 (silný/střední déšť)
  - Base2: ≥ 2,000 (bez deště/velmi slabý déšť)
- **Typ atributu:** precipitation_cat_seq použit jako 'rcut' (4ft) a 'rcut'/'lcut' (SD4ft)
- **Ověření:** 125 (4ft) + 652 (SD4ft) kombinací

---

## Question 8: Kombinovaný vliv hodiny a teploty na objednávky

### 🎯 Výzkumná otázka
**Jak interaguje čas objednávky s teplotou a jak se tato kombinace projevuje v chování zákazníků?**

Konkrétně:
- Existují časové vzory ovlivněné teplotou?
- Jak se liší efekt teploty v různou denní dobu?

### ⚙️ Konfigurace

**Soubor:** `Question8.py`

**Dvě analýzy:**

#### Analýza A: 4ft-Miner (základní asociační pravidla)

**Antecedent (příčina):**
- `Hour` (hodina objednávky, 1-3 prvky, seq)
- `mean_temp_cat_seq` (teplota, 1-2 prvky, seq)
- Celkově: min 2, max 5 prvků

**Sukcedent (důsledek):**
- `Total_Products_cat_seq` (velikost objednávky, 1-2 prvky)
- `Total_Price_cat_seq` (cena objednávky, 1-2 prvky)
- Celkově: min 1, max 2 prvky

**Kvantifikátory:**
- Confidence: ≥ 0.6
- Base: ≥ 100
- AAD: ≥ 1.0

#### Analýza B: SD4ft-Miner (porovnání teplotních podmínek)

**Antecedent:** `Hour` (1-3 prvky, seq)

**Sukcedent:**
- `Total_Products_cat_seq` (1-2 prvky) &
- `Total_Price_cat_seq` (1-2 prvky)

**First set:** `mean_temp_cat_seq` (1-2 prvky) - jedna teplotní kategorie

**Second set:** `mean_temp_cat_seq` (1-2 prvky) - jiná teplotní kategorie

**Kvantifikátory:**
- RatioConf: ≥ 1.4 (minimálně 40% relativní změna)
- Base1: ≥ 100
- Base2: ≥ 200

### 📊 Výsledky

#### Analýza A: 4ft-Miner (základní asociační pravidla)

**Celkově nalezeno:** 7 pravidel (z 10,852 ověření)

##### 🌡️ Mírné teploty v poledních hodinách:

**1. Poledne + mírné teploty → malé objednávky**
```
Hour(10-11-12) & mean_temp_cat(fresh, warm) => Total_Products_cat(tiny, small)
Base: 105 | Confidence: 66.0% | AAD: +1.192
```
**Interpretace:** V poledních hodinách (10-12h) při mírných teplotách (fresh/warm, 10-20°C) 66% objednávek je malých (1-3 položky). AAD +1.192 představuje velmi silný efekt.

**2. Odpolední hodiny + teplé počasí → malé objednávky**
```
Hour(12-13-14) & mean_temp_cat(warm, very warm) => Total_Products_cat(tiny, small)
Base: 100 | Confidence: 62.5% | AAD: +1.074
```

**3. Nejvyšší confidence:**
```
Hour(11-12-13) & mean_temp_cat(fresh, warm) => Total_Products_cat(tiny, small)
Base: 150 | Confidence: 62.0% | AAD: +1.057
```

**Všechna 7 pravidel:**
- Týkají se **polední a odpolední doby** (10-15h)
- Všechna ukazují na **tiny/small** objednávky
- Všechna vyžadují **fresh/warm/very warm** teploty
- Confidence: 60.3-66.0%
- AAD: +1.01 až +1.19 (velmi silný efekt)

#### Analýza B: SD4ft-Miner (porovnání teplotních podmínek)

**Celkově nalezeno:** 15 pravidel (z 257,049 ověření)

**Procedura:** Porovnání pravděpodobností při různých teplotách.

##### TOP pravidla (podle RatioConf):

**1. Nejvyšší relativní změna:**
```
Hour(15-16-17) => Total_Products_cat(tiny, small) & Total_Price_cat(very low)
warm vs cold/fresh
Base1: 144 | Base2: 222 | RatioConf: 1.483 | DeltaConf: +0.043
```
**Interpretace:** V odpoledních hodinách (15-17h) je při teplém počasí pravděpodobnost malých levných objednávek o 48.3% vyšší než při chladném/mírném počasí.

**2. Velmi teplé počasí vs chladné:**
```
Hour(17-18-19) => Total_Products_cat(large) & Total_Price_cat(medium)
freezing/very cold vs cold
Base1: 138 | Base2: 219 | RatioConf: 1.455 | DeltaConf: +0.027
```
**Interpretace:** V 17-19h je při extrémně chladném počasí pravděpodobnost velkých středně drahých objednávek o 45.5% vyšší než při běžném chladném počasí.

**3. Odpolední teplo vs chlad:**
```
Hour(15-16-17) => Total_Price_cat(very low)
warm vs cold/fresh
Base1: 163 | Base2: 254 | RatioConf: 1.467 | DeltaConf: +0.048
```

##### Dva opačné vzory identifikované SD4ft-Miner:

**Vzor A: Teplé počasí (15-17h) → malé levné objednávky**
- 6 pravidel s RatioConf 1.42-1.48
- Teplé/velmi teplé počasí vs chladné/mírné
- Efekt: tiny/small + very low price

**Vzor B: Velmi chladné počasí (17-19h) → velké střední objednávky**
- 4 pravidla s RatioConf 1.41-1.46
- Freezing/very cold vs cold/fresh/warm
- Efekt: large + medium price

### 💡 Závěry

1. **Velmi silný synergický efekt:**
   - 4ft-Miner: AAD +1.0 až +1.2 (100-120% nárůst pravděpodobnosti)
   - SD4ft-Miner: RatioConf 1.4-1.5 (40-50% relativní změna)
   - Kombinace času a teploty má dramatický dopad

2. **Dva protichůdné vzory:**
   - **Poledne/odpoledne + teplo** (10-17h, fresh/warm/very warm):
     - tiny/small objednávky
     - very low ceny
     - Confidence 60-66% (4ft-Miner)
   
   - **Večer + extrémní chlad** (17-19h, freezing/very cold):
     - large objednávky
     - medium ceny
     - RatioConf 1.4-1.5 (SD4ft-Miner)

3. **Časová závislost teploty:**
   - Teplé počasí má největší efekt v odpoledních hodinách (15-17h)
   - Chladné počasí nejvíce ovlivňuje večerní hodiny (17-19h)
   - Poledne (10-13h) stabilně generuje malé objednávky při mírných teplotách

4. **Praktické aplikace:**
   - Teplý den 15-17h: příprava malých levných položek
   - Velmi chladný večer 17-19h: příprava větších porcí
   - Confidence 60-66% umožňuje robustní predikci

### 📈 Klíčové vzory:

#### 4ft-Miner (asociační pravidla):

| Čas | Teplota | Efekt | Confidence | AAD | Base |
|-----|---------|-------|------------|-----|------|
| 10-11-12h | Fresh/Warm | Tiny/Small | 66.0% | +1.192 | 105 |
| 11-12-13h | Fresh/Warm | Tiny/Small | 62.0% | +1.057 | 150 |
| 12-13-14h | Warm/Very warm | Tiny/Small | 62.5% | +1.074 | 100 |

#### SD4ft-Miner (porovnání teplot):

| Čas | Porovnání | Efekt | RatioConf | DeltaConf | Base1/Base2 |
|-----|-----------|-------|-----------|-----------|-------------|
| 15-16-17h | Warm vs Cold/Fresh | Tiny/Small + Very low | 1.483 | +0.043 | 144/222 |
| 15-16-17h | Warm vs Cold/Fresh | Very low price | 1.467 | +0.048 | 163/254 |
| 17-18-19h | Freezing/Very cold vs Cold | Large + Medium | 1.455 | +0.027 | 138/219 |
| 16-17-18h | Very warm vs Very cold/Cold | Very low price | 1.457 | +0.045 | 105/381 |

### 🎯 Praktické využití:

1. **Predikce poptávky:**
   - Teplý odpolední den → malé levné položky (66% confidence)
   - Velmi chladný večer → velké porce (45% vyšší pravděpodobnost)

2. **Optimalizace nabídky:**
   - 10-15h + teplo: svačinky, rychlé malé porce
   - 17-19h + mráz: plnohodnotná jídla, rodinné balíčky

3. **Dynamické ceny:**
   - Teplé odpoledne: akce na malé porce
   - Mrazivý večer: premium pricing na velké objednávky

### ⚠️ Limitace

#### 4ft-Miner:
- Pouze 7 pravidel z 10,852 ověření
- Všechna pravidla koncentrována na poledne/odpoledne
- Absence pravidel pro večerní/ranní hodiny s mírným počasím

#### SD4ft-Miner:
- 15 pravidel z 257,049 ověření (0.006% úspěšnost)
- Vysoké kvantifikátory (RatioConf ≥ 1.4) eliminovaly slabší vztahy
- Base1 často nižší (100-200)

### 🔄 Technické detaily

- **Dataset:** `datasetAnalyzed.csv` (19,311 objednávek)
- **Dekódování:** Automatické pomocí `DecodeCleverMinerOutput.py`
- **Procedury:**
  - 4ft-Miner: Základní asociační pravidla (přísné kvantifikátory)
  - SD4ft-Miner: Porovnání pravděpodobností mezi teplotami
- **4ft-Miner kvantifikátory:** conf ≥ 0.6, Base ≥ 100, AAD ≥ 1.0
- **SD4ft-Miner kvantifikátory:** RatioConf ≥ 1.4, Base1 ≥ 100, Base2 ≥ 200
- **Ověření:** 10,852 (4ft) + 257,049 (SD4ft) kombinací

---

*Další otázky budou přidány podle potřeby analýzy.*
