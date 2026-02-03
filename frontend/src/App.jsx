import { useState, useEffect } from "react";
import styles from "./App.module.css";

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className={styles.root}>
      <h1 className={styles.title}>Sentiment Trends</h1>
      {loading && <p>Loading...</p>}
      {error && <p className={styles.error}>Error: {error}</p>}
      {data?.message && <p className={styles.message}>{data.message}</p>}
    </div>
  );
}

export default App;
