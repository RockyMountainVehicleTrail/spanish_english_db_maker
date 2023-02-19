# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 13:34:58 2019

@author: mark
"""

import os, re
import psycopg2
import psycopg2.extras


SQL_GET_NOUNS = """SELECT * FROM blog_spanishword WHERE pos = 'n'"""

SQL_GET_NOUNS_NEW = """SELECT * FROM blog_spanishword 
                    WHERE pos = 'n' 
                    AND id IN (12171)"""
                    
SQL_INSERT_MORPH = """INSERT INTO blog_spanishmorph
    (def_id_id, form, lower_form, pos, number, gender, concat)
    VALUES ($${def_id_id}$$, $${form}$$, $${lower_form}$$, $${pos}$$,
            $${number}$$, $${gender}$$, $${concat}$$)
    """

SQL_DELETE_MORPHS = """DELETE FROM blog_spanishmorph WHERE def_id_id = {}"""



dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()


dict_cur.execute(SQL_GET_NOUNS)
fetched = dict_cur.fetchall()

spanish_char_set = set()
vowel_list = ['a',  'e',  'i',  'o',  'u',  'á',  'é',  'í',  'ó',  'ú',  'ü']

for sword in fetched:
    cur.execute(SQL_DELETE_MORPHS.format(sword['id']))
    for c in sword['word']:
        spanish_char_set.add(c)
    insert_dict = {'def_id_id':sword['id'],
                   'form':sword['word'],
                   'lower_form':sword['word'].lower(),
                   'pos':'n',
                   'number':'sing'}

    concat = '{}; {} -- {} {}'.format(sword['word'], sword['word'], 'noun', 'sing')
    insert_dict['concat'] = concat                
                    
    # get gender
    if sword['word'][-1:] == 'a':
        insert_dict['gender'] = 'fem'
    elif sword['word'][-1:] == 'o':
        insert_dict['gender'] = 'mas'
    else:
        insert_dict['gender'] = 'unk'
        
    # insert singular    
    cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
    
    # make plural
    insert_dict['number'] = 'plural'
    if sword['word'][-1:] in vowel_list:
        insert_dict['form'] = '{}s'.format(sword['word'])
        insert_dict['lower_form'] = '{}s'.format(sword['word'].lower())
        concat = '{}; {} -- {} {}'.format(
                sword['word'], insert_dict['lower_form'], 'noun', 'plural'
                )
    elif  sword['word'][-1:] == 'z':
        insert_dict['form'] = '{}ces'.format(sword['word'][:-1])
        insert_dict['lower_form'] = '{}ces'.format(sword['word'][:-1].lower())
        concat = '{}; {} -- {} {}'.format(
                sword['word'], insert_dict['lower_form'], 'noun', 'plural'
                )
    else:
        insert_dict['form'] = '{}es'.format(sword['word'])
        insert_dict['lower_form'] = '{}es'.format(sword['word'].lower())
        concat = '{}; {} -- {} {}'.format(
                sword['word'], insert_dict['lower_form'], 'noun', 'plural'
                )
                
    insert_dict['concat'] = concat                

        
    cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
    
conn.commit()
conn.close()
        
        
        
        
        

    
    
        
    
    












