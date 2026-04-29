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
      <h2>{trip.name}</h2>
      <p>{trip.location}</p>
      <p>{trip.startDate} - {trip.endDate}</p>
    </div>
  );
}

export default TripCard;