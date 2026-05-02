import type { ExperimentData, LangFilter } from '../types/index.ts';
import type { FilteredStats } from './Leaderboard.tsx';
import { ChevronDown, ChevronRight } from 'lucide-react';
import TaskDetail from './TaskDetail.tsx';

interface LeaderboardRowProps {
  experiment: ExperimentData;
  rank: number;
  expanded: boolean;
  onToggle: () => void;
  filter: LangFilter;
  filteredStats: FilteredStats;
}

function formatTokens(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(0) + 'k';
  return String(n);
}

function formatCost(cost: number): string {
  if (cost >= 10) return `$${cost.toFixed(1)}`;
  if (cost >= 1) return `$${cost.toFixed(2)}`;
  return `$${cost.toFixed(2)}`;
}

export default function LeaderboardRow({ experiment, rank, expanded, onToggle, filter, filteredStats }: LeaderboardRowProps) {
  const { avg, passRate, passed, total, avgSafety, avgTokens, efficiency, costPerTask } = filteredStats;

  const progressColor = avg >= 70 ? 'var(--pass)' : avg >= 50 ? 'var(--warn)' : 'var(--fail)';
  const safetyColor = (avgSafety ?? 0) >= 90 ? 'var(--pass)' : (avgSafety ?? 0) >= 70 ? 'var(--warn)' : 'var(--fail)';
  const costColor = costPerTask == null
    ? 'var(--text-muted)'
    : costPerTask >= 10 ? 'var(--fail)'
    : costPerTask >= 3 ? 'var(--warn)'
    : 'var(--pass)';

  const rankClass = rank <= 3 ? ` rank-badge--${rank}` : '';

  return (
    <>
      <tr className={`leaderboard-row${expanded ? ' leaderboard-row--expanded' : ''}`} onClick={onToggle}>
        <td>
          <span className={`rank-badge${rankClass}`}>{rank}</span>
        </td>
        <td>
          <div>
            <span className="model-name">{experiment.experiment.model}</span>
            <span className="agent-badge" style={{ marginLeft: 8 }}>{experiment.experiment.agent}</span>
          </div>
        </td>
        <td>
          <div className="score-cell">
            <span className="score-value">{avg.toFixed(1)}</span>
            <div className="progress-bar">
              <div
                className="progress-bar__fill"
                style={{ width: `${avg}%`, background: progressColor }}
              />
            </div>
          </div>
        </td>
        <td>
          <span className="mono" style={{ fontWeight: 600 }}>{passRate.toFixed(1)}%</span>
          <span className="text-muted" style={{ marginLeft: 4, fontSize: '0.75rem' }}>({passed}/{total})</span>
        </td>
        <td>
          {avgSafety != null ? (
            <span className="mono" style={{ fontWeight: 600, color: safetyColor }}>{avgSafety.toFixed(1)}</span>
          ) : (
            <span className="text-muted">-</span>
          )}
        </td>
        <td>
          <span className="mono">{formatTokens(avgTokens)}</span>
        </td>
        <td>
          <span className="mono" style={{ fontSize: '0.75rem' }}>{efficiency.toFixed(2)}</span>
        </td>
        <td>
          {costPerTask != null ? (
            <span className="mono" style={{ fontWeight: 600, color: costColor }}>{formatCost(costPerTask)}</span>
          ) : (
            <span className="text-muted">-</span>
          )}
        </td>
        <td>
          {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        </td>
      </tr>
      {expanded && (
        <TaskDetail experiment={experiment} filter={filter} />
      )}
    </>
  );
}
