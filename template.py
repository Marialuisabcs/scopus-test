from pybliometrics.scopus import utils, ScopusSearch
import pandas as pd

#  se não criou o .config automático: ~/.pybliometrics/config.in na home
# utils.create_config()

search_string_1 = 'TITLE-ABS-KEY ( machine  AND learning )'
search_string_2 = 'TITLE-ABS-KEY ( "software process improvement"  AND  "software engineering" )'

search_results = ScopusSearch(search_string_1, subscriber=False, start='0', count='10')


results_df = pd.DataFrame(pd.DataFrame(search_results.results))
results_df['title'].to_csv('teste.csv', index=False)
print(results_df)


