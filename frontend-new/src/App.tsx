import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Scenarios from "./pages/Scenarios";
import Simulation from "./pages/SimulationsPage";
import Terrain from "./pages/Terrain";
import Viruses from "./pages/Viruses";
import Preventions from "./pages/Preventions";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Scenarios" element={<Scenarios />} />
        <Route path="/Simulation" element={<Simulation />} />
        <Route path="/Terrain" element={<Terrain />} />
        <Route path="/Viruses" element={<Viruses />} />
        <Route path="/Preventions" element={<Preventions />} />
      </Routes>
    </Router>
  );
}

export default App;
