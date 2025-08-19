import sqlite3
from dotenv import load_dotenv
from main import db, Cafes, app

# Load environment variables
load_dotenv()

# Connect to SQLite
sqlite_conn = sqlite3.connect("instance/cafes.db")
sqlite_cursor = sqlite_conn.cursor()

# Fetch all cafes from the SQLite DB
sqlite_cursor.execute("SELECT * FROM cafe")
rows = sqlite_cursor.fetchall()

print(f"Found {len(rows)} cafes in SQLite DB.")

# Insert into PostgreSQL (Neon)
with app.app_context():
    for row in rows:
        # Skip if cafe with same name already exists in PostgreSQL
        if Cafes.query.filter_by(name=row[1]).first():
            continue

        
        # Handle 'seats' values like "40-50", "50+", or integers
        seats_str = str(row[9]) if row[9] is not None else ""
        seats = int(seats_str.split("-")[0]) if "-" in seats_str else (int(seats_str) if seats_str.isdigit() else None)

        new_cafe = Cafes(
            id=row[0],
            name=row[1],
            map_url=row[2],
            img_url=row[3],
            location=row[4],
            has_sockets=bool(row[5]),
            has_toilet=bool(row[6]),
            has_wifi=bool(row[7]),
            can_take_calls=bool(row[8]),
            seats=seats,
            coffee_price=row[10],
        )
        db.session.add(new_cafe)

    db.session.commit()

print("✅ Migration complete.")
