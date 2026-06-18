from enum import Enum
import sqlite3

dbcon = sqlite3.connect("databases/trpg.db")
dbcsr = dbcon.cursor()

entry_types = Enum("Entry_Type", ["GENERAL", "LOCATION", "NPC", "QUEST"])

class Entry:
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
                
        
class Location(Entry):

    def __init__(self, time_of_entry, last_edit, name, description, region, landmarks):
        super().__init__(time_of_entry, last_edit, name, description)
        self.region = region
        self.landmarks = landmarks


class NPC(Entry):
    
    def __init__(self, time_of_entry, last_edit, name, description):
        super().__init__(time_of_entry, last_edit, name, description)


def create_entry(name, description)
    
    dbcsr.execute(
        "INSERT INTO Entrys (name, description) VALUES (%s, %s);", 
        (name, description)
    )

def assemble_entry(row):
    entry = Entry(row[0], row[1])