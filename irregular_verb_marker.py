# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:04:35 2019

@author: mark

marks verbs as special from a text file made from grammar ook
"""

import os, re
import psycopg2
import psycopg2.extras


dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()


base_path = '/home/mark/Documents/NFSRemote/Spanish/'
fname = 'irregular_verb_list_from_grammar_book.txt'

file_lines = []

SQL_SELECT_VERB = """SELECT id, word, pos 
    FROM blog_spanishword 
    WHERE word=$${}$$ """
    
SQL_UPDATE_VERB = """UPDATE blog_spanishword
    SET special_num = $${special_num}$$
    WHERE id = $${id}$$;
    """

with open(os.path.join(base_path, fname)) as infile:
    for line in infile.readlines():
        file_lines.append(line.strip())
       
not_found_set = set()
type_set = set()   
       
for word_line in file_lines:
    split = word_line.split(',')
#    print('-{}-\t{}'.format(split[0], split))
    dict_cur.execute(SQL_SELECT_VERB.format(split[0]))
    fetched = dict_cur.fetchall()
    if len(fetched) == 1:
        print(word_line)
        print(int(split[1].split('.')[0]))
        type_set.add(int(split[1].split('.')[0]))
        insert_dict = {'id':fetched[0]['id'], 'special_num':split[1].split('.')[0] }
        dict_cur.execute(SQL_UPDATE_VERB.format_map(insert_dict))
        insert_dict = {'id':fetched[0]['id'], 'special_num':split[1].split('.')[0] }
        print(SQL_UPDATE_VERB.format_map(insert_dict))
    else:
#        print(split[0])
        not_found_set.add(split[0])



conn.commit()
conn.close()
def clear_special():
    SQL_SELECT_SPECIAL = """SELECT * FROM treasure_spanish_word WHERE special_num IS NOT NULL;"""
    SQL_REMOVE_SPECIAL = """UPDATE treasure_spanish_word SET special_num = NULL WHERE id = $${}$$;"""
    dict_cur.execute(SQL_SELECT_SPECIAL)
    fetched = dict_cur.fetchall()
    for verb in fetched:
        print(SQL_REMOVE_SPECIAL.format(verb['id']))
        cur.execute(SQL_REMOVE_SPECIAL.format(verb['id']))
    
