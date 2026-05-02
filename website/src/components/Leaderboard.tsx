import { useState } from 'react';
import type { ExperimentData, LangFilter, TaskResult } from '../types/index.ts';
import { useSortable } from '../hooks/useSortable.ts';
import FilterPills from './FilterPills.tsx';
import SortHeader from './SortHeader.tsx';
import LeaderboardRow from './LeaderboardRow.tsx';

interface LeaderboardProps {
  experiments: ExperimentData[];
}

export interface FilteredStats {
  avg: number;
  passRate: number;
  passed: number;
  total: number;
  avgSafety: number | null;
  avgTokens: number;
  efficiency: number;
  costPerTask: number | null;
}

function getFilteredStats(exp: ExperimentData, filter: LangFilter): FilteredStats {
  let tasks: TaskResult[];
  if (filter === 'all') {
    tasks = exp.results;
  } else {
    tasks = exp.results.filter((r) => r.task.startsWith(filter + '_'));
  }
  const total = tasks.length;
  const passed = tasks.filter((t) => t.score >= 75).length;
  const avg = total > 0 ? tasks.reduce((s, t) => s + t.score, 0) / total : 0;
  const passRate = total > 0 ? (passed / total) * 100 : 0;

  const safetyTasks = tasks.filter((t) => t.safety_score != null);
  const avgSafety = safetyTasks.length > 0
    ? safetyTasks.reduce((s, t) => s + t.safety_score!, 0) / safetyTasks.length
    : null;

  const totalTokens = tasks.reduce((s, t) => s + (t.tokens || 0), 0);
  const avgTokens = total > 0 ? Math.round(totalTokens / total) : 0;

  const efficiency = avgTokens > 0 ? (avg / (avgTokens / 1000)) * 1000 : 0;

  // Cost per task lives at the summary level (aggregates all 80 tasks). Scale
  // it for the filtered subset using the ratio of filtered→total tokens, so
  // the language pills don't silently hide the cost column.
  const summaryCost = exp.summary.cost_per_task;
  const summaryTotalTokens = exp.summary.total_tokens ?? 0;
  let costPerTask: number | null = null;
  if (summaryCost != null) {
    if (filter === 'all' || summaryTotalTokens === 0) {
      costPerTask = summaryCost;
    } else {
      const avgCostPerToken = (summaryCost * exp.summary.total_tasks) / summaryTotalTokens;
      costPerTask = total > 0 ? (avgCostPerToken * totalTokens) / total : null;
    }
  }

  return { avg, passRate, passed, total, avgSafety, avgTokens, efficiency, costPerTask };
}

export default function Leaderboard({ experiments }: LeaderboardProps) {
  const [filter, setFilter] = useState<LangFilter>('all');
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const { sortKey, sortDir, toggleSort } = useSortable('avg_score', 'desc');

  const sorted = [...experiments]
    .map((exp) => ({ exp, stats: getFilteredStats(exp, filter) }))
    .sort((a, b) => {
      let va: number | string;
      let vb: number | string;
      switch (sortKey) {
        case 'model':
          va = a.exp.experiment.model;
          vb = b.exp.experiment.model;
          break;
        case 'agent':
          va = a.exp.experiment.agent;
          vb = b.exp.experiment.agent;
          break;
        case 'pass_rate':
          va = a.stats.passRate;
          vb = b.stats.passRate;
          break;
        case 'passed':
          va = a.stats.passed;
          vb = b.stats.passed;
          break;
        case 'safety':
          va = a.stats.avgSafety ?? 0;
          vb = b.stats.avgSafety ?? 0;
          break;
        case 'tokens':
          va = a.stats.avgTokens;
          vb = b.stats.avgTokens;
          break;
        case 'efficiency':
          va = a.stats.efficiency;
          vb = b.stats.efficiency;
          break;
        case 'cost':
          // Treat missing cost as +Infinity so they sort last ascending.
          va = a.stats.costPerTask ?? Number.POSITIVE_INFINITY;
          vb = b.stats.costPerTask ?? Number.POSITIVE_INFINITY;
          break;
        case 'avg_score':
        default:
          va = a.stats.avg;
          vb = b.stats.avg;
          break;
      }
      if (typeof va === 'string' && typeof vb === 'string') {
        return sortDir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
      }
      return sortDir === 'asc' ? (va as number) - (vb as number) : (vb as number) - (va as number);
    });

  return (
    <section id="leaderboard" className="leaderboard">
      <div className="container">
        <div className="leaderboard__header">
          <h2 className="leaderboard__title">Leaderboard</h2>
          <FilterPills filter={filter} onChange={setFilter} />
        </div>
        <div className="card leaderboard-table">
          <table>
            <thead>
              <tr>
                <SortHeader label="#" sortKey="rank" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Model" sortKey="model" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Avg Score" sortKey="avg_score" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Pass Rate" sortKey="pass_rate" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Safety" sortKey="safety" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Avg Tokens" sortKey="tokens" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="Efficiency" sortKey="efficiency" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <SortHeader label="$/task" sortKey="cost" currentKey={sortKey} currentDir={sortDir} onSort={toggleSort} />
                <th style={{ width: 32 }}></th>
              </tr>
            </thead>
            <tbody>
              {sorted.map(({ exp, stats }, i) => {
                const id = `${exp.experiment.model}_${exp.experiment.agent}`;
                return (
                  <LeaderboardRow
                    key={id}
                    experiment={exp}
                    rank={i + 1}
                    expanded={expandedId === id}
                    onToggle={() => setExpandedId(expandedId === id ? null : id)}
                    filter={filter}
                    filteredStats={stats}
                  />
                );
              })}
            </tbody>
          </table>
        </div>
        <p className="leaderboard__note">
          * A task is considered <strong>passed</strong> when its score ≥ 75 (out of 100).
          Costs use public list prices at paper submission time — see <code>analysis/pricing.example.json</code>.
        </p>
      </div>
    </section>
  );
}
