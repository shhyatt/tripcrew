-- USERS
INSERT INTO users (id, first_name, last_name, email, password_hash) VALUES
(1, 'Sam', 'Hyatt', 'sam@example.com', 'hashed_pw_1'),
(2, 'Alex', 'Rivera', 'alex@example.com', 'hashed_pw_2'),
(3, 'Jordan', 'Lee', 'jordan@example.com', 'hashed_pw_3'),
(4, 'Taylor', 'Smith', 'taylor@example.com', 'hashed_pw_4');

-- TRIPS
INSERT INTO trips (id, owner_user_id, trip_name, description, start_date, end_date) VALUES
(1, 1, 'Santa Fe Trip', 'Long weekend trip with friends', '2026-06-10', '2026-06-13');

-- TRIP MEMBERS
INSERT INTO trip_members (trip_id, user_id, role) VALUES
(1, 1, 'owner'),
(1, 2, 'member'),
(1, 3, 'member'),
(1, 4, 'member');

-- TRIP DESTINATIONS
INSERT INTO trip_destinations (id, trip_id, location_name, start_date, end_date, order_index) VALUES
(1, 1, 'Santa Fe', '2026-06-10', '2026-06-13', 1);

-- ITINERARY ITEMS
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
) VALUES
(1, 1, 'Meow Wolf Visit', 'Immersive art experience', 'activity', 'Meow Wolf Santa Fe', '2026-06-10', '2026-06-10 10:00:00', '2026-06-10 12:00:00', 1),

(1, 1, 'Dinner at La Choza', 'Authentic New Mexican food', 'food', 'La Choza Restaurant', '2026-06-10', '2026-06-10 18:30:00', '2026-06-10 20:00:00', 2),

(1, 1, 'Ojo Santa Fe Spa Day', 'Relax at hot springs', 'relaxation', 'Ojo Santa Fe', '2026-06-11', '2026-06-11 11:00:00', '2026-06-11 15:00:00', 3);

-- TRIP CHECKLIST ITEMS
INSERT INTO trip_checklist_items (trip_id, title, is_completed) VALUES
(1, 'Book Airbnb', true),
(1, 'Pack clothes', false),
(1, 'Bring hiking shoes', false),
(1, 'Confirm reservations', true);

-- TRIP IDEA ITEMS (want-to-go list)
INSERT INTO trip_idea_items (
  trip_id,
  title,
  description,
  category,
  location_name,
  proposed_date,
  must_do,
  created_by_user_id
) VALUES
(1, 'Brewery Crawl', 'Visit multiple local breweries', 'activity', 'Santa Fe', '2026-06-12', false, 4),

(1, 'Sunset Hike', 'Easy hike with a sunset view', 'outdoors', 'Dale Ball Trails', '2026-06-12', true, 2),

(1, 'Chocolate Shop Stop', 'Check out local chocolate shops', 'food', 'Downtown Santa Fe', NULL, false, 3);