import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('customer', 'agent', 'admin'))
)
""")

# Create Tickets table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('open', 'in_progress', 'closed')),
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id)
)
""")

# Create Comments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    ticket_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users (id),
    FOREIGN KEY (ticket_id) REFERENCES tickets (id)
)
""")

# Create TicketImages table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    image_data BLOB NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets (id)
)
""")

print("Database and tables created successfully.")

connection.commit()
connection.close()
