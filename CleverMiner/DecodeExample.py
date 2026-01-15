"""
📖 UKÁZKA POUŽITÍ DEKÓDOVACÍHO SKRIPTU

Tento soubor ukazuje, jak použít DecodeCleverMinerOutput.py
"""

from DecodeCleverMinerOutput import decode_cleverminer_output

# ============================================================================
# PŘÍKLAD 1: Dekódování výstupu z proměnné
# ============================================================================

cleverminer_output = """
RULE LIST:
5103   109 0.333 +0.345 mean_temp_cat_seq(6) & precipitation_cat_seq(1 2) 
                        & Day of Week(Monday) => Total_Products_cat_seq(2)

5104   87 0.298 +0.312 Total_Price_cat_seq(4 5) & Avg_Item_Price_cat_seq(3) 
                       => precipitation_cat_seq(1)
"""

print("="*70)
print("📄 PŮVODNÍ VÝSTUP:")
print("="*70)
print(cleverminer_output)

print("\n" + "="*70)
print("🔄 DEKÓDOVANÝ VÝSTUP:")
print("="*70)
decoded = decode_cleverminer_output(cleverminer_output)
print(decoded)

# ============================================================================
# PŘÍKLAD 2: Dekódování ze souboru
# ============================================================================

# Spusť v příkazové řádce:
# python DecodeCleverMinerOutput.py cleverminer_output.txt

# Vytvoří soubor: cleverminer_output_decoded.txt

# ============================================================================
# PŘÍKLAD 3: Použití v Question skriptu
# ============================================================================

"""
import pandas as pd
from cleverminer import cleverminer
from DecodeCleverMinerOutput import decode_cleverminer_output
import io
import sys

df = pd.read_csv('datasetAnalyzed.csv')

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.3, 'Base': 100},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 1
    }
)

# Zachyť výstup
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

clm.print_rulelist()

# Získej výstup
output = buffer.getvalue()
sys.stdout = old_stdout

# Dekóduj a vytiskni
decoded_output = decode_cleverminer_output(output)
print(decoded_output)
"""

