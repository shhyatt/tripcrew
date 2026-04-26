from fastapi import FastAPI, HTTPException
from database import get_connection

app = FastAPI()

# simple test endpoint
@app.get("/")
def home():
    return {"message": "TripCrew API is running"}


# GET all trips
@app.get("/trips")
def get_trips():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            trips.id,
            trips.trip_name,
            trips.description,
            trips.start_date,
            trips.end_date,
            users.first_name || ' ' || users.last_name AS owner_name
        FROM trips
        JOIN users ON trips.owner_user_id = users.id
        ORDER BY trips.id;
    """)

    trips = cur.fetchall()

    cur.close()
    conn.close()

    return trips


@app.get("/trips/{trip_id}")
def get_trip(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            trips.id,
            trips.trip_name,
            trips.description,
            trips.start_date,
            trips.end_date,
            users.first_name || ' ' || users.last_name AS owner_name
        FROM trips
        JOIN users ON trips.owner_user_id = users.id
        WHERE trips.id = %s;
    """, (trip_id,))

    trip = cur.fetchone()

    cur.close()
    conn.close()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip