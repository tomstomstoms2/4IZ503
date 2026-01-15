import pandas as pd
from cleverminer import cleverminer
import sys
import io

sys.path.append('..')
from DecodeCleverMinerOutput import decode_cleverminer_output

df = pd.read_csv('../datasetAnalyzed.csv')

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.3, 'Base': 100, 'aad': 0.2},
    ante={
        'attributes': [
            {'name': 'Hour', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
            {'name': 'precipitation_cat_seq', 'type': 'rcut', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 2, 'maxlen': 6
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'Total_Price_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)

# Zachytit výstup summary
print("=" * 70)
print("SUMMARY (original)")
print("=" * 70)
clm.print_summary()

# Zachytit a dekódovat rulelist
print("\n" + "=" * 70)
print("RULELIST (decoded)")
print("=" * 70)

old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()
clm.print_rulelist()
output = buffer.getvalue()
sys.stdout = old_stdout

# Dekódovat a vytisknout
decoded_output = decode_cleverminer_output(output)
print(decoded_output)

clm = cleverminer(
    df=df,
    proc='SD4ftMiner',
    quantifiers={'Ratioconf': 1.1, 'Base1': 200, 'Base2': 2000},
    ante={
        'attributes': [
            {'name': 'Hour', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 3
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'Total_Price_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    frst={
        'attributes': [
            {'name': 'precipitation_cat_seq', 'type': 'rcut', 'minlen': 1, 'maxlen': 2}
        ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
    scnd={
        'attributes': [
            {'name': 'precipitation_cat_seq', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}
        ], 'minlen': 1, 'maxlen': 2, 'type': 'con'}
)

# Zachytit výstup summary
print("=" * 70)
print("SUMMARY (original)")
print("=" * 70)
clm.print_summary()

# Zachytit a dekódovat rulelist
print("\n" + "=" * 70)
print("RULELIST (decoded)")
print("=" * 70)

old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()
clm.print_rulelist()
output = buffer.getvalue()
sys.stdout = old_stdout

# Dekódovat a vytisknout
decoded_output = decode_cleverminer_output(output)
print(decoded_output)
