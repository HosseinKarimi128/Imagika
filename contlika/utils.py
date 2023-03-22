import sqlite3
import json
import random
import time

def clean_db():
    conn = sqlite3.connect('db.sqlite3')

    # Disable foreign key checks
    conn.execute('PRAGMA foreign_keys = OFF;')

    # Get a list of all tables
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';").fetchall()

    # Delete all records from each table
    for table in tables:
        if table[0].startswith("celestial"):
            conn.execute(f"DELETE FROM {table[0]};")

    # Enable foreign key checks
    conn.execute('PRAGMA foreign_keys = ON;')

    conn.commit()
    conn.close()

def test_json_load_speed():

    data = [random.randint(1, 100) for _ in range(10000000)]
    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    start_time = time.time()

    with open('data.json', 'r') as f:
        data = json.load(f)
    s = 's'
    l = []
    for i in data:
        if str(i) != s:
            l.append(str(i))
    end_time = time.time()

    print(f"Loaded {len(data)} items in {end_time - start_time:.2f} seconds")