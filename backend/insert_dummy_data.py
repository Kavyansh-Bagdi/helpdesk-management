import sqlite3
import bcrypt

# --- Configuration ---
DB_NAME = 'data.db'

# --- Data ---
users_to_insert = [
    {
        "username": "alice_admin",
        "email": "alice.a@example.com",
        "password": "securepassword123",
        "role": "admin"
    },
    {
        "username": "bob_agent",
        "email": "bob.b@example.com",
        "password": "agentpassword456",
        "role": "agent"
    },
    {
        "username": "charlie_customer",
        "email": "charlie.c@example.com",
        "password": "customerpassword789",
        "role": "customer"
    },
    {
        "username": "diana_customer",
        "email": "diana.d@example.com",
        "password": "anotherpassword101",
        "role": "customer"
    }
]

tickets_to_insert = [
    {
        "title": "Login Issue on Mobile App",
        "description": "I'm unable to log into my account using the Android app. It keeps saying 'Authentication Failed' even with the correct password.",
        "status": "open",
        "author_id": 3 # Charlie Customer
    },
    {
        "title": "Feature Request: Dark Mode",
        "description": "The dashboard is very bright. It would be great to have a dark mode option to reduce eye strain, especially at night.",
        "status": "in_progress",
        "author_id": 4 # Diana Customer
    },
    {
        "title": "Billing Discrepancy",
        "description": "I was charged twice for my subscription this month. Can you please investigate and refund the extra charge?",
        "status": "closed",
        "author_id": 3 # Charlie Customer
    }
]

comments_to_insert = [
    {
        "text": "Hi Charlie, I've received your ticket. Could you please confirm which version of the Android app you are using?",
        "author_id": 2, # Bob Agent
        "ticket_id": 1
    },
    {
        "text": "Thanks for the suggestion, Diana! We've added this to our development backlog and are actively looking into it.",
        "author_id": 2, # Bob Agent
        "ticket_id": 2
    },
    {
        "text": "I'm using version 2.5.1.",
        "author_id": 3, # Charlie Customer
        "ticket_id": 1
    },
    {
        "text": "Hi Charlie, we've investigated the billing issue and confirmed a duplicate charge. A refund has been processed and should appear in your account within 3-5 business days. We apologize for the inconvenience.",
        "author_id": 1, # Alice Admin
        "ticket_id": 3
    }
]


# --- Database Operations ---
def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def main():
    """Connects to the DB and inserts dummy data."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Insert Users
        print("Inserting users...")
        for user in users_to_insert:
            hashed_pw = hash_password(user["password"])
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (user["username"], user["email"], hashed_pw, user["role"])
            )
        print(f"  -> Inserted {len(users_to_insert)} users.")

        # Insert Tickets
        print("\nInserting tickets...")
        for ticket in tickets_to_insert:
            cursor.execute(
                "INSERT INTO tickets (title, description, status, author_id) VALUES (?, ?, ?, ?)",
                (ticket["title"], ticket["description"], ticket["status"], ticket["author_id"])
            )
        print(f"  -> Inserted {len(tickets_to_insert)} tickets.")

        # Insert Comments
        print("\nInserting comments...")
        for comment in comments_to_insert:
            cursor.execute(
                "INSERT INTO comments (text, author_id, ticket_id) VALUES (?, ?, ?)",
                (comment["text"], comment["author_id"], comment["ticket_id"])
            )
        print(f"  -> Inserted {len(comments_to_insert)} comments.")

        conn.commit()
        print("\nDummy data inserted successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
