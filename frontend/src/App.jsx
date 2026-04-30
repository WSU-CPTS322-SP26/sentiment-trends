import "./App.css";
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";  
import HomePage from "./pages/HomePage";
import TopicDetailPage from "./pages/TopicDetailPage";
import { HomepageCardsProvider } from "./utils/HomepageCardsContext";
import AboutPage from "./pages/AboutPage";

function App() {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "light" || savedTheme === "dark") {
      return savedTheme;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  });

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("theme", theme);
  }, [theme]);

  const handleToggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <HomepageCardsProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route
              path="/"
              element={<HomePage theme={theme} onToggleTheme={handleToggleTheme} />}
            />
            <Route
              path="/topic/:topic"
              element={
                <TopicDetailPage theme={theme} onToggleTheme={handleToggleTheme} />
              }
            />
            <Route
              path="/about"
              element={<AboutPage theme={theme} onToggleTheme={handleToggleTheme} />}
            />
          </Routes>
        </div>
      </Router>
    </HomepageCardsProvider>
  );
}

export default App;