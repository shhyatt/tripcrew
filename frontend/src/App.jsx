
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import TripDetail from "./pages/TripDetail";
import CreateTrip from "./pages/CreateTrip";
import CreateDestination from "./pages/CreateDestination";
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trips/:tripId" element={<TripDetail />} />
        <Route path="/trips" element={<TripDetail />} />
        <Route path="/trips/new" element={<CreateTrip />} />
        <Route path="/trips/:tripId/new_destination" element={<CreateDestination />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

