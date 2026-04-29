import { useParams } from "react-router-dom";

function TripDetail() {
  const { tripId } = useParams();

  return (
    <div>
      <h1>Trip {tripId}</h1>

      {/* Destinations */}
      <section>
        <h2>Destinations</h2>
        <button>Add Destination</button>
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