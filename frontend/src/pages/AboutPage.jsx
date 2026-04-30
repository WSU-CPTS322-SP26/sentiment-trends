import { useState } from "react";
import Header from "../components/Header";
import topicStyles from "../styles/pages/TopicDetailPage.module.css";
import styles from "../styles/pages/AboutPage.module.css";
import { appConfig } from "../constants";
import { useHomepageCards } from "../utils/HomepageCardsContext";
import { FaGithub } from "react-icons/fa";

const AboutPage = ({ theme, onToggleTheme }) => {
  const [results, setResults] = useState([]);
  const { navbarCategories } = useHomepageCards();

  return (
    <div className={topicStyles.DetailPage}>
      <Header
        title={appConfig.name}
        onSearch={setResults}
        results={results}
        categories={navbarCategories}
        theme={theme}
        onToggleTheme={onToggleTheme}
      />
      <div className={`${topicStyles.pageContainer} min-h-screen`}>
        <div className={`${topicStyles.content} py-4`}>
          <div
            className={`${topicStyles.panel} ${topicStyles.sectionCard} flex flex-col space-y-4`}
          >
            <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">About</h1>
            <p className={styles.lead}>
              Inspired by other forms of public opinion analysis, such as
              Polymarket and Google Trends, {appConfig.name} aims to provide a
              comprehensive view of public opinion based on social media data
              analysis. By leveraging advanced natural language processing
              techniques, we analyze sentiment and trends across various topics
              to help users understand the public discourse in real-time.
            </p>
            <br />
            <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Data Sources</h2>
            <p className={styles.lead}>
              We collect data from Mastodon and Bluesky, with plans to expand to
              other platforms in the future. Our data collection process is
              designed to be ethical and compliant with platform policies,
              ensuring that we respect user privacy and data rights.
            </p>
            <br />
            <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Authors</h2>
            <p className={styles.lead}>
              This project was developed by a small team of passionate devs from
              Washington State University who are dedicated to providing
              insights into public opinion through data analysis. We are
              committed to transparency and open-source principles, and we
              welcome contributions from the community to help improve and
              expand the capabilities of {appConfig.name}.
            </p>
            <br />
            <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Contact</h2>
            <p className={styles.lead}>
              If you have any questions, suggestions, or would like to
              contribute to the project, please feel free to reach out to us at{" "}
              <a
                className="font-medium text-[var(--color-primary)] underline-offset-2 hover:underline"
                href={`mailto:${appConfig.contactEmail}`}
              >
                {appConfig.contactEmail}
              </a>
              .
            </p>
            <div className="mt-auto flex w-full flex-row flex-wrap items-center justify-between gap-4 pt-4">
              <a
                href={appConfig.repoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-primary)] underline-offset-2 hover:underline"
              >
                <FaGithub
                  className="size-4 shrink-0 text-[var(--color-text-primary)]"
                  aria-hidden
                />
                GitHub repository
              </a>
              <a
                href={appConfig.issueTicketURL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-primary)] underline-offset-2 hover:underline"
              >
                Issues? Submit a ticket
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
