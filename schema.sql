CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	first_name VARCHAR(100),
	last_name VARCHAR(100),
	email VARCHAR(255) UNIQUE NOT NULL,
	password_hash TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trips (
	id SERIAL PRIMARY KEY,
	owner_user_id INTEGER NOT NULL,
	trip_name VARCHAR(255) NOT NULL,
	description TEXT,
	start_date DATE,
	end_date DATE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_trips_owner
		FOREIGN KEY (owner_user_id)
		REFERENCES users(id)
		ON DELETE CASCADE
);

CREATE TABLE trip_members (
	id SERIAL PRIMARY KEY,
	trip_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	role VARCHAR(50) DEFAULT 'member',
	joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_trip_members_trip
		FOREIGN KEY (trip_id)
		REFERENCES trips(id)
		ON DELETE CASCADE,

	CONSTRAINT fk_trip_members_user
		FOREIGN KEY (user_id)
		REFERENCES users(id)
		ON DELETE CASCADE,

	CONSTRAINT unique_trip_member
		UNIQUE (trip_id, user_id)
);

CREATE TABLE trip_destinations (
	id SERIAL PRIMARY KEY,
	trip_id INTEGER NOT NULL,
	location_name VARCHAR(255) NOT NULL,
	start_date DATE,
	end_date DATE,
	order_index INTEGER,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_trip_destinations_trip
		FOREIGN KEY (trip_id)
		REFERENCES trips(id)
		ON DELETE CASCADE
);

CREATE TABLE itinerary_items (
	id SERIAL PRIMARY KEY,
	trip_id INTEGER NOT NULL,
	trip_destination_id INTEGER NOT NULL,
	title VARCHAR(255) NOT NULL,
	description TEXT,
	category VARCHAR(50),
	location_name VARCHAR(255),
	date DATE,
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	created_by_user_id INTEGER,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_itinerary_trip
		FOREIGN KEY (trip_id)
		REFERENCES trips(id)
		ON DELETE CASCADE,

	CONSTRAINT fk_itinerary_destination
		FOREIGN KEY (trip_destination_id)
		REFERENCES trip_destinations(id)
		ON DELETE CASCADE,

	CONSTRAINT fk_itinerary_user
		FOREIGN KEY (created_by_user_id)
		REFERENCES users(id)
		ON DELETE SET NULL
);

CREATE TABLE trip_checklist_items (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_checklist_trip
        FOREIGN KEY (trip_id)
        REFERENCES trips(id)
        ON DELETE CASCADE
);

CREATE TABLE trip_idea_items (
	id SERIAL PRIMARY KEY,
	trip_id INTEGER NOT NULL,
	title VARCHAR(255),
	description TEXT,
	category VARCHAR(50),
	location_name VARCHAR(255),
	proposed_date DATE,
	must_do BOOLEAN DEFAULT FALSE,
	created_by_user_id INTEGER,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_ideas_trip
		FOREIGN KEY (trip_id)
		REFERENCES trips(id)
		ON DELETE CASCADE,

	CONSTRAINT fk_ideas_user
		FOREIGN KEY (created_by_user_id)
		REFERENCES users(id)
		ON DELETE SET NULL
);
















