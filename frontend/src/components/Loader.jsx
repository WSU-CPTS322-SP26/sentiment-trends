/* Credit to: https://cssloaders.github.io */
import styles from "../styles/components/Loader.module.css";

const Loader = () => {
    return (
        <div className="flex min-h-[550px] w-full flex-col items-center justify-center">
            <span className={styles.loader} />
        </div>
    );
}

export default Loader;