import React from "react";
import styles from "../styles/components/Header.module.css";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";
import Categories from "../components/Categories";
import { Link } from "react-router-dom";
import { useEffect, useRef } from "react";
import lightModeLogo from "../assets/light_mode_logo.png";
import darkModeLogo from "../assets/dark_mode_logo.png";

const Header = ({ title, onSearch, results, categories, theme, onToggleTheme }) => {
  const searchRef = useRef(null);
  const logoSrc = theme === "dark" ? darkModeLogo : lightModeLogo;
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
            <img
              className={styles.headerLogo}
              src={logoSrc}
              alt=""
              aria-hidden="true"
            />
            {title}
          </Link>
        </div>
        <div ref={searchRef} className={styles.headerSearch}>
          <SearchBar setResults={onSearch} />
          {results?.length > 0 && <SearchResultsList results={results} />}
        </div>
        <div className={styles.headerActions}>
          <Link to="/about" className={styles.aboutButton}>
            About
          </Link>
          <button
            type="button"
            className={styles.themeToggle}
            onClick={onToggleTheme}
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
            aria-pressed={theme === "dark"}
          >
            {theme === "dark" ? "Light" : "Dark"}
          </button>
        </div>
      </div>
      <Categories categories={categories} />
    </div>
  );
};

export default Header;
