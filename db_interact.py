from enum import Enum
import sqlite3

dbcon = sqlite3.connect("databases/trpg.db")
dbcsr = dbcon.cursor()

entry_types = Enum("Entry_Type", ["GENERAL", "LOCATION", "NPC", "QUEST"])

class Entry:
    
    def __init__(self, time_of_entry, last_edit, name, description):
        self.time_of_entry = time_of_entry
        self.last_edit = last_edit
        self.name = name
        self.description = description
    
    def add_entry(self, name, description):
                
        
class Location(Entry):

    def __init__(self, time_of_entry, last_edit, name, description, region, landmarks):
        super().__init__(time_of_entry, last_edit, name, description)
        self.region = region
        self.landmarks = landmarks


class NPC(Entry):
    def __init__(self, time_of_entry, last_edit, name, description):
        super().__init__(time_of_entry, last_edit, name, description)


def start_entry(entry_type):
    if entry_type == Entry_Type.GENERAL:
        return create_entry()
    if entry_type == Entry_Type.LOCATION:
        return create_location()
    if entry_type == Entry_Type.NPC:
        return create_npc()
    if entry_type == Entry_Type.QUEST:
        return create_quest()


def create_entry(name, description)
    
    dbcsr.execute(
        "INSERT INTO Entrys (name, description) VALUES (%s, %s);", 
        (name, description)
    )