-- Locations table

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

-- NPCs table

CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    location_id INTEGER,
    status VARCHAR(10) DEFAULT "UNKNOWN",
    pc_relationship VARCHAR(10) DEFAULT "NEUTRAL",
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

-- Quests table

CREATE TABLE IF NOT EXISTS quests (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    giver_id INTEGER,
    status VARCHAR(10) DEFAULT "ACTIVE",
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

-- Goals table

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY,
    quest_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(10) DEFAULT "ACTIVE",
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
    CONSTRAINT fk_quest_id FOREIGN KEY (quest_id) REFERENCES quests(id)
);

CREATE TRIGGER IF NOT EXISTS update_goal_timestamp AFTER UPDATE ON goals
FOR EACH ROW
BEGIN
    UPDATE goals SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- General Entries table

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

-- Relational tables

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



/* 

OLD SCHEMA TO USE WHEN UPDATING

# NPCs table

CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    location_id INTEGER,
    status ENUM("alive", "dead", "unknown") DEFAULT "unknown",
    pc_relationship ENUM("ally", "friendly", "neutral", "hostile") DEFAULT "neutral",
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
    CONSTRAINT fk_location_id FOREIGN KEY (location_id) REFERENCES locations(id),
);

CREATE TRIGGER IF NOT EXISTS update_npc_timestamp AFTER UPDATE ON npcs
FOR EACH ROW
BEGIN
    UPDATE npcs SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

# Locations table

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    parent_location_id INTEGER DEFAULT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
    CONSTRAINT fk_parent_location_id FOREIGN KEY (parent_location_id) REFERENCES locations(id),
);

CREATE TRIGGER IF NOT EXISTS update_location_timestamp AFTER UPDATE ON locations
FOR EACH ROW
BEGIN
    UPDATE locations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

# Quests table

CREATE TABLE IF NOT EXISTS quests (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    goals TEXT,
    giver_id INTEGER,
    status ENUM("active", "completed", "failed", "abandoned") DEFAULT "active",
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
    CONSTRAINT fk_giver_id FOREIGN KEY (giver_id) REFERENCES npcs(id),
);

CREATE TRIGGER IF NOT EXISTS update_quest_timestamp AFTER UPDATE ON quests
FOR EACH ROW
BEGIN
    UPDATE quests SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

# General Entries table

CREATE TABLE IF NOT EXISTS general_entries (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    deleted_at TEXT DEFAULT "9999-12-31 23:59:59",
);

CREATE TRIGGER IF NOT EXISTS update_general_entry_timestamp AFTER UPDATE ON general_entries
FOR EACH ROW
BEGIN
    UPDATE general_entries SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

# Relational tables

CREATE TABLE IF NOT EXISTS entries_x_npcs (
    id INTEGER PRIMARY KEY,
    entry_id INTEGER,
    npc_id INTEGER,
    FOREIGN KEY (entry_id) REFERENCES general_entries(id),
    FOREIGN KEY (npc_id) REFERENCES npcs(id),
);

CREATE TABLE IF NOT EXISTS entries_x_locations (
    id INTEGER PRIMARY KEY,
    entry_id INTEGER,
    location_id INTEGER,
    FOREIGN KEY (entry_id) REFERENCES general_entries(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
);

CREATE TABLE IF NOT EXISTS entries_x_quests (
    id INTEGER PRIMARY KEY,
    entry_id INTEGER,
    quest_id INTEGER,
    FOREIGN KEY (entry_id) REFERENCES general_entries(id),
    FOREIGN KEY (quest_id) REFERENCES quests(id),
);

CREATE TABLE IF NOT EXISTS quests_x_locations (
    id INTEGER PRIMARY KEY,
    quest_id INTEGER,
    location_id INTEGER,
    FOREIGN KEY (quest_id) REFERENCES quests(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
);

CREATE TABLE IF NOT EXISTS quests_x_npcs (
    id INTEGER PRIMARY KEY,
    quest_id INTEGER,
    npc_id INTEGER,
    FOREIGN KEY (quest_id) REFERENCES quests(id),
    FOREIGN KEY (npc_id) REFERENCES npcs(id),
);

CREATE TABLE IF NOT EXISTS npcs_x_locations (
    id INTEGER PRIMARY KEY,
    npc_id INTEGER,
    location_id INTEGER,
    FOREIGN KEY (npc_id) REFERENCES npcs(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
);

*/