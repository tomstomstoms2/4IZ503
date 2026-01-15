import pandas as pd
from cleverminer import cleverminer

df = pd.read_csv('../datasetAnalyzed.csv')

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.4, 'Base': 200},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
            {'name': 'precipitation_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
            {'name': 'Day of Week', 'type': 'subset', 'minlen': 1, 'maxlen': 4}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 3
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'Total_Price_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)

clm.print_summary()
clm.print_rulelist()

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.3, 'Base': 100, 'aad': 0.4},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
            {'name': 'precipitation_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
            {'name': 'Day of Week', 'type': 'subset', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 5
    },
    succ={
        'attributes': [
            {'name': 'Total_Products_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'Total_Price_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)

clm.print_summary()
clm.print_rulelist()
