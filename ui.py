def main_menu():
    while True:
        print("1. Add a new entry\n2. See a previous entry\n3. Last session recap")
        match input("Select: "):
            case "1": create_entry()
            case "2": view_entry()
            case "3": recap()
            case _: print("Invalid choice")

