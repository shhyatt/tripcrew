import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_URL;

function CreateDestination() {
    const { tripId } = useParams();
    const [form, setForm] = useState({
    location_name: "",
    start_date: "",
    end_date: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch(`${API_URL}/trips/${tripId}/destinations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        ...form,
        trip_id: tripId,
      })
    });

    const data = await res.json();
    console.log(data);

    // redirect after create
    window.location.href = `/trips/${tripId}`;
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="location_name" placeholder="Destination Name" onChange={handleChange} />
      <input type="date" name="start_date" onChange={handleChange} />
      <input type="date" name="end_date" onChange={handleChange} />

      <button type="submit">Add Destination</button>
    </form>
  );
}

export default CreateDestination;