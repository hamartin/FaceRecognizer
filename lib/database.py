'''
This file represents the database of the software.

Dabase structure

labels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
)

images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  labelid INTEGER NOT NULL,
  data BLOB NOT NULL,
  FOREIGN KEY (labelid)
    REFERENCES labels (id)
)
'''


import sqlite3

import pandas as pd


class DB():

    '''This class represents the database of the software.'''

    def __init__(self, filename=""):
        assert isinstance(filename, str)
        if filename:
            self._conn = sqlite3.connect(filename)
        else:
            self._conn = sqlite3.connect(":memory:")
        self._cursor = self._conn.cursor()
        self._initializeDb()

    def __repr__(self):
        return "DB(filename={0})".format(self._filename)

    def __str__(self):
        return self.__repr__()

    def _initializeDb(self):
        self._cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS labels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );''')
        self._cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    labelid INTEGER NOT NULL,
                    data BLOB NOT NULL,
                    FOREIGN KEY (labelid)
                        REFERENCES labels (id)
                );''')
        self._conn.commit()

    def addFrame(self, frame, labelId):
        '''Creates a new record in the images table.'''
        assert isinstance(frame, bytes)
        assert isinstance(labelId, int)
        self._cursor.execute('''INSERT INTO images (labelid, data) VALUES(?, ?);''', [labelId, sqlite3.Binary(frame)])
        self._conn.commit()

    def addLabel(self, name):
        '''Creates a new record in the labels table with name=name.'''
        assert isinstance(name, str)
        self._cursor.execute('''INSERT INTO labels (name) VALUES(?);''', [name, ])
        self._conn.commit()
        return self.getLabelId(name)

    def getInformation(self):
        '''Returns information about all the tables in the database.'''
        self._cursor.execute('''SELECT * FROM sqlite_master WHERE type='table';''')
        tables = self._cursor.fetchall()

        ret = []
        for table in tables:
            tableName = table[1]
            if tableName == "sqlite_sequence":
                continue
            ret.append(pd.read_sql_query("SELECT * FROM %s" % tableName, self._conn).describe)
        return ret

    def getLabelId(self, name):
        '''Returns the ID of a label if it exist, else None.'''
        self._cursor.execute('''SELECT id FROM labels WHERE name='%s';''' % name)
        data = self._cursor.fetchall()
        if data:
            data = data[0][0]
        return data
