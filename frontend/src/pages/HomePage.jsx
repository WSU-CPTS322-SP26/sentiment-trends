import { useState } from "react";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";
import styles from "../styles/pages/HomePage.module.css";


const HomePage = () => {

const [results, setResults] = useState([]);

  return (

    <div className={styles.HomePage}>
      <h1 className={styles.title}>Sentiment Trends</h1>
      <div className={styles.subtitle}>Discover the pulse of public opinion with our sentiment analysis tool.</div>
      <div className={styles.searchBarContainer}>
        <SearchBar setResults={setResults}/>
        <SearchResultsList results = {results}/>
      </div>
    </div>
    
  );
}

export default HomePage;