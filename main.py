import requests
import pandas as pd
import csv
import time
from multiprocessing import Pool
import os


def pool_call(rg_start, rg_end):
    get_manual_result(range_start=rg_start, range_end=rg_end)


def get_manual_result(query: str = 'TITLE-ABS-KEY ( machine  AND learning )',
                      api_key: str = 'bddfe2f4cd0dabf385c0ab5d6c9cd7f2', range_start: int = 0,
                      range_end: int = 3000) -> list:
    titles = []
    for start in range(range_start, range_end, 25):
        print(f'[...] start: {start}')
        req_url = f'https://api.elsevier.com/content/search/scopus?apiKey={api_key}&query={query}&start={start}'
        req_result = requests.get(req_url)
        result_json = req_result.json()
        try:
            entry = result_json['search-results']['entry']
        except KeyError:
            return titles
        for element in entry:
            title = element['dc:title']
            titles.append(title)
    titles_to_csv_writer(titles, 'test_pool.csv')
    return titles


# Pior desempenho em relação csv writer
def titles_to_csv_pd(titles: list, file: str):
    start_time = time.time()
    titles_df = pd.DataFrame(titles, columns=['title'])
    titles_df.set_index('title')
    titles_df.to_csv(file, index=False)
    print(f"titles_to_csv_pd = {(time.time() - start_time)}seconds ---")


def titles_to_csv_writer(titles: list[str], file: str):
    if not os.path.exists(file):
        with open(file, 'w', newline='', encoding='utf-8') as file:
            write = csv.writer(file, delimiter=',', lineterminator='\n')
            write.writerow(['title'])
    else:
        with open(file, 'a', newline='', encoding='utf-8') as file:
            write = csv.writer(file, delimiter=',', lineterminator='\n')
            for title in titles:
                if '<inf>' in title:
                    title = title.replace('<inf>', '').replace('</inf>', '')
                if ' ' in title:
                    title = title.replace(' ', ' ')
                write.writerow([title])


if __name__ == '__main__':
    start_time = time.time()

    args = [(0, 600), (600, 1200), (1200, 1800), (1800, 2400), (2400, 3000)]

    with Pool(5) as p:
        print('Pool:')
        records = p.starmap(pool_call, args)

    print(f"\n[***] main = {(time.time() - start_time)} seconds")


    # result_titles = get_manual_result(query='TITLE-ABS-KEY ( machine  AND learning )',
    #                                   api_key='bddfe2f4cd0dabf385c0ab5d6c9cd7f2')
    # result_titles_error = get_manual_result(query='TITLE-ABS-KEY ( "software process improvement"  AND  "software '
    #                                               'engineering" )', api_key='bddfe2f4cd0dabf385c0ab5d6c9cd7f2',
    #                                         range_start=1000, range_end=1075)
    # titles_to_csv_writer(result_titles_error, 'test_writer_2.csv')
