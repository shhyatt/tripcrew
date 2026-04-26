from fastapi import FastAPI, HTTPException
from database import get_connection
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password_hash: str

class TripCreate(BaseModel):
    owner_user_id: int
    trip_name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class DestinationCreate(BaseModel):
    trip_id: int
    location_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    order_index: Optional[int] = None

class ItineraryItemCreate(BaseModel):
    trip_id: int
    trip_destination_id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location_name: Optional[str] = None
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    created_by_user_id: Optional[int] = None

class TripIdeaCreate(BaseModel):
    trip_id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    location_name: Optional[str] = None
    proposed_date: Optional[str] = None
    must_do: bool = False
    created_by_user_id: Optional[int] = None

class ChecklistItemCreate(BaseModel):
    trip_id: int
    title: str
    is_completed: bool = False

class TripMemberCreate(BaseModel):
    trip_id: int
    user_id: int
    role: Optional[str] = "member"


# simple test endpoint
@app.get("/")
def home():
    return {"message": "TripCrew API is running"}

# Get all users 

@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id,
            first_name,
            last_name,
            email,
            created_at
        FROM users
        ORDER BY id;
    """)

    users = cur.fetchall()

    cur.close()
    conn.close()

    return users

# Get one user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            id,
            first_name,
            last_name,
            email,
            created_at
        FROM users
        WHERE id = %s;
    """, (user_id,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

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

# get one trip 

# @app.get("/trips/{trip_id}")
# def get_trip(trip_id: int):
#     conn = get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT 
#             trips.id,
#             trips.trip_name,
#             trips.description,
#             trips.start_date,
#             trips.end_date,
#             users.first_name || ' ' || users.last_name AS owner_name
#         FROM trips
#         JOIN users ON trips.owner_user_id = users.id
#         WHERE trips.id = %s;
#     """, (trip_id,))

#     trip = cur.fetchone()

#     cur.close()
#     conn.close()

#     if not trip:
#         raise HTTPException(status_code=404, detail="Trip not found")

#     return trip

@app.get("/trips/{trip_id}")
def get_trip_details(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # 1. Trip
    cur.execute("""
        SELECT * FROM trips WHERE id = %s;
    """, (trip_id,))
    trip = cur.fetchone()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # 2. Members
    cur.execute("""
        SELECT u.*
        FROM trip_members tm
        JOIN users u ON tm.user_id = u.id
        WHERE tm.trip_id = %s;
    """, (trip_id,))
    members = cur.fetchall()

    # 3. Destinations
    cur.execute("""
        SELECT *
        FROM trip_destinations
        WHERE trip_id = %s
        ORDER BY start_date;
    """, (trip_id,))
    destinations = cur.fetchall()

    # 4. Itinerary Items
    cur.execute("""
        SELECT *
        FROM itinerary_items
        WHERE trip_id = %s
        ORDER BY date, start_time
    """, (trip_id,))
    itinerary_items = cur.fetchall()

    # 5. Checklists
    cur.execute("""
        SELECT *
        FROM trip_checklist_items
        WHERE trip_id = %s;
    """, (trip_id,))
    checklists = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "trip": trip,
        "members": members,
        "destinations": destinations,
        "itinerary_items": itinerary_items,
        "checklists": checklists
    }

#get trip members

@app.get("/trips/{trip_id}/members")
def get_trip_members(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            users.id,
            users.first_name,
            users.last_name,
            users.email,
            trip_members.role,
            trip_members.joined_at
        FROM trip_members
        JOIN users ON trip_members.user_id = users.id
        WHERE trip_members.trip_id = %s
        ORDER BY users.id;
    """, (trip_id,))

    members = cur.fetchall()

    cur.close()
    conn.close()

    return members

#Get one trip member

@app.get("/checklist-items/{item_id}")
def get_checklist_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_checklist_items
        WHERE id = %s;
    """, (item_id,))

    item = cur.fetchone()

    cur.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    return item

#get itinerarys

@app.get("/trips/{trip_id}/itinerary")
def get_trip_itinerary(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM itinerary_items
        WHERE trip_id = %s
        ORDER BY date, start_time;
    """, (trip_id,))

    itinerary = cur.fetchall()

    cur.close()
    conn.close()

    return itinerary

# Get one itinerary item 

@app.get("/itinerary-items/{item_id}")
def get_itinerary_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM itinerary_items
        WHERE id = %s;
    """, (item_id,))

    item = cur.fetchone()

    cur.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")

    return item

# get idea items

@app.get("/trips/{trip_id}/ideas")
def get_trip_ideas(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_idea_items
        WHERE trip_id = %s
        ORDER BY created_at;
    """, (trip_id,))

    ideas = cur.fetchall()

    cur.close()
    conn.close()

    return ideas

# get one idea item

@app.get("/ideas/{idea_id}")
def get_idea(idea_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_idea_items
        WHERE id = %s;
    """, (idea_id,))

    idea = cur.fetchone()

    cur.close()
    conn.close()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return idea

#Get destinations

@app.get("/trips/{trip_id}/destinations")
def get_trip_destinations(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_destinations
        WHERE trip_id = %s
        ORDER BY order_index;
    """, (trip_id,))

    destinations = cur.fetchall()

    cur.close()
    conn.close()

    return destinations

# get one destination

@app.get("/destinations/{destination_id}")
def get_destination(destination_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_destinations
        WHERE id = %s;
    """, (destination_id,))

    destination = cur.fetchone()

    cur.close()
    conn.close()

    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    return destination

# Get Checklist

@app.get("/trips/{trip_id}/checklist")
def get_trip_checklist(trip_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_checklist_items
        WHERE trip_id = %s
        ORDER BY id;
    """, (trip_id,))

    checklist = cur.fetchall()

    cur.close()
    conn.close()

    return checklist

#get one checklist item

@app.get("/checklist-items/{item_id}")
def get_checklist_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM trip_checklist_items
        WHERE id = %s;
    """, (item_id,))

    item = cur.fetchone()

    cur.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    return item

#Posts

# post Users

@app.post("/users")
def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (
            first_name,
            last_name,
            email,
            password_hash
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id, first_name, last_name, email, created_at;
    """, (
        user.first_name,
        user.last_name,
        user.email,
        user.password_hash
    ))

    new_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_user

# post Trips

@app.post("/trips")
def create_trip(trip: TripCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trips (
            owner_user_id,
            trip_name,
            description,
            start_date,
            end_date
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        trip.owner_user_id,
        trip.trip_name,
        trip.description,
        trip.start_date,
        trip.end_date
    ))

    new_trip = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_trip

#post itinerary item

@app.post("/itinerary-items")
def create_itinerary_item(item: ItineraryItemCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO itinerary_items (
            trip_id,
            trip_destination_id,
            title,
            description,
            category,
            location_name,
            date,
            start_time,
            end_time,
            created_by_user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        item.trip_id,
        item.trip_destination_id,
        item.title,
        item.description,
        item.category,
        item.location_name,
        item.date,
        item.start_time,
        item.end_time,
        item.created_by_user_id
    ))

    new_item = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_item

# post Ideas

@app.post("/ideas")
def create_trip_idea(idea: TripIdeaCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trip_idea_items (
            trip_id,
            title,
            description,
            category,
            location_name,
            proposed_date,
            must_do,
            created_by_user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        idea.trip_id,
        idea.title,
        idea.description,
        idea.category,
        idea.location_name,
        idea.proposed_date,
        idea.must_do,
        idea.created_by_user_id
    ))

    new_idea = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_idea

# post checklist items

@app.post("/checklist-items")
def create_checklist_item(item: ChecklistItemCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trip_checklist_items (
            trip_id,
            title,
            is_completed
        )
        VALUES (%s, %s, %s)
        RETURNING *;
    """, (
        item.trip_id,
        item.title,
        item.is_completed
    ))

    new_item = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_item

# post destinations

@app.post("/destinations")
def create_destination(destination: DestinationCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trip_destinations (
            trip_id,
            location_name,
            start_date,
            end_date,
            order_index
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        destination.trip_id,
        destination.location_name,
        destination.start_date,
        destination.end_date,
        destination.order_index
    ))

    new_destination = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_destination

#post trip members 

@app.post("/trip-members")
def add_trip_member(member: TripMemberCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO trip_members (
            trip_id,
            user_id,
            role
        )
        VALUES (%s, %s, %s)
        RETURNING *;
    """, (
        member.trip_id,
        member.user_id,
        member.role
    ))

    new_member = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return new_member

# Updates

#update idea

@app.put("/ideas/{idea_id}")
def update_idea(idea_id: int, idea: TripIdeaCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE trip_idea_items
        SET title = %s,
            description = %s,
            category = %s,
            location_name = %s,
            proposed_date = %s,
            must_do = %s,
            created_by_user_id = %s
        WHERE id = %s
        RETURNING *;
    """, (
        idea.title,
        idea.description,
        idea.category,
        idea.location_name,
        idea.proposed_date,
        idea.must_do,
        idea.created_by_user_id,
        idea_id
    ))

    updated_idea = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return updated_idea

#update checklist item

@app.put("/checklist-items/{item_id}")
def update_checklist_item(item_id: int, item: ChecklistItemCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE trip_checklist_items
        SET title = %s,
            is_completed = %s
        WHERE id = %s
        RETURNING *;
    """, (
        item.title,
        item.is_completed,
        item_id
    ))

    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    return updated_item

#update itinerary item

@app.put("/itinerary-items/{item_id}")
def update_itinerary_item(item_id: int, item: ItineraryItemCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE itinerary_items
        SET trip_id = %s,
            trip_destination_id = %s,
            title = %s,
            description = %s,
            category = %s,
            location_name = %s,
            date = %s,
            start_time = %s,
            end_time = %s,
            created_by_user_id = %s
        WHERE id = %s
        RETURNING *;
    """, (
        item.trip_id,
        item.trip_destination_id,
        item.title,
        item.description,
        item.category,
        item.location_name,
        item.date,
        item.start_time,
        item.end_time,
        item.created_by_user_id,
        item_id
    ))

    updated_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")

    return updated_item

#update destination

@app.put("/destinations/{destination_id}")
def update_destination(destination_id: int, destination: DestinationCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE trip_destinations
        SET trip_id = %s,
            location_name = %s,
            start_date = %s,
            end_date = %s,
            order_index = %s
        WHERE id = %s
        RETURNING *;
    """, (
        destination.trip_id,
        destination.location_name,
        destination.start_date,
        destination.end_date,
        destination.order_index,
        destination_id
    ))

    updated_destination = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    return updated_destination

# update trip member

@app.put("/trip-members/{member_id}")
def update_trip_member(member_id: int, member: TripMemberCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE trip_members
        SET trip_id = %s,
            user_id = %s,
            role = %s
        WHERE id = %s
        RETURNING *;
    """, (
        member.trip_id,
        member.user_id,
        member.role,
        member_id
    ))

    updated_member = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated_member:
        raise HTTPException(status_code=404, detail="Trip member not found")

    return updated_member

#deletes

#delete idea 

@app.delete("/ideas/{idea_id}")
def delete_idea(idea_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM trip_idea_items
        WHERE id = %s
        RETURNING *;
    """, (idea_id,))

    deleted_idea = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted_idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return {"message": "Idea deleted", "deleted_idea": deleted_idea}

#delete checklist item 

@app.delete("/checklist-items/{item_id}")
def delete_checklist_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM trip_checklist_items
        WHERE id = %s
        RETURNING *;
    """, (item_id,))

    deleted_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted_item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    return {"message": "Checklist item deleted", "deleted_item": deleted_item}

# delete itinerary item

@app.delete("/itinerary-items/{item_id}")
def delete_itinerary_item(item_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM itinerary_items
        WHERE id = %s
        RETURNING *;
    """, (item_id,))

    deleted_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted_item:
        raise HTTPException(status_code=404, detail="Itinerary item not found")

    return {"message": "Itinerary item deleted", "deleted_item": deleted_item}

#delete destinations

@app.delete("/destinations/{destination_id}")
def delete_destination(destination_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM trip_destinations
        WHERE id = %s
        RETURNING *;
    """, (destination_id,))

    deleted_destination = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted_destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    return {"message": "Destination deleted", "deleted_destination": deleted_destination}

#delete trip member

@app.delete("/trip-members/{member_id}")
def delete_trip_member(member_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM trip_members
        WHERE id = %s
        RETURNING *;
    """, (member_id,))

    deleted_member = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not deleted_member:
        raise HTTPException(status_code=404, detail="Trip member not found")

    return {"message": "Trip member deleted", "deleted_member": deleted_member}




