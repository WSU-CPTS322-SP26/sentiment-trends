import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  
import HomePage from "./pages/HomePage";
import TopicDetailPage from "./pages/TopicDetailPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/topic/:topic" element={<TopicDetailPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;