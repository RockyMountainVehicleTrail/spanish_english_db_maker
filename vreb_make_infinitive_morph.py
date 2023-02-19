# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 12:00:48 2019

@author: mark
"""


dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()

SQL_SELECT_VERBS = """SELECT * FROM drb_spanishword WHERE pos = 'v';"""
SQL_INSERT_MORPH = """INSERT INTO drb_spanishmorph
    (def_id_id, form, lower_form, pos, mood, voice, concat)
    VALUES ($${def_id_id}$$, $${form}$$, $${lower_form}$$, $${pos}$$,
            $${mood}$$, $${voice}$$, $${concat}$$)
    """
    
    
dict_cur.execute(SQL_SELECT_VERBS)
fetched = dict_cur.fetchall()

for word in fetched:
    insert_dict = {'def_id_id':word['id'], 'form':word['word'], 'lower_form':word['word'],
                   'pos':word['pos'], 'mood':'infinitive', 'voice':'active',
                    'concat':word['word']}
    print(SQL_INSERT_MORPH.format_map(insert_dict))
    cur.execute(SQL_INSERT_MORPH.format_map(insert_dict))
    
    
conn.commit()
conn.close()    





    
    
    
    
