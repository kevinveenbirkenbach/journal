import sqlite3
from tkinter import *

# Create connection to SQLite database
conn = sqlite3.connect('journal.db')
c = conn.cursor()

# Create tables
c.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        start_time TEXT NOT NULL,
        end_time TEXT,
        description TEXT,
        location_id INTEGER,
        FOREIGN KEY(location_id) REFERENCES location(id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS location (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        latitude REAL,
        longitude REAL
    )
''')

# Commit and close connection
conn.commit()
conn.close()

# Create GUI
root = Tk()

# Frames
entry_frame = Frame(root)
entry_frame.pack()
location_frame = Frame(root)
location_frame.pack()
display_frame = Frame(root)
display_frame.pack()

# Entry Widgets
Label(entry_frame, text="Start Time:").pack()
start_time_entry = Entry(entry_frame)
start_time_entry.pack()

Label(entry_frame, text="End Time:").pack()
end_time_entry = Entry(entry_frame)
end_time_entry.pack()

Label(entry_frame, text="Description:").pack()
description_entry = Entry(entry_frame)
description_entry.pack()

Label(entry_frame, text="Location ID:").pack()
location_id_entry = Entry(entry_frame)
location_id_entry.pack()

# Location Widgets
Label(location_frame, text="Location Name:").pack()
location_name_entry = Entry(location_frame)
location_name_entry.pack()

Label(location_frame, text="Latitude:").pack()
latitude_entry = Entry(location_frame)
latitude_entry.pack()

Label(location_frame, text="Longitude:").pack()
longitude_entry = Entry(location_frame)
longitude_entry.pack()

# Listbox to display entries
listbox = Listbox(display_frame)
listbox.pack()

# Functions to add entries and refresh display
def add_entry():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('INSERT INTO entries (start_time, end_time, description, location_id) VALUES (?, ?, ?, ?)',
              (start_time_entry.get(), end_time_entry.get(), description_entry.get(), location_id_entry.get()))
    conn.commit()
    conn.close()
    refresh_display()

def add_location():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('INSERT INTO location (name, latitude, longitude) VALUES (?, ?, ?)',
              (location_name_entry.get(), latitude_entry.get(), longitude_entry.get()))
    conn.commit()
    conn.close()

def refresh_display():
    # Clear the listbox
    listbox.delete(0, END)

    # Get data from database
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    rows = c.execute('SELECT * FROM entries').fetchall()
    conn.close()

    # Add data to listbox
    for row in rows:
        listbox.insert(END, row)

# Buttons
Button(entry_frame, text="Add Entry", command=add_entry).pack()
Button(location_frame, text="Add Location", command=add_location).pack()

root.mainloop()
