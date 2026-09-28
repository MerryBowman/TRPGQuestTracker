from db_interact import create_general_entry, create_location, create_npc, create_quest, create_goal, view_entry, close_program, recap
import sys

def main_menu():
    while True:
        print("1. Add a new entry\n2. See a previous entry\n3. Last session recap\n4. Close program")
        match input("Select: "):
            case "1": return create_entry()
            case "2": return view_entry()
            case "3": return recap()
            case "4": return close_program()
            case _: print("Invalid choice")

def create_entry():
    while True:
        print("1. General entry\n2. Location\n3. NPC\n4. Quest\n5. Quest Goal\n6. Back to main menu")
        match input("Select: "):
            case "1": return create_general_entry()
            case "2": return create_location()
            case "3": return create_npc()
            case "4": return create_quest()
            case "5": return create_goal()
            case "6": return main_menu()
            case _: print("Invalid choice")