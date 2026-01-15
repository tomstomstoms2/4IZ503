"""
🔄 Dekódování číselných kategorií z CleverMiner výstupu

Tento skript nahradí číselné kódy kategorií (_seq sloupce)
zpět na jejich textové podoby pro lepší čitelnost.

Použití:
1. Spusť CleverMiner dotaz a zkopíruj výstup
2. Ulož výstup do souboru (např. output.txt) NEBO
3. Vlož přímo do kódu níže do proměnné 'cleverminer_output'
"""

# ============================================================================
# MAPOVÁNÍ KATEGORIÍ (DECODE)
# ============================================================================

# Order metriky
TOTAL_PRICE_DECODE = {
    0: 'unknown',
    1: 'very low',
    2: 'low',
    3: 'medium-low',
    4: 'medium',
    5: 'medium-high',
    6: 'high',
    7: 'very high'
}

AVG_ITEM_PRICE_DECODE = {
    0: 'unknown',
    1: 'budget',
    2: 'economy',
    3: 'standard',
    4: 'premium',
    5: 'luxury'
}

TOTAL_PRODUCTS_DECODE = {
    0: 'unknown',
    1: 'tiny',
    2: 'small',
    3: 'medium',
    4: 'large',
    5: 'very large',
    6: 'huge'
}

AVG_ITEM_QUANTITY_DECODE = {
    0: 'unknown',
    1: 'single',
    2: 'mostly single',
    3: 'mixed',
    4: 'mostly double',
    5: 'bulk'
}

# Weather kategorie
CLOUD_COVER_DECODE = {
    0: 'unknown',
    1: 'clear',
    2: 'mostly clear',
    3: 'partly cloudy',
    4: 'mostly cloudy',
    5: 'overcast',
    6: 'sky obscured'
}

SUNSHINE_DECODE = {
    0: 'unknown',
    1: 'none',
    2: 'very short',
    3: 'short',
    4: 'moderate',
    5: 'long',
    6: 'very long'
}

GLOBAL_RADIATION_DECODE = {
    0: 'unknown',
    1: 'very low',
    2: 'low',
    3: 'moderate',
    4: 'high',
    5: 'very high',
    6: 'extreme'
}

MEAN_TEMP_DECODE = {
    0: 'unknown',
    1: 'hard freezing',
    2: 'freezing',
    3: 'very cold',
    4: 'cold',
    5: 'fresh',
    6: 'warm',
    7: 'very warm',
    8: 'hot'
}

PRECIPITATION_DECODE = {
    0: 'unknown',
    1: 'no rain',
    2: 'very light',
    3: 'light',
    4: 'medium',
    5: 'strong',
    6: 'very strong',
    7: 'extremely strong'
}

SNOW_DEPTH_DECODE = {
    0: 'unknown',
    1: 'none',
    2: 'trace',
    3: 'shallow',
    4: 'moderate',
    5: 'deep',
    6: 'very deep'
}

PRESSURE_DECODE = {
    0: 'unknown',
    1: 'extremely low',
    2: 'very low',
    3: 'low',
    4: 'normal',
    5: 'high',
    6: 'very high',
    7: 'extremely high'
}

# Day of Week (pandas dt.dayofweek: 0=Monday, 6=Sunday)
DAY_OF_WEEK_DECODE = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

# Spojení všech mapování
DECODE_MAPS = {
    'Total_Price_cat_seq': TOTAL_PRICE_DECODE,
    'Avg_Item_Price_cat_seq': AVG_ITEM_PRICE_DECODE,
    'Total_Products_cat_seq': TOTAL_PRODUCTS_DECODE,
    'Avg_Item_Quantity_cat_seq': AVG_ITEM_QUANTITY_DECODE,
    'cloud_cover_cat_seq': CLOUD_COVER_DECODE,
    'sunshine_cat_seq': SUNSHINE_DECODE,
    'global_radiation_cat_seq': GLOBAL_RADIATION_DECODE,
    'mean_temp_cat_seq': MEAN_TEMP_DECODE,
    'precipitation_cat_seq': PRECIPITATION_DECODE,
    'snow_depth_cat_seq': SNOW_DEPTH_DECODE,
    'pressure_cat_seq': PRESSURE_DECODE,
    'Day of Week Number': DAY_OF_WEEK_DECODE
}

# ============================================================================
# DEKÓDOVACÍ FUNKCE
# ============================================================================

import re

def decode_cleverminer_output(text):
    """
    Dekóduje CleverMiner výstup - nahradí číselné kódy textovými kategoriemi

    Args:
        text: Textový výstup z CleverMiner

    Returns:
        Dekódovaný text s textovými kategoriemi
    """
    decoded_text = text

    # Pro každý atribut s _seq
    for attr_name, decode_map in DECODE_MAPS.items():
        # Najdi všechny výskyty typu: attr_name(1), attr_name(2 3), atd.
        pattern = rf'{attr_name}\(([0-9\s]+)\)'

        def replace_codes(match):
            codes_str = match.group(1)
            codes = [int(c) for c in codes_str.split()]

            # Dekóduj všechny kódy
            decoded_values = []
            for code in codes:
                if code in decode_map:
                    decoded_values.append(decode_map[code])
                else:
                    decoded_values.append(f'?{code}?')  # Neznámý kód

            # Vrať dekódovaný string (odstraň _seq)
            attr_clean = attr_name.replace('_cat_seq', '_cat')
            return f'{attr_clean}({", ".join(decoded_values)})'

        decoded_text = re.sub(pattern, replace_codes, decoded_text)

    return decoded_text

# ============================================================================
# POUŽITÍ
# ============================================================================

if __name__ == "__main__":
    import sys

    print("="*70)
    print("🔄 DEKÓDOVÁNÍ CLEVERMINER VÝSTUPU")
    print("="*70)

    # Možnost 1: Čtení ze souboru
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print(f"\n📂 Čtu soubor: {input_file}")

        with open(input_file, 'r', encoding='utf-8') as f:
            cleverminer_output = f.read()

        decoded = decode_cleverminer_output(cleverminer_output)

        # Ulož dekódovaný výstup
        output_file = input_file.replace('.txt', '_decoded.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decoded)

        print(f"✅ Dekódovaný výstup uložen: {output_file}")
        print("\n" + "="*70)
        print("📄 DEKÓDOVANÝ VÝSTUP:")
        print("="*70)
        print(decoded)

    # Možnost 2: Přímé vložení textu
    else:
        print("\n⚠️  Použití:")
        print("   python DecodeCleverMinerOutput.py <soubor_s_výstupem.txt>")
        print("\n   NEBO upravte kód níže a vložte výstup přímo:")
        print("\n" + "="*70)

        # VLOŽ CLEVERMINER VÝSTUP SEM:
        cleverminer_output = """
        PŘÍKLAD:
        5103   109 0.333 +0.345 mean_temp_cat_seq(6) & precipitation_cat_seq(1 2) 
                                & Day of Week(Monday) => Total_Products_cat_seq(2)
        """

        if cleverminer_output.strip() and "PŘÍKLAD" not in cleverminer_output:
            decoded = decode_cleverminer_output(cleverminer_output)
            print("📄 DEKÓDOVANÝ VÝSTUP:")
            print("="*70)
            print(decoded)
        else:
            print("\n💡 TIP: Můžeš také použít funkci decode_cleverminer_output() ")
            print("   přímo ve svém kódu:")
            print("\n   from DecodeCleverMinerOutput import decode_cleverminer_output")
            print("   decoded = decode_cleverminer_output(your_text)")

