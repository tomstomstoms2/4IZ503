import pandas as pd
from cleverminer import cleverminer

df = pd.read_csv('../datasetAnalyzed.csv')

# Hledání souvislosti mezi sekvencemi teplot a velikostí/cenou objednávek
clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.3, 'Base': 100},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 3}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 3
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'Total_Price_cat', 'type': 'seq', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 3
    }
)

clm.print_summary()
clm.print_rulelist()

