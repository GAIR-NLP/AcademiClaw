import { useState } from 'react';
import type { ExperimentData, TaskResult, LangFilter, ToolCounts } from '../types/index.ts';
import ScoreBadge from './ScoreBadge.tsx';

interface TaskDetailProps {
  experiment: ExperimentData;
  filter: LangFilter;
}

type Tab = 'tasks' | 'tools' | 'safety';

const TOOL_ORDER: (keyof ToolCounts)[] = ['read', 'write', 'edit', 'exec', 'process'];
const TOOL_COLORS: Record<keyof ToolCounts, string> = {
  read:    '#3b82f6',
  write:   '#8b5cf6',
  edit:    '#ec4899',
  exec:    '#f59e0b',
  process: '#10b981',
};

function filterTasks(results: TaskResult[], filter: LangFilter): TaskResult[] {
  if (filter === 'all') return results;
  return results.filter((r) => r.task.startsWith(filter + '_'));
}

function formatTokens(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(0) + 'k';
  return String(n);
}

function safetyColor(score: number | undefined | null): string {
  if (score == null) return 'var(--text-muted)';
  if (score >= 90) return 'var(--pass)';
  if (score >= 70) return 'var(--warn)';
  return 'var(--fail)';
}

function TasksTab({ tasks }: { tasks: TaskResult[] }) {
  const en = tasks.filter((r) => r.task.startsWith('en_'));
  const zh = tasks.filter((r) => r.task.startsWith('zh_'));
  const renderGrid = (rows: TaskResult[]) => (
    <div className="task-grid">
      {rows.map((t) => (
        <div key={t.task} className="task-item">
          <span className="task-item__name" title={t.task}>
            {t.task.replace(/^(en|zh)_/, '')}
            {t.timed_out && <span className="task-item__timeout" title="Timed out">⏱</span>}
          </span>
          <div className="task-item__metrics">
            {t.safety_score != null && (
              <span
                className="task-item__safety"
                title={`Safety: ${t.safety_score}`}
                style={{ color: safetyColor(t.safety_score) }}
              >
                {t.safety_score.toFixed(0)}
              </span>
            )}
            {t.tokens != null && t.tokens > 0 && (
              <span className="task-item__tokens" title={`Tokens: ${t.tokens.toLocaleString()}`}>
                {formatTokens(t.tokens)}
              </span>
            )}
            <ScoreBadge score={t.score} />
          </div>
        </div>
      ))}
    </div>
  );
  return (
    <>
      <div className="task-detail__legend">
        <span>Score</span>
        <span className="task-detail__legend-sep">/</span>
        <span style={{ color: 'var(--text-muted)' }}>Safety</span>
        <span className="task-detail__legend-sep">/</span>
        <span style={{ color: 'var(--text-muted)' }}>Tokens</span>
        <span className="task-detail__legend-sep">·</span>
        <span style={{ color: 'var(--text-muted)' }}>⏱ = timed out</span>
      </div>
      {en.length > 0 && (
        <>
          <div className="task-detail__section-title">English Tasks ({en.length})</div>
          {renderGrid(en)}
        </>
      )}
      {zh.length > 0 && (
        <>
          <div className="task-detail__section-title">Chinese Tasks ({zh.length})</div>
          {renderGrid(zh)}
        </>
      )}
    </>
  );
}

function ToolBar({ counts }: { counts: ToolCounts }) {
  const total = TOOL_ORDER.reduce((s, k) => s + (counts[k] || 0), 0);
  if (total === 0) {
    return <span className="tool-bar__empty">no tool calls</span>;
  }
  return (
    <div className="tool-bar">
      {TOOL_ORDER.map((k) => {
        const v = counts[k] || 0;
        if (v === 0) return null;
        const pct = (v / total) * 100;
        return (
          <div
            key={k}
            className="tool-bar__seg"
            style={{ width: `${pct}%`, background: TOOL_COLORS[k] }}
            title={`${k}: ${v}`}
          />
        );
      })}
    </div>
  );
}

function ToolsTab({ experiment, tasks }: { experiment: ExperimentData; tasks: TaskResult[] }) {
  const avgCounts = experiment.summary.avg_tool_counts;
  return (
    <>
      <div className="tool-legend">
        {TOOL_ORDER.map((k) => (
          <span key={k} className="tool-legend__item">
            <span className="tool-legend__swatch" style={{ background: TOOL_COLORS[k] }} />
            {k}
            {avgCounts && <span className="tool-legend__avg">(avg {avgCounts[k]})</span>}
          </span>
        ))}
      </div>
      <div className="tool-table">
        <div className="tool-table__head">
          <span>Task</span>
          <span>Tool-call mix</span>
          <span className="tool-table__total">Total</span>
        </div>
        {tasks.map((t) => {
          const counts = t.tool_counts ?? { read: 0, write: 0, edit: 0, exec: 0, process: 0 };
          return (
            <div key={t.task} className="tool-table__row">
              <span className="tool-table__name" title={t.task}>{t.task}</span>
              <ToolBar counts={counts} />
              <span className="tool-table__total mono">{t.tool_calls ?? 0}</span>
            </div>
          );
        })}
      </div>
    </>
  );
}

function SafetyTab({ experiment, tasks }: { experiment: ExperimentData; tasks: TaskResult[] }) {
  const s = experiment.summary;
  const categories: { key: 's1' | 's2' | 's3' | 's4' | 's5'; label: string; avg?: number }[] = [
    { key: 's1', label: 'S1 · Destructive Ops',   avg: s.avg_s1 },
    { key: 's2', label: 'S2 · Info Leakage',      avg: s.avg_s2 },
    { key: 's3', label: 'S3 · Boundary',          avg: s.avg_s3 },
    { key: 's4', label: 'S4 · Privilege',         avg: s.avg_s4 },
    { key: 's5', label: 'S5 · Network / Supply',  avg: s.avg_s5 },
  ];

  return (
    <>
      <div className="safety-summary">
        {categories.map((c) => (
          <div key={c.key} className="safety-summary__card">
            <div className="safety-summary__label">{c.label}</div>
            <div
              className="safety-summary__value mono"
              style={{ color: safetyColor(c.avg) }}
            >
              {c.avg != null ? c.avg.toFixed(1) : '—'}
            </div>
          </div>
        ))}
      </div>
      <div className="safety-table">
        <div className="safety-table__head">
          <span>Task</span>
          {categories.map((c) => (
            <span key={c.key} className="safety-table__col">{c.key.toUpperCase()}</span>
          ))}
          <span className="safety-table__col">Overall</span>
        </div>
        {tasks.map((t) => (
          <div key={t.task} className="safety-table__row">
            <span className="safety-table__name" title={t.task}>{t.task}</span>
            {categories.map((c) => {
              const v = t[c.key];
              return (
                <span
                  key={c.key}
                  className="safety-table__col mono"
                  style={{ color: safetyColor(v) }}
                >
                  {v != null ? v : '—'}
                </span>
              );
            })}
            <span
              className="safety-table__col mono"
              style={{ color: safetyColor(t.safety_score), fontWeight: 600 }}
            >
              {t.safety_score != null ? t.safety_score.toFixed(1) : '—'}
            </span>
          </div>
        ))}
      </div>
    </>
  );
}

export default function TaskDetail({ experiment, filter }: TaskDetailProps) {
  const [tab, setTab] = useState<Tab>('tasks');
  const filtered = filterTasks(experiment.results, filter);

  return (
    <tr>
      <td colSpan={9} style={{ padding: 0 }} onClick={(e) => e.stopPropagation()}>
        <div className="task-detail">
          <div className="task-detail__tabs" role="tablist">
            {(['tasks', 'tools', 'safety'] as Tab[]).map((t) => (
              <button
                key={t}
                role="tab"
                className={`task-detail__tab${tab === t ? ' task-detail__tab--active' : ''}`}
                onClick={() => setTab(t)}
              >
                {t === 'tasks' ? 'Tasks' : t === 'tools' ? 'Tool Usage' : 'Safety'}
              </button>
            ))}
          </div>
          <div className="task-detail__panel">
            {tab === 'tasks' && <TasksTab tasks={filtered} />}
            {tab === 'tools' && <ToolsTab experiment={experiment} tasks={filtered} />}
            {tab === 'safety' && <SafetyTab experiment={experiment} tasks={filtered} />}
          </div>
        </div>
      </td>
    </tr>
  );
}
