from enum import Enum
from datetime import datetime
import sqlite3
import sys

# Establish database connection

cnx = sqlite3.connect("databases/trpg.db")
csr = cnx.cursor()
cnx.execute("PRAGMA foreign_keys = ON;")

# Create tables
csr.executescript("""

    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        parent_location_id INTEGER DEFAULT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
        CONSTRAINT fk_parent_location_id FOREIGN KEY (parent_location_id) REFERENCES locations(id)
    );

    CREATE TRIGGER IF NOT EXISTS update_location_timestamp AFTER UPDATE ON locations
    FOR EACH ROW
    BEGIN
        UPDATE locations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

            
    CREATE TABLE IF NOT EXISTS npcs (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        location_id INTEGER,
        status VARCHAR(10) DEFAULT "unknown", -- Add ENUM on Python side
        relationship VARCHAR(10) DEFAULT "neutral", -- Add ENUM on Python side
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
        CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES locations(id)
    );

    CREATE TRIGGER IF NOT EXISTS update_npc_timestamp AFTER UPDATE ON npcs
    FOR EACH ROW
    BEGIN
        UPDATE npcs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;


    CREATE TABLE IF NOT EXISTS quests (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        goals TEXT,
        giver_id INTEGER,
        status VARCHAR(10) DEFAULT "active", -- Add ENUM on Python side
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
        CONSTRAINT fk_giver_id FOREIGN KEY (giver_id) REFERENCES npcs(id)
    );

    CREATE TRIGGER IF NOT EXISTS update_quest_timestamp AFTER UPDATE ON quests
    FOR EACH ROW
    BEGIN
        UPDATE quests SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;


    CREATE TABLE IF NOT EXISTS general_entries (
        id INTEGER PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        deleted_at TEXT DEFAULT "9999-12-31 23:59:59"
    );

    CREATE TRIGGER IF NOT EXISTS update_general_entry_timestamp AFTER UPDATE ON general_entries
    FOR EACH ROW
    BEGIN
        UPDATE general_entries SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;


    CREATE TABLE IF NOT EXISTS entries_x_npcs (
        id INTEGER PRIMARY KEY,
        entry_id INTEGER,
        npc_id INTEGER,
        FOREIGN KEY (entry_id) REFERENCES general_entries(id),
        FOREIGN KEY (npc_id) REFERENCES npcs(id),
        UNIQUE (entry_id, npc_id)
    );

    CREATE TABLE IF NOT EXISTS entries_x_locations (
        id INTEGER PRIMARY KEY,
        entry_id INTEGER,
        location_id INTEGER,
        FOREIGN KEY (entry_id) REFERENCES general_entries(id),
        FOREIGN KEY (location_id) REFERENCES locations(id),
        UNIQUE (entry_id, location_id)
    );

    CREATE TABLE IF NOT EXISTS entries_x_quests (
        id INTEGER PRIMARY KEY,
        entry_id INTEGER,
        quest_id INTEGER,
        FOREIGN KEY (entry_id) REFERENCES general_entries(id),
        FOREIGN KEY (quest_id) REFERENCES quests(id),
        UNIQUE (entry_id, quest_id)
    );

    CREATE TABLE IF NOT EXISTS quests_x_locations (
        id INTEGER PRIMARY KEY,
        quest_id INTEGER,
        location_id INTEGER,
        FOREIGN KEY (quest_id) REFERENCES quests(id),
        FOREIGN KEY (location_id) REFERENCES locations(id),
        UNIQUE (quest_id, location_id)
    );

    CREATE TABLE IF NOT EXISTS quests_x_npcs (
        id INTEGER PRIMARY KEY,
        quest_id INTEGER,
        npc_id INTEGER,
        FOREIGN KEY (quest_id) REFERENCES quests(id),
        FOREIGN KEY (npc_id) REFERENCES npcs(id),
        UNIQUE (quest_id, npc_id)
    );

    CREATE TABLE IF NOT EXISTS npcs_x_locations (
        id INTEGER PRIMARY KEY,
        npc_id INTEGER,
        location_id INTEGER,
        FOREIGN KEY (npc_id) REFERENCES npcs(id),
        FOREIGN KEY (location_id) REFERENCES locations(id),
        UNIQUE (npc_id, location_id)
    );
    """)

cnx.commit()

entry_types = Enum("Entry_Type", ["GENERAL", "LOCATION", "NPC", "QUEST"])

class NPC_Status(Enum):
    ALIVE: str = "Alive"
    DEAD: str = "Dead"
    UNKNOWN: str = "Unknown"

class NPC_Relationship(Enum):
    ALLY: str = "Ally"
    FRIENDLY: str = "Friendly"
    NEUTRAL: str = "Neutral"
    HOSTILE: str = "Hostile"

class Quest_Status(Enum):
    ACTIVE: str = "Active"
    COMPLETED: str = "Completed"
    FAILED: str = "Failed"

class Entry:
    
    def __init__(self, id: int, name: str, description: str, created_at: str, updated_at: str, deleted_at: str):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.created_at: datetime = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        self.updated_at: datetime = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
        self.deleted_at: datetime = datetime.strptime(deleted_at, "%Y-%m-%d %H:%M:%S")

class Location(Entry):

    def __init__(self, id: int, name: str, description: str, created_at: str, updated_at: str, deleted_at: str, parent: int = None):
        super().__init__(id, name, description, created_at, updated_at, deleted_at)
        self.parent: Location = parent


class NPC(Entry):
    
    def __init__(self, id: int, name: str, description: str, created_at: str, updated_at: str, deleted_at: str, location, status: NPC_Status, pc_relationship: NPC_Relationship):
        super().__init__(id, name, description, created_at, updated_at, deleted_at)
        self.location: Location = location
        self.status = NPC_Status[status].value
        self.relationship = NPC_Relationship[pc_relationship].value

class Goal:

    def __init__(self, id: int, description: str, status: str, created_at: str, updated_at: str, deleted_at: str):
        self.id: int = id
        self.description: str = description
        self.status: Quest_Status = Quest_Status[status].value
        self.created_at: datetime = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        self.updated_at: datetime = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
        self.deleted_at: datetime = datetime.strptime(deleted_at, "%Y-%m-%d %H:%M:%S")

class Quest(Entry):
    
    def __init__(self, id: int, name: str, description: str, created_at: str, updated_at: str, deleted_at: str, giver: NPC, status: str, goals: list[Goal] = []):
        super().__init__(id, name, description, created_at, updated_at, deleted_at)
        self.giver: NPC = giver
        self.status: Quest_Status = Quest_Status[status].value
        self.goals: list[Goal] = goals


# input functions

def create_general_entry() -> None:
    
    name: str = input("Entry name:\n>")
    description: str = input("Entry description:\n>")

    try:
        csr.execute(
            "INSERT INTO general_entries (name, description) VALUES (?, ?);", 
            (name, description)
        )
    except Exception as e:
        print(f"Error occurred while creating general entry: {e}")
        cnx.rollback()
        return

    cnx.commit()

    print(f"General entry '{name}' created successfully!")

    return

def create_location() -> None:
    
    name: str = input("Location name:\n>")
    description: str = input("Location description:\n>")
    region: str = input("Location region (leave blank if none):\n>")
    landmarks: str = input("Location landmarks (leave blank if none):\n>")

    try:
        csr.execute(
            "INSERT INTO locations (name, description, region, landmarks) VALUES (?, ?, ?, ?);", 
            (name, description, region, landmarks)
        )
    except Exception as e:
        print(f"Error occurred while creating location: {e}")
        cnx.rollback()
        return

    cnx.commit()

    print(f"Location '{name}' added to notes")

    return

def create_npc() -> None:
    name: str = input("NPC name:\n>")
    description: str = input("NPC description:\n>")
    location_id: str = input("NPC location ID (leave blank if none):\n> ")

    # NEED TO ADD ABILITY TO LOOK UP LOCATION ID BY NAME, ADD PREVIEW OF MOST RECENT LOCATIONS

    while True:
        status: str = input("NPC status (alive, dead, unknown):\n>").upper()
        if not isinstance(status, NPC_Status):
            print("Invalid status. Please enter alive, dead, or unknown.")
        break
    
    while True:
        relationship: str = input("NPC relationship (ally, friendly, neutral, hostile): ").upper()
        if not isinstance(relationship, NPC_Relationship):
            print("Invalid relationship. Please enter ally, friendly, neutral, or hostile.")
        break

    try:
        csr.execute(
                "INSERT INTO npcs (name, description, location_id, status, relationship) VALUES (?, ?, ?, ?, ?);", 
                (name, description, location_id if location_id else None, status, relationship)
            )
        
    except Exception as e:
        print(f"Error occurred while creating NPC: {e}")
        cnx.rollback()
        return

    cnx.commit()

    print(f"NPC '{name}' added to notes")

    return

def create_quest() -> None:
    name: str = input("Quest name: ")
    description: str = input("Quest description: ")
    giver_id = input("Quest giver ID (leave blank if none): ")
    status: str = "ACTIVE"

    try:
        csr.execute(
            "INSERT INTO quests (name, description, giver_id, status) VALUES (?, ?, ?, ?);", 
            (name, description, giver_id if giver_id else None, status)
        )
    except Exception as e:
        print(f"Error occurred while creating quest: {e}")
        cnx.rollback()
        return

    cnx.commit()

    print(f"Quest '{name}' added to log")
    add_goals = input("Would you like to add goals to this quest? (y/n):\n>").lower()
    if add_goals == "y":
        create_goal(csr.lastrowid)

def create_goal(quest_id: int = None):

    if quest_id is None:

        csr.execute("SELECT id, name, SUBSTR(description, 1, 25) FROM quests ORDER BY MAX(created_at, updated_at) DESC;")

        while True:
            recent_quests: list[tuple[int, str, str]] = csr.fetchmany(5)

            print("Recent quests:")
            for quest in recent_quests:
                print(f"ID: {quest[0]} | Name: {quest[1]} | Preview: \"{quest[2]}\" [ ... ]")
            more_quests: str = input("Would you like to see more quests? (y/n):\n>").lower()
            if more_quests != "y":
                break

        while True:
            try:
                quest_id: int = int(input("Enter the ID of the quest this goal belongs to: "))
                csr.execute("SELECT id FROM quests WHERE id = ?;", (quest_id,))
                if csr.fetchone() is None:
                    print("Invalid quest ID. Please try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer for the quest ID.")

    description: str = input("Goal description: ")
    status: str = input("Goal status (active, completed, failed): ").upper()

    try:
        csr.execute(
            "INSERT INTO goals (quest_id, description, status) VALUES (?, ?, ?);", 
            (quest_id, description, status)
        )
    except Exception as e:
        print(f"Error occurred while creating goal: {e}")
        cnx.rollback()
        return

    cnx.commit()

    print(f"Goal '{description}' added to log")

    create_new_goal:str = ("Would you like to add another goal to this quest? (y/n)\n>").lower()

    if create_new_goal == "y":
        return create_goal(quest_id)

    return

# view functions

def convert_sql_date_format_to_mdy(sql_date) -> str:

    # convert date from SQL table to a more readable format (JAN 01 2026)

    dt: datetime = datetime.strptime(sql_date, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%b %d %Y")

def convert_dmy_to_sql_date_format(date_str) -> str:

    # convert date from JAN 01 2026 to SQL table format (2026-01-01)

    dt = datetime.strptime(date_str, "%b %d %Y")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def view_entry() -> None:

    # pull the 10 most recent entries from all tables, ordered by latest timestamp
    
    csr.execute("""
                SELECT * FROM (
                SELECT 'general_entries' AS source_table,
                    name,
                    SUBSTR(description, 1, 25) AS preview,
                    NULL AS related_quest,
                    NULL AS status,
                    MAX(created_at, updated_at) AS latest_timestamp
                FROM general_entries

                UNION ALL

                SELECT 'locations', name, SUBSTR(description, 1, 25), NULL, NULL, MAX(created_at, updated_at)
                FROM locations

                UNION ALL

                SELECT 'npcs', name, SUBSTR(description, 1, 25), NULL, status, MAX(created_at, updated_at)
                FROM npcs

                UNION ALL

                SELECT 'quests', name, SUBSTR(description, 1, 25), NULL, NULL, MAX(created_at, updated_at)
                FROM quests

                UNION ALL

                SELECT 'goals',
                    SUBSTR(g.description, 1, 25) AS name,
                    SUBSTR(g.description, 1, 25) AS preview,
                    q.name AS related_quest,
                    q.status AS status,
                    MAX(g.created_at, g.updated_at) AS latest_timestamp
                FROM goals g
                JOIN quests q ON q.id = g.quest_id
                )
                ORDER BY latest_timestamp DESC
                LIMIT 10;
                """)
    
    recent_entries = csr.fetchall()

    # display the recent entries, modifying according to data type

    print("Recent entries:")
    for entry in recent_entries:
        if entry[0] == "goals":
            print(f"Goal: {entry[1]} | Preview: \"{entry[2]}\" [ ... ] | Status: {entry[4]} | Quest: {entry[3]}")
        if entry[0] == "general_entries":
            print(f"Entry: {entry[1]} | Preview: \"{entry[2]}\" [ ... ]")
        if entry[0] == "locations":
            print(f"Location: {entry[1]} | Preview: \"{entry[2]}\" [ ... ]")
        if entry[0] == "npcs":
            print(f"NPC: {entry[1]} | Preview: \"{entry[2]}\" [ ... ] | Status: {entry[4]}")

def recap_entry(entry: Entry) -> str:

    

def recap():

    # pull all entries from all tables, ordered by the latest timestamp

    csr.execute("""
        SELECT latest_timestamp
        FROM (
            SELECT MAX(created_at, updated_at) AS latest_timestamp FROM general_entries
            UNION ALL
            SELECT MAX(created_at, updated_at) AS latest_timestamp FROM locations
            UNION ALL
            SELECT MAX(created_at, updated_at) AS latest_timestamp FROM npcs
            UNION ALL
            SELECT MAX(created_at, updated_at) AS latest_timestamp FROM quests
            UNION ALL
            SELECT MAX(created_at, updated_at) AS latest_timestamp FROM goals
        ) 
        ORDER BY latest_timestamp DESC;
    """)

    # assemble a prompt for the user to select which date they want to recap

    latest_dates_prompt = "Input the number for the date you wish to recap:\n"

    # counter for easy user input

    entry_number = 0

    # variable to track the last date entry to avoid duplicates
    # REPLACE WITH BETTER SQL PULL?

    last_date_entry = ""

    entry_days = []

    while True:
        entry_number += 1
        if entry_number > 10:
            break
        date_entry = csr.fetchone()
        if date_entry is None:
            break
        formatted_date_entry = convert_sql_date_format_to_mdy(date_entry[0])
        if formatted_date_entry == last_date_entry:
            continue
        last_date_entry = formatted_date_entry
        entry_days.append(formatted_date_entry)
        latest_dates_prompt += f"{entry_number}. {formatted_date_entry}\n"

    print(latest_dates_prompt)

    while True:
        user_date_selection = int(input(">"))
        try:
            selected_date = entry_days[user_date_selection - 1]
            break
        except IndexError:
            print("Invalid selection. Please choose a valid number from the list.")

    # pull source table, id, created_at, and updated_at from all tables on the selected date

    csr.execute("""
        SELECT * FROM (
            SELECT 'general_entries' AS source_table, id, created_at, updated_at FROM general_entries WHERE DATE(created_at) = ? OR DATE(updated_at) = ?
            UNION ALL
            SELECT 'locations', id, created_at, updated_at FROM locations WHERE DATE(created_at) = ? OR DATE(updated_at) = ?
            UNION ALL
            SELECT 'npcs', id, created_at, updated_at FROM npcs WHERE DATE(created_at) = ? OR DATE(updated_at) = ?
            UNION ALL
            SELECT 'quests', id, created_at, updated_at FROM quests WHERE DATE(created_at) = ? OR DATE(updated_at) = ?
            UNION ALL
            SELECT 'goals', id, created_at, updated_at FROM goals WHERE DATE(created_at) = ? OR DATE(updated_at) = ?
        )
        ORDER BY MAX(created_at, updated_at) DESC;
                """)

    entries_on_selected_date = csr.fetchall()

    # pull individual entries from their respective tables and assemble them into objects

    assembled_entries = []

    for entry in entries_on_selected_date:
        if entry[0] == "general_entries":
            assembled_entry = pull_entry_by_id(entry[1])
        if entry[0] == "locations":
            assembled_entry = pull_location_by_id(entry[1])
        if entry[0] == "npcs":
            assembled_entry = pull_npc_by_id(entry[1])
        if entry[0] == "quests":
            assembled_entry = pull_quest_by_id(entry[1])
        if entry[0] == "goals":
            assembled_entry = pull_goal_by_id(entry[1])
        else:
            continue
        assembled_entries.append(assembled_entry)









# assembly functions

def assemble_entry(row: tuple[int, str, str, str, str, str]):
    return Entry(row[0], row[1], row[2], row[3], row[4], row[5])

def assemble_location(row: tuple[int, str, str, int|None, str, str, str]) -> Location:
    parent_location: Location = None
    if row[3] is not None:
        parent_location: Location = pull_location_by_id(row[3])
    return Location(row[0], row[1], row[2], row[4], row[5], row[6], parent_location)

def assemble_npc(row: tuple[int, str, str, int, str, str, str, str, str]):
    location: Location = None
    if row[3] is not None:
        location = pull_location_by_id(row[3])
    return NPC(row[0], row[1], row[2], row[6], row[7], row[8], location, row[4], row[5])

def assemble_quest(row: tuple[int, str, str, int|None, str, str, str, str]):
    giver: NPC = None
    goals: list[Goal] = []
    csr.execute("SELECT id FROM goals WHERE quest_id = ?;", (row[0],))
    goals_data: list[tuple[int]] = csr.fetchall()
    for id in goals_data:
        goals.append(pull_goal_by_id(id[0]))
    if row[3] is not None:
        giver: NPC = pull_npc_by_id(row[3])
    return Quest(row[0], row[1], row[2], row[6], row[7], row[8], goals, giver, row[5])

def pull_location_by_id(location_id):
    csr.execute("SELECT * FROM locations WHERE id = ?;", (location_id,))
    location_row = csr.fetchone()
    if location_row:
        return assemble_location(location_row)
    return None

def pull_npc_by_id(npc_id):
    csr.execute("SELECT * FROM npcs WHERE id = ?;", (npc_id,))
    npc_row = csr.fetchone()
    if npc_row:
        return assemble_npc(npc_row)
    return None

def pull_quest_by_id(quest_id):
    csr.execute("SELECT * FROM quests WHERE id = ?;", (quest_id,))
    quest_row = csr.fetchone()
    if quest_row:
        return assemble_quest(quest_row)
    return None

def pull_entry_by_id(entry_id):
    csr.execute("SELECT * FROM general_entries WHERE id = ?;", (entry_id,))
    entry_row = csr.fetchone()
    if entry_row:
        return assemble_entry(entry_row)
    return None

def pull_goal_by_id(goal_id):
    csr.execute("SELECT * FROM goals WHERE id = ?;", (goal_id,))
    goal_row = csr.fetchone()
    if goal_row:
        return Goal(goal_row[0], goal_row[1], goal_row[2])
    return None

# program functions

def close_program():
    print("Thank you for using the TRPG Quest Tracker!")
    cnx.close()
    sys.exit()