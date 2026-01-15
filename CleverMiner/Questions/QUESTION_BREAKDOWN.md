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
2. **Business význam:** 
   - V zimě lidé objednávají více a dražší jídlo (možná více kalorií, rodinné objednávky)
   - V létě převažují malé levné svačinky (nižší chuť k jídlu v horku)
3. **Sekvence fungují:** CleverMiner úspěšně detekoval ordinální vztahy mezi teplotními kategoriemi

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

- Pouze 10 pravidel = specifické vzory
- Pravidla se zaměřují pouze na medium/strong déšť (light není zajímavý)
- Nejvyšší confidence 47% = stále polovina případů se neřídí pravidlem

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

**Kvantifikátory (PŘÍSNĚJŠÍ):**
- Confidence: ≥ 0.3 (30%) ← vyšší než Q1-Q3
- Base: ≥ 100 objednávek
- AAD: ≥ 0.15 (silný efekt) ← vyšší než Q1-Q3

### 📊 Výsledky

**Celkově nalezeno:** 11 pravidel (z 7,990 ověření)

⚠️ **Pouze 11 pravidel = kombinace má VELMI specifické, ale SILNÉ efekty!**

#### 🔥 TOP pravidla (seřazeno podle AAD):

**1. 🌡️☀️ VERY WARM/HOT + LONG SUNSHINE → Tiny/Small objednávky**
```
mean_temp_cat(very warm, hot) & sunshine_cat(long) => Total_Products_cat(tiny, small)
Base: 106 | Confidence: 37.6% | AAD: +0.248 ⭐
```
**Interpretace:** Při **horkém počasí s dlouhým slunečním svitem** objednává **37.6% lidí malé porce** - o 24.8% víc než normálně!

**2. 🌡️☀️ VERY WARM/HOT + LONG SUNSHINE → Very low cena**
```
mean_temp_cat(very warm, hot) & sunshine_cat(long) => Total_Price_cat(very low, low)
Base: 101 | Confidence: 35.8% | AAD: +0.244
```
**Interpretace:** Při horku a slunci **dominují nejlevnější objednávky**.

**3. 🌡️☀️ VERY WARM + MODERATE/LONG SUNSHINE → Tiny/Small**
```
mean_temp_cat(very warm) & sunshine_cat(moderate, long) => Total_Products_cat(tiny, small)
Base: 163 | Confidence: 35.7% | AAD: +0.186
```

**4. 🌡️☀️ VERY WARM/HOT + MODERATE/LONG SUNSHINE → Very low cena**
```
mean_temp_cat(very warm, hot) & sunshine_cat(moderate, long) => Total_Price_cat(very low, low)
Base: 166 | Confidence: 34.7% | AAD: +0.203
```

**5. 🌡️☀️ FRESH + VERY LONG SUNSHINE → Very low/Low cena**
```
mean_temp_cat(fresh) & sunshine_cat(very long) => Total_Price_cat(very low, low)
Base: 329 | Confidence: 33.8% | AAD: +0.174
```
**Interpretace:** I při **mírné teplotě** s **velmi dlouhým sluncem** převažují levné objednávky.

#### 📈 Synergické efekty:

| Kombinace | Efekt | Confidence | AAD |
|-----------|-------|------------|-----|
| Very warm/hot + Long sun | Tiny/small | **37.6%** | **+0.248** 🔥 |
| Very warm + Moderate/long sun | Tiny/small | 35.7% | +0.186 |
| Fresh + Very long sun | Very low price | 33.8% | +0.174 |

### 💡 Závěry

1. **Synergický efekt existuje!** Kombinace teploty + slunce má **SILNĚJŠÍ** efekt než jednotlivé faktory:
   - Q1 (sunshine): AAD 0.10-0.14
   - Q2 (teplota): AAD 0.11-0.15
   - **Q4 (kombinace): AAD 0.15-0.25** ⭐

2. **Fresh temp + Very long sun:**
   - I při **mírné teplotě** dlouhý sluneční svit vede k levným objednávkám
   - Důležitější je **slunce** než teplota!

3. **Business insight:**
   - **Krásné počasí (horko+slunce) = dramatický pokles objednávek**
   - Confidence 35-38% = **více než třetina objednávek!**
   - Lidé jsou venku → neobjednávají nebo jen svačinky

### ⚠️ Limitace

- Pouze 11 pravidel = **velmi specifické vzory**
- Všechny se týkají **teplého/horkého počasí** s různým slunečním svitem
- Žádná pravidla pro **chladné počasí** se sluncem (nedostatečná podpora/efekt)
- Přísnější kvantifikátory (conf 0.3, aad 0.15) eliminovaly slabé vzory

### 🎯 Klíčové poznatky:

1. **Kombinace faktorů má silnější efekt než jednotlivé faktory**
2. **Sluneční svit je důležitější než samotná teplota** (fresh + long sun = levně)
3. **Krásné počasí (warm/hot + sun) = nejsilnější prediktor malých/levných objednávek**
4. **Synergický efekt až +25% nad baseline!**

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
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 100, AAD ≥ 0.5 (VELMI přísné!)

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
- **Pondělí a středa večer (20-22h)** → **více než polovina objednávek** je malých a levných
- **AAD +0.946** = extrémně silný efekt
- **94.6% nárůst** pravděpodobnosti malých levných objednávek oproti baseline

#### 📅 Analýza B: Sobotní odpoledne/večer (8 pravidel)

**Konzistentní vzor:**

```
Day of Week(Saturday) & Hour(16-19) => Medium/Large objednávky
Confidence: 58.8-59.9% | AAD: +0.106-0.126
```

**Všech 8 pravidel ukazuje stejné:**
- **Sobota 16:00-21:00** → **téměř 60% objednávek** je středních nebo velkých
- **Base 1,134-2,799** = velmi silná podpora (až 14% všech objednávek!)
- Konzistentní napříč různými časovými okny

### 💡 Závěry

1. **Extrémně silný efekt:**
   - Pondělí 20-22h má AAD +0.946 (94.6% nárůst pravděpodobnosti)
   - Téměř **95% nárůst** pravděpodobnosti malých/levných objednávek

2. **Dva jasné vzory:**
   - **Pondělí/Středa večer** → malé levné objednávky (lidé unavení po práci?)
   - **Sobota odpoledne/večer** → velké objednávky (rodinné večeře?)

3. **Časové okno je klíčové:**
   - **20-22h** (pozdní večer) = malé/levné
   - **16-20h** (sobotní večer) = velké/střední

4. **Business insight:**
   - **Sobota 17-19h** = **peak pro velké objednávky** (confidence 60%, base 2,799)
   - **Pondělí večer** = **peak pro malé svačinky** (confidence 56%, AAD +0.95)
   - Jasná segmentace zákazníků podle dne a času

### 📈 Klíčové časové vzory:

| Den | Čas | Efekt | Confidence | AAD |
|-----|-----|-------|------------|-----|
| **Monday** | 20-22h | Tiny/Small + Very low price | 56% | **+0.95** 🔥 |
| **Wednesday** | 20-21h | Tiny/Small + Very low price | 54% | +0.81 |
| **Saturday** | 17-19h | Medium/Large | **60%** | +0.12 |

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
**Kvantifikátory:** conf ≥ 0.5, Base ≥ 100, AAD ≥ 1.0 (EXTRÉMNĚ přísné!)

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
- **Dopoledne/poledne (10-12h) BEZ deště** → **více než polovina objednávek** je malých a levných
- **AAD +1.579** = extrémně silný efekt (158% nárůst pravděpodobnosti!)
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
- **Večer (20-22h) BEZ deště** → **65% objednávek** je malých nebo středních
- **Base 1,889** = 10% všech objednávek v datasetu!
- Velmi konzistentní napříč různými časovými okny

### 💡 Závěry

1. **Extrémní synergický efekt:**
   - Poledne + bez deště = AAD +1.579 (158% nárůst!)
   - Kombinace času a počasí má **dramatický** efekt

2. **Dva časové vzory:**
   - **Poledne (10-12h)** + sucho → tiny/small + very low price (confidence 55-63%)
   - **Večer (20-22h)** + sucho → small/medium (confidence 65%)

3. **Vliv srážek je kritický:**
   - Všechna pravidla vyžadují "no rain" nebo "very light"
   - Při dešti se chování **dramaticky mění**

4. **Business insight:**
   - **Poledne bez deště** = lidé venku → jen malé svačinky
   - **Večer bez deště** = stále menší objednávky (lidé nejsou doma?)
   - **Absence deště má větší efekt než přítomnost deště**

### 📈 Klíčové vzory:

| Čas | Počasí | Efekt | Confidence | AAD | Base |
|-----|--------|-------|------------|-----|------|
| **10-12h** | No rain | Tiny/Small + Very low | 55% | **+1.58** 🔥 | 100 |
| **10-12h** | No/Very light | Tiny/Small | 63% | +1.09 | 130 |
| **20-22h** | No/Very light | Small/Medium | **65%** | +0.13 | 1,889 |

### 🎯 Porovnání s Q5 (čas bez počasí):

**Q5:** Monday 20-22h → Tiny/Small (AAD +0.946)  
**Q6:** 20-22h + No rain → Small/Medium (AAD +0.133)

**Rozdíl:**
- Q5 se zaměřilo na **specifický den** (pondělí) → silnější efekt
- Q6 se zaměřuje na **obecný čas + počasí** → širší aplikovatelnost

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

*Další otázky budou přidány podle potřeby analýzy.*

