import {useState, useRef} from "react";
import styles from "../styles/components/Categories.module.css";

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
                <a
                    key={category.id}
                    href={category.href}
                    className={styles.categoryItem}
                >
                    {category.label}
                </a>
            ))}
            </div>
        </div>
    );
};

export default Categories;