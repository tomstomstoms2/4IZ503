import pandas as pd
import sys
import io
sys.path.append('..')
from cleverminer import cleverminer
from DecodeCleverMinerOutput import decode_cleverminer_output

df = pd.read_csv('../datasetDailyCompound.csv')

clm = cleverminer(
    df=df,
    target='Orders_Count_cat_seq',
    proc='CFMiner',
    quantifiers={'Base': 300, 'S_Down': 1},
    cond={
        'attributes': [
            {'name': 'Day of Week Number', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'mean_temp_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'precipitation_cat_seq', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)

print("="*70)
print("SUMMARY")
print("="*70)
clm.print_summary()

print("\n" + "="*70)
print("RULELIST (decoded)")
print("="*70)

# Zachytit výstup jako string
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()
clm.print_rulelist()
output = buffer.getvalue()
sys.stdout = old_stdout

# Dekódovat a vytisknout
decoded = decode_cleverminer_output(output)
print(decoded)

