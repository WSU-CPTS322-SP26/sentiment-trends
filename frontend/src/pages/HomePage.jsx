import { useState } from "react";
import Header from "../components/Header";
import Card from "../components/Card";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";
import { mockCards, mockCategories } from "../../mocks/data/mock_data";
import { useSearchParams } from "react-router-dom";

const predefinedCategories = mockCategories.map(c => c.label);
const fromCards = [...new Set(mockCards.map(c => c.category))];
const ordered = [...new Set([...predefinedCategories, ...fromCards])]
  .filter(Boolean)
  .map((label, i) => ({
    id: i,
    label,
    href: label === "All" ? "/" : `/?category=${encodeURIComponent(label)}`
  }));

const HomePage = () => {

const [searchParams] = useSearchParams();
const catParam = searchParams.get("category");
const [results, setResults] = useState([]);
const filteredCards = !catParam || catParam === "All" ? mockCards : mockCards.filter(c => c.category === catParam); 


  return (

    <div className={styles.HomePage}>
      <Header title={appConfig.name} 
        onSearch={setResults} 
        results={results}
        categories={ordered}
      />
      <div className={styles.pageContainer}>
        <div className={styles.cardsContainer}>
          {filteredCards.map((card) => 
          <Card key={card.id} card={card} />
          )}
        </div>
      </div>
    </div>
    
  );
}

export default HomePage;