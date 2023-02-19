# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:23:49 2019

@author: mark

Run make special before morphing


"""
import os, re
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import pandas as pd

def make_concat(x):
    if x['root'] == 'root':
        concat = '{}{}; {} {} {} {} {} -- {} {}'.format(
                root, x['ending'],
                x['person'], x['number'], x['tense'], x['voice'], x['mood'],
                x['extra'], x['gender'])
    elif x['root'] == 'infinitive':
        concat = '{}{}; {} {} {} {} {} -- {} {}'.format(
                infinitive, x['ending'],
                x['person'], x['number'], x['tense'], x['voice'], x['mood'],
                x['extra'], x['gender'])
    else:
#        print(x)
        concat = ''
    return concat

dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()

SQL_SELECT_SPECIAL = """SELECT * FROM blog_spanishword WHERE special_num IS  NULL and POS = 'v';"""
SQL_INSERT_MORPH = """INSERT INTO blog_spanishmorph
    (def_id_id, form, lower_form, pos, person, number, tense, mood, voice, extra, gender, concat)
    VALUES ($${def_id_id}$$, $${form}$$, $${lower_form}$$, $${pos}$$, $${person}$$, $${number}$$,
            $${tense}$$, $${mood}$$, $${voice}$$, $${extra}$$, $${gender}$$, $${concat}$$)
    """

#SQL_SELECT_SINGLE = """SELECT * FROM treasure_spanish_word WHERE id = 12170"""
#SQL_DELETE_SINGLE = """DELETE FROM treasure_spanishmorph WHERE def_id_id = {}"""

good_endings = ['ar', 'ir', 'er']
dict_cur.execute(SQL_SELECT_SPECIAL)
fetched = dict_cur.fetchall()

def insert_morph(wid):
    print(infinitive, root, wid)
    df = pd.read_csv('/home/mark/Documents/NFSRemote/Spanish/verbs/3_regular.csv', 
                     header=0, 
                     sep = '`',
                     dtype='str')
    df.fillna(' ', inplace=True)
    df['concat'] = df.apply(make_concat, axis=1)
    root_df = df[df['root'] == 'root']
    inf_df = df[df['root'] == 'infinitive']
    
    for l in range(0, len(root_df)):
        insert_dict = root_df.iloc[l].to_dict()
        insert_dict['pos'] = 'v'
        insert_dict['def_id_id'] = wid
        insert_dict['form'] = insert_dict['concat'].split(';')[0]
        insert_dict['lower_form'] = insert_dict['form']
#        print(SQL_INSERT_MORPH.format_map(insert_dict))
        cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
        
    for l in range(0, len(inf_df)):
        insert_dict = inf_df.iloc[l].to_dict()
        insert_dict['pos'] = 'v'
        insert_dict['def_id_id'] = wid
        insert_dict['form'] = insert_dict['concat'].split(';')[0]
        insert_dict['lower_form'] = insert_dict['form']
#        print(SQL_INSERT_MORPH.format_map(insert_dict))
        cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
        
    



for word in fetched:
    print(word['word'])
    verb = word['word']
    ending = verb[-2:]
    if ending == 'ir':
        pass
        infinitive = word['word']
        root = word['word'][:-2]
#        cur.execute(SQL_DELETE_SINGLE.format(word['id']))
        insert_morph(word['id'])
        print('{}\t{}'.format(ending, word['word']))
    else:
        pass
#        print('{}\ se verb'.format(word))


conn.commit()
conn.close()


#def make_concat_root(x):
#    concat = '{}{}; {} {} {} {} {} -- {} {}'.format(
#                root, x['ending'],
#                x['person'], x['number'], x['tense'], x['voice'], x['mood'],
#                x['extra'], x['gender'])
#    print(concat)
#    return concat