import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

function CreateTrip() {
  const [form, setForm] = useState({
    trip_name: "",
    description: "",
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

    const res = await fetch(`${API_URL}/trips`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        ...form,
        owner_user_id: 1 // temp hardcode for MVP
      })
    });

    const data = await res.json();
    console.log(data);

    // redirect after create
    window.location.href = "/";
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="trip_name" placeholder="Trip Name" onChange={handleChange} />
      <input name="trip_name" placeholder="Destination" onChange={handleChange} />
      <input name="description" placeholder="Description" onChange={handleChange} />
      <input type="date" name="start_date" onChange={handleChange} />
      <input type="date" name="end_date" onChange={handleChange} />

      <button type="submit">Create Trip</button>
    </form>
  );
}

export default CreateTrip;