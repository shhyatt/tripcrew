
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import TripDetail from "./pages/TripDetail";
import CreateTrip from "./pages/CreateTrip";
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/trips/:tripId" element={<TripDetail />} />
        <Route path="/trips" element={<TripDetail />} />
        <Route path="/trips/new" element={<CreateTrip />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

