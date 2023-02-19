# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 12:18:28 2019

@author: mark
"""
#Imported do not reenable
intentionally broken so as to not run again and ruin the database



import os, re
import psycopg2
import psycopg2.extras


dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()

SQL_INSERT_ENG_WORD = """INSERT INTO blog_spanishengword
    (word, pos, spanish_phrase )   VALUES
    ( $${word}$$, $${pos}$$,  $${spanish_phrase}$$)
    """

SQL_INSERT_SPANISH_WORD = """INSERT INTO blog_spanishword
    (word, pos, eng_trans, special, morphed)  VALUES
    ( $${word}$$, $${pos}$$,  $${eng_trans}$$, $${special}$$, $${morphed}$$)
    """
    
SQL_GET_SPANISH_WORD = """SELECT id, eng_trans 
        FROM blog_spanishword
        WHERE word = $${}$$"""
        
SQL_UPDATE_SPANISH_WORD = """UPDATE blog_spanishword
    SET eng_trans = $${}$$ 
    WHERE id = $${}$$;"""
    



def spanish_word_handler(eng_word, pos, spanish_word):
    dict_cur.execute(SQL_GET_SPANISH_WORD.format(spanish_word))
    fetched = dict_cur.fetchall()
    
    if fetched:
        eng_trans = '{} ;; {}'.format(fetched[0]['eng_trans'], eng_word.lower())
        spanish_insert_dict = {'word':spanish_word, 'pos':pos,
                               'eng_trans':eng_trans, 'special':False,
                               'morphed':False}
        cur.execute(SQL_UPDATE_SPANISH_WORD.format(eng_trans, fetched[0]['id']))
    else:
        eng_trans = eng_word
        spanish_insert_dict = {'word':spanish_word, 'pos':pos, 
                               'eng_trans':eng_word.lower(), 'special':False,
                               'morphed':False }
        dict_cur.execute(SQL_INSERT_SPANISH_WORD.format_map(spanish_insert_dict))

main_file_name = 'pg20738_guenberg_dictionary_cropped.txt'
root_fodler = '/home/mark/Documents/NFSRemote/Spanish/gut_spanish_dictionary/'

with open(os.path.join(root_fodler, main_file_name)) as infile:
    file_str = infile.read()
    
file_tilda = file_str.replace('\n', '`')
letters = re.findall('[A-Z]{1}`', file_tilda)
split = re.split('[A-Z]{1}`', file_tilda)

count = 0
pos_set = set()
pos_raw_set = set()
spanish_char_set = set()

for i in range(0, len(letters)):
    with open(os.path.join(root_fodler, letters[i]), 'w') as ofile:
        with open(os.path.join(root_fodler, 'parsed_{}.txt'.format(letters[i])), 'w') as parse_file:
            words = re.split(r'``', split[i+1])
            for word in words:
                if len(re.findall(r'`', word)) > 2:
                    count += 1
#                    print(word.replace('`', '\n'))
#                    print('\n')
                if len(re.findall(r'`', word)) == 2:
                    parse_file.write(word)
                    eng_section = word.split('`')[0]
                    parse_file.write('eng_section:{}\n'.format(eng_section))
                    eng_word = eng_section.split(',')[0]
#                    if len(eng_section.split(',')) > 2:
#                        print(word)
                    parse_file.write('eng_word:{}\n'.format(eng_word))
#                    if eng_word.find(',')

# PARSE POS                    
                    pos_found = re.findall(r' [a-z.]{1,5}.', eng_section.split(',')[1])
                    if pos_found:
                        pos_raw_set.add(pos_found[0])
                        pos = pos_found[0].strip().replace('.', '').replace(':', '')
                        if pos == 'a':
                            pos = 'adj'
                        pos_set.add(pos)
                        parse_file.write('pos:{}:\n'.format(pos))
                    else:
                        parse_file.write('pos:none\n')

## PARSE SPANISH
                    spanish_section = word.split('`')[1] 
                    parse_file.write('\nspanish:{}\n'.format(spanish_section))
                    for spanish_split in spanish_section.split(','):
                        if spanish_split.strip().find(' ') == -1:
                            parse_file.write('spanish_word:{}\n'.format(spanish_split.strip()))
                            spanish_word = spanish_split.strip().lower().replace('.', '').replace('!','').replace('(','').replace(')','').replace('-','').replace('-','').replace('[','').replace(']','').replace(';','')
                            spanish_word_handler(eng_word.lower(), pos, spanish_word)
                        else:
                            parse_file.write('spanish_phrase:{}\n'.format(spanish_split.strip()))
#                    parse_file.write(word)
                    parse_file.write('\n\n')

## INSERT ENGLISH                    
                    eng_insert_dict = {'word':eng_word.lower(), 
                                       'pos':pos, 
                                       'spanish_phrase': spanish_section.lower()}
                    parse_file.write(SQL_INSERT_ENG_WORD.format_map(eng_insert_dict))
                    dict_cur.execute(SQL_INSERT_ENG_WORD.format_map(eng_insert_dict))
                    parse_file.write('\n\n\n')
            ofile.write(split[i+1].replace('`', '\n'))
        
conn.commit()
conn.close()      
       
print(pos_set)
print(pos_raw_set)

