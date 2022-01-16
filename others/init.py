import os
import platform
import sqlite3

# Saber en cual SO estamos, para la compatibilidad del comando
if platform.system() == "Windows":
    os.system('del /s /q ..\\database.sqlite')
else:
    os.system('rm ../database.sqlite')

db_name = '../database.sqlite'
db = sqlite3.connect(db_name)


with open('dbScripts/create_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor = db.cursor()
cursor.executescript(sql_script)
db.commit()
db.close()
