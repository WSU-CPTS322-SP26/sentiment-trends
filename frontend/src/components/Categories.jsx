import {useState, useRef} from "react";
import styles from "../styles/components/Categories.module.css";
import { Link } from "react-router-dom";

const Categories = ({ categories = []}) => {
    const [hasScrolled, setHasScrolled] = useState(false);
    const containerRef = useRef(null);
    const handleScroll = () => {
        setHasScrolled((containerRef.current?.scrollLeft ?? 0) > 0);
    };

    return (
        <div ref={containerRef} 
        className={`${styles.categoryContainer} ${hasScrolled ? styles.scrolled : ""}`}
        onScroll={handleScroll} >
            <div className={styles.categoryInner}>
            {categories.map((category) => (
                <Link
                    key={category.id}
                    to={category.href}
                    className={styles.categoryItem}
                >
                    {category.label}
                </Link>
            ))}
            </div>
        </div>
    );
};

export default Categories;