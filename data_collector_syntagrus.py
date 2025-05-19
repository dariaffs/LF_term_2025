import os
import csv
from bs4 import BeautifulSoup as bs

def syntagrus_data_collector(filepath):
    with open('lf_data_words.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['LFARG', 'LFFUNC', 'LFVAL'])
        writer.writeheader()

        for address, dirs, files in os.walk(filepath):
            for filename in files:
                with open(os.path.join(address, filename), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    soup = bs(content, 'xml')

                    for s_tag in soup.find_all("S", attrs={ "CLASS": "LF"}):
                        id_to_word = {}
                        for w_tag in s_tag.find_all('W'):
                            word_id = w_tag.get('ID')
                            if word_id:
                                id_to_word[word_id] = w_tag.get('LEMMA')

                        for lf_tag in s_tag.find_all("LF"):

                            lfarg_id = lf_tag.get('LFARG')
                            lfval_id = lf_tag.get('LFVAL')

                            lfarg_word = id_to_word.get(lfarg_id, lfarg_id).lower()
                            lfval_word = id_to_word.get(lfval_id, lfval_id).lower()

                            lffunc = lf_tag.get('LFFUNC', '').lstrip('_')

                            writer.writerow({
                                        'LFARG': lfarg_word,
                                        'LFFUNC': lffunc,
                                        'LFVAL': lfval_word
                                    })

    print('done')   

my_filepath = '/Users/fedko/Desktop/syntagrus/SynTagRus2022'
syntagrus_data_collector(my_filepath)