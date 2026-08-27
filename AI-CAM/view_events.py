import sqlite3

connection = sqlite3.connect(
    "database/ai_cam.db"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        timestamp,
        camera_id,
        event_type,
        object_id,
        zone,
        severity
    FROM events
    ORDER BY id DESC
""")

events = cursor.fetchall()

print("\nAI-CAM SECURITY EVENTS")
print("-" * 90)

for event in events:

    print(
        f"ID: {event[0]} | "
        f"Time: {event[1]} | "
        f"Camera: {event[2]} | "
        f"Event: {event[3]} | "
        f"Object: {event[4]} | "
        f"Zone: {event[5]} | "
        f"Severity: {event[6]}"
    )

connection.close()