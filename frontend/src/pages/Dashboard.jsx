function Dashboard() {
  const trips = [
    {
      id: 1,
      name: "Santa Fe Girls Trip",
      location: "Santa Fe, NM",
      startDate: "June 12",
      endDate: "June 14",
    },
    {
      id: 2,
      name: "Greenville Family Trip",
      location: "Greenville, SC",
      startDate: "July 24",
      endDate: "July 29",
    },
  ];

  return (
    <div>
      <h1>Upcoming Trips</h1>

      {trips.map((trip) => (
        <div key={trip.id}>
          <h2>{trip.name}</h2>
          <p>{trip.location}</p>
          <p>
            {trip.startDate} - {trip.endDate}
          </p>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;