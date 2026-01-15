import pandas as pd
from cleverminer import cleverminer

df = pd.read_csv('CleverMiner/datasetMerged.csv')

clm = cleverminer(
    df=df,
    proc='4ftMiner',
    quantifiers={'conf': 0.2, 'Base': 500},
    ante={
        'attributes': [
            {'name': 'mean_temp_cat', 'type': 'subset', 'minlen': 1, 'maxlen': 2}#,
            #{'name': 'DAY_OF_WEEK', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    },
    succ={
        'attributes': [
            {'name': 'Total products', 'type': 'subset', 'minlen': 1, 'maxlen': 2}
        ],
        'type': 'con', 'minlen': 1, 'maxlen': 2
    }
)

clm.print_summary()
clm.print_rulelist()
