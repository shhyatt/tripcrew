import { useNavigate } from "react-router-dom";

function TripCard({ trip }) {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate(`/trips/${trip.id}`)}
      style={{
        border: "1px solid #ccc",
        padding: "16px",
        marginBottom: "12px",
        borderRadius: "8px",
        cursor: "pointer"
      }}
    >
      <h2>{trip.trip_name}</h2>
      <p>{trip.description}</p>
      <p>{trip.start_date} - {trip.end_date}</p>
      <p>Owner: {trip.owner_name}</p>
    </div>
  );
}

export default TripCard;