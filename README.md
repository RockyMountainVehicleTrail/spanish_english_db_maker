I found a Spanish English dictionary on project gutenberg and wrote various scripts to parse it create a morphology table and upload to my database.

The dictionary_parser.py parsed the dictionary

I wrote separate scripts for different POSs and also for different classes of verbs.  None of the sripts work they are missing the DB connection and one was broken intentionally after the inital upload to avoid rerunning and ruining the databse.
