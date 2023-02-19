# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:23:49 2019

@author: mark
"""

import os, re
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas as pd

def make_concat(x):
    
    concat = '{}{}; {} {} {} {} {} -- {} {}'.format(
            prefix, x['ending'],
            x['person'], x['number'], x['tense'], x['voice'], x['mood'],
            x['extra'], x['gender'])
    
    return concat


dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()

#SQL_SELECT_SPECIAL = """SELECT * FROM treasure_spanish_word WHERE special_num IS  NULL and POS = 'v';"""
SQL_INSERT_MORPH = """INSERT INTO blog_spanishmorph
    (def_id_id, form, lower_form, pos, person, number, tense, mood, voice, extra, gender, concat)
    VALUES ($${def_id_id}$$, $${form}$$, $${lower_form}$$, $${pos}$$, $${person}$$, $${number}$$,
            $${tense}$$, $${mood}$$, $${voice}$$, $${extra}$$, $${gender}$$, $${concat}$$)
    """
    
SQL_GET_VERB = """SELECT * FROM blog_spanishword WHERE word = '{}'"""    
    
    
root = 'poner'
ver_list = [ 'deponer','descomponer','imponer','entreponer','interponer','componer','posponer','disponer','presuponer','proponer','reponer','exponer','poner','suponer','trasponer']

for pref_word in ver_list:
    dict_cur.execute(SQL_GET_VERB.format(pref_word))
    fetched = dict_cur.fetchall()
    if len(fetched) == 1:
        wid = fetched[0]['id']
        prefix = pref_word[0:(len(pref_word) - len(root))]
        print(prefix)
    
    
        #print(infinitive, root, wid)
        df = pd.read_csv('/home/mark/Documents/NFSRemote/Spanish/verbs/irregular/{}.csv'.format(root), 
                         header=0, 
                         sep = '`',
                         dtype='str')
        df.fillna(' ', inplace=True)
        df['concat'] = df.apply(make_concat, axis=1)
        root_df = df[df['root'] == 'root']
        inf_df = df[df['root'] == 'infinitive']
        special_df = df[df['root'] == 'special']
        
        for l in range(0, len(root_df)):
            insert_dict = root_df.iloc[l].to_dict()
            insert_dict['pos'] = 'v'
            insert_dict['def_id_id'] = wid
            insert_dict['form'] = insert_dict['concat'].split(';')[0]
            insert_dict['lower_form'] = insert_dict['form']
            print(SQL_INSERT_MORPH.format_map(insert_dict))
            cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
            
        for l in range(0, len(inf_df)):
            insert_dict = root_df.iloc[l].to_dict()
            insert_dict['pos'] = 'v'
            insert_dict['def_id_id'] = wid
            insert_dict['form'] = insert_dict['concat'].split(';')[0]
            insert_dict['lower_form'] = insert_dict['form']
            print(SQL_INSERT_MORPH.format_map(insert_dict))
            cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
            
        for l in range(0, len(special_df)):
            insert_dict = special_df.iloc[l].to_dict()
            insert_dict['pos'] = 'v'
            insert_dict['def_id_id'] = wid
            insert_dict['form'] = insert_dict['concat'].split(';')[0]
            insert_dict['lower_form'] = insert_dict['form']
            print(SQL_INSERT_MORPH.format_map(insert_dict))
            cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
        
    
    
    
    
    


conn.commit()
conn.close()


