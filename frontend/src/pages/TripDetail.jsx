import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function TripDetail() {
  const { tripId } = useParams();
  const [trip, setTrip] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/trips/${tripId}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("DATA:", data);
        setTrip(data)
      });
  }, [tripId]);

  if (!trip) return <p>Loading trip...</p>;

  return (
    <div>
      <h1>{trip.trip.trip_name}</h1>

      {/* Destinations */}
      <section>
        <h2>Destinations</h2>
         <button onClick={() => navigate(`/trips/${trip.trip.id}/new_destination`)}>
          Add Destination</button>
      </section>

      {/* Itinerary */}
      <section>
        <h2>Itinerary</h2>
        <button>Add Item</button>
      </section>

      {/* Want To Do */}
      <section>
        <h2>Want To Do</h2>
        <button>Add Idea</button>
      </section>
    </div>
  );
}

export default TripDetail;