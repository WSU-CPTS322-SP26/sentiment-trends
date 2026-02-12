import { useState } from "react";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";
import Header from "../components/Header";
import Card from "../components/Card";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";
import { mockCards } from "../../mocks/data/mock_data";


const HomePage = () => {

const [results, setResults] = useState([]);

  return (

    <div className={styles.HomePage}>

      <Header title={appConfig.name} 
        onSearch={setResults} 
        results={results}
      />

      <div className={styles.pageContainer}>
        <div className={styles.cardsContainer}>
          {mockCards.map((card) => 
          <Card key={card.id} {...card} />
          )}
        </div>
      </div>
    </div>
    
  );
}

export default HomePage;