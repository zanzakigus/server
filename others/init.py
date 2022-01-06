import os
import sqlite3

os.system('rm ../database.sqlite')
db_name = '../database.sqlite'
db = sqlite3.connect(db_name)


with open('dbScripts/create_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()