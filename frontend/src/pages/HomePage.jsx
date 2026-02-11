import { useState } from "react";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";
import Header from "../components/Header";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";


const HomePage = () => {

const [results, setResults] = useState([]);

  return (

    <div className={styles.HomePage}>
      <Header title={appConfig.name} onSearch={setResults} results={results}/>
    </div>
    
  );
}

export default HomePage;