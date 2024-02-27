import datetime

class Event:
    def _init_(self, name, date, location):
        self.name = name
        self.date = date
        self.location = location

class EventManagementSystem:
    def _init_(self):
        self.events = []

    def add_event(self, name, date, location):
        event = Event(name, date, location)
        self.events.append(event)
        print(f"Event '{name}' added successfully!")

    def view_events(self):
        if not self.events:
            print("No events available.")
        else:
            print("List of Events:")
            for i, event in enumerate(self.events, start=1):
                print(f"{i}. {event.name} - Date: {event.date}, Location: {event.location}")

    def delete_event(self, index):
        try:
            event_name = self.events[index - 1].name
            del self.events[index - 1]
            print(f"Event '{event_name}' deleted successfully!")
        except IndexError:
            print("Invalid index. No event deleted.")

# Example usage
event_manager = EventManagementSystem()

while True:
    print("\nEvent Management System Menu:")
    print("1. Add Event")
    print("2. View Events")
    print("3. Delete Event")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        name = input("Enter event name: ")
        date_str = input("Enter event date (DD-MM-YYYY): ")
        location = input("Enter event location: ")

        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            event_manager.add_event(name, date, location)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    elif choice == '2':
        event_manager.view_events()

    elif choice == '3':
        event_manager.view_events()
        index_to_delete = input("Enter the index of the event to delete (0 to cancel): ")
        if index_to_delete.isdigit():
            index_to_delete = int(index_to_delete)
            if 0 < index_to_delete <= len(event_manager.events):
                event_manager.delete_event(index_to_delete)
            else:
                print("Invalid index. No event deleted.")
        else:
            print("Invalid input. No event deleted.")

    elif choice == '4':
        print("Exiting Event Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
import sqlite3

class EventManagementSystem:
    def _init_(self, db_name='events.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.events = []

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date DATE,
                location TEXT
            )
        ''')
        self.conn.commit()

    def add_event(self, name, date, location):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO events (name, date, location)
            VALUES (?, ?, ?)
        ''', (name, date, location))
        self.conn.commit()
        print(f"Event '{name}' added successfully!")

    def load_events(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, date, location FROM events')
        rows = cursor.fetchall()
        for row in rows:
            event = Event(row[1], row[2], row[3])
            self.events.append(event)

    def view_events(self):
        if not self.events:
            print("No events available.")
        else:
            print("List of Events:")
            for i, event in enumerate(self.events, start=1):
                print(f"{i}. {event.name} - Date: {event.date}, Location: {event.location}")

    def delete_event(self, index):
        try:
            event_name = self.events[index - 1].name
            event_id = index
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            self.conn.commit()
            print(f"Event '{event_name}' deleted successfully!")
        except IndexError:
            print("Invalid index. No event deleted.")