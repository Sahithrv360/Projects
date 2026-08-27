import sqlite3
import os

DB_PATH = "database/ai_cam.db"


def create_database():

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            camera_id TEXT,
            event_type TEXT,
            object_id INTEGER,
            zone TEXT,
            severity TEXT,
            snapshot TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_event(
    timestamp,
    camera_id,
    event_type,
    object_id,
    zone,
    severity,
    snapshot
):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (
            timestamp,
            camera_id,
            event_type,
            object_id,
            zone,
            severity,
            snapshot
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        camera_id,
        event_type,
        object_id,
        zone,
        severity,
        snapshot
    ))

    connection.commit()
    connection.close()