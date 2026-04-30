import { useEffect, useState } from "react";
import TripCard from "../components/TripCard";


function Dashboard() {
  const [trips, setTrips] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/trips`)
      .then((response) => response.json())
      .then((data) => setTrips(data));
  }, []);

  return (
    <div>
      <h1>Upcoming Trips</h1>

      {trips.map((trip) => (
        <TripCard key={trip.id} trip={trip} />
      ))}
    </div>
  );
}

export default Dashboard;