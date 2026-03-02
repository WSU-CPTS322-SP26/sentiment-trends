import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  
import HomePage from "./pages/HomePage";
import CardDetailPage from "./pages/CardDetailPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/card/:id" element={<CardDetailPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;