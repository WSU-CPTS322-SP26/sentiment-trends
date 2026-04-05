import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  
import HomePage from "./pages/HomePage";
import TopicDetailPage from "./pages/TopicDetailPage";
import { HomepageCardsProvider } from "./utils/HomepageCardsContext";
import AboutPage from "./pages/AboutPage";

function App() {
  return (
    <HomepageCardsProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/topic/:topic" element={<TopicDetailPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </div>
      </Router>
    </HomepageCardsProvider>
  );
}

export default App;