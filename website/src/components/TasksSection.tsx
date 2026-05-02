import { useState, useMemo } from 'react';
import { Search } from 'lucide-react';
import { useTasksCatalog } from '../hooks/useTasksCatalog.ts';
import type { LangFilter } from '../types/index.ts';
import TaskCard from './TaskCard.tsx';

const languages: { label: string; value: LangFilter }[] = [
  { label: 'All', value: 'all' },
  { label: 'English', value: 'en' },
  { label: 'Chinese', value: 'zh' },
];

export default function TasksSection() {
  const { tasks, loading, error } = useTasksCatalog();
  const [langFilter, setLangFilter] = useState<LangFilter>('all');
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    let result = tasks;
    if (langFilter !== 'all') {
      result = result.filter((t) => t.lang === langFilter);
    }
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      result = result.filter(
        (t) =>
          t.name.toLowerCase().includes(q) ||
          t.task_id.toLowerCase().includes(q) ||
          t.query_snippet.toLowerCase().includes(q)
      );
    }
    return result;
  }, [tasks, langFilter, search]);

  if (loading) {
    return (
      <section id="tasks" className="tasks-section">
        <div className="container">
          <div className="spinner" />
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="tasks" className="tasks-section">
        <div className="container">
          <p className="error-state">Failed to load tasks: {error}</p>
        </div>
      </section>
    );
  }

  return (
    <section id="tasks" className="tasks-section">
      <div className="container">
        <div className="tasks-header">
          <h2 className="section-title">Tasks</h2>
          <span className="tasks-count">{filtered.length} of {tasks.length} tasks</span>
        </div>

        <div className="tasks-filters">
          <div className="filter-pills">
            {languages.map((l) => (
              <button
                key={l.value}
                className={`filter-pill${langFilter === l.value ? ' filter-pill--active' : ''}`}
                onClick={() => setLangFilter(l.value)}
              >
                {l.label}
              </button>
            ))}
          </div>
          <div className="search-box">
            <Search size={16} className="search-box__icon" />
            <input
              type="text"
              className="search-input"
              placeholder="Search tasks by name or ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        {filtered.length === 0 ? (
          <p className="tasks-empty">No tasks match your filters.</p>
        ) : (
          <div className="tasks-grid">
            {filtered.map((task) => (
              <TaskCard key={task.task_id} task={task} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
