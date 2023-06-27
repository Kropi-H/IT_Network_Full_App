from flask import Flask, g
import sqlite3
# Connect to the database
def connect_db():
    sql = sqlite3.connect('/home/honza/Dokumenty/Python_Flask_Udemy/IT_Network_ZP_Plna_verze/pojisteni.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db