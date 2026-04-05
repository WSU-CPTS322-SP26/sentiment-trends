import React from "react";
import styles from "../styles/components/Header.module.css";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";
import Categories from "../components/Categories"
import { Link } from "react-router-dom";
import { useEffect, useRef } from "react";

const Header = ({ title, onSearch, results, categories }) => {
    const searchRef = useRef(null);
    useEffect(() => {
    const close = (e) => {
        if (searchRef.current && !searchRef.current.contains(e.target)) {
        onSearch([]);
        }
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
    }, [onSearch]);
    return (
        <div className={styles.header}>
            <div className={styles.headerContainer}>
                <div className={styles.headerTitleContainer}>
                    <Link to="/" className={styles.headerTitle}>
                        {title}
                    </Link>                
                </div>
                <div ref={searchRef} className={styles.headerSearch}>
                    <SearchBar setResults={onSearch} />
                    {results?.length > 0 && <SearchResultsList results={results} />}
                </div>
            </div>
            <Categories categories={categories} />
        </div>
    );
}

export default Header;