import { useState, useEffect, useCallback } from 'react';
import { useExperiments } from './hooks/useExperiments.ts';
import Navbar from './components/Navbar.tsx';
import Hero from './components/Hero.tsx';
import Leaderboard from './components/Leaderboard.tsx';
import TasksSection from './components/TasksSection.tsx';

type Page = 'leaderboard' | 'tasks';

function getPageFromHash(): Page {
  const hash = window.location.hash.replace('#', '');
  if (hash === 'tasks') return 'tasks';
  return 'leaderboard';
}

function App() {
  const { experiments, loading, error } = useExperiments();
  const [page, setPage] = useState<Page>(getPageFromHash);

  const onHashChange = useCallback(() => {
    setPage(getPageFromHash());
  }, []);

  useEffect(() => {
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, [onHashChange]);

  if (loading) {
    return (
      <>
        <Navbar activePage={page} />
        <div className="loading-state">
          <div className="spinner" />
          <span>Loading...</span>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Navbar activePage={page} />
        <div className="error-state">
          <p>Failed to load data: {error}</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar activePage={page} />
      {page === 'leaderboard' ? (
        <>
          <Hero experiments={experiments} />
          <Leaderboard experiments={experiments} />
        </>
      ) : (
        <TasksSection />
      )}
      <footer className="footer">
        <div className="container">
          AcademiClaw · Evaluation Dashboard · <a href="https://github.com/GAIR-NLP/AcademiClaw" target="_blank" rel="noopener noreferrer">GAIR-NLP/AcademiClaw</a>
        </div>
      </footer>
    </>
  );
}

export default App;
