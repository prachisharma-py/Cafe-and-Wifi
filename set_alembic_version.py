from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///instance/cafes.db")

with engine.connect() as conn:
    conn.execute(
        text("UPDATE alembic_version SET version_num = :rev"),
        {"rev": "5c89f95a5dde"}
    )
    conn.commit()

print("Alembic version updated successfully.")
