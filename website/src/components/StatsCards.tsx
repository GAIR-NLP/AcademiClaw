import { ListChecks, Bot, Trophy, Shield } from 'lucide-react';

interface StatsCardsProps {
  totalTasks: number;
  modelCount: number;
  bestPassRate: number;
  avgSafety?: number | null;
}

export default function StatsCards({ totalTasks, modelCount, bestPassRate, avgSafety }: StatsCardsProps) {
  const cards = [
    {
      icon: <ListChecks size={20} />,
      bg: '#dbeafe',
      color: '#2563eb',
      value: totalTasks,
      label: 'Total Tasks',
    },
    {
      icon: <Bot size={20} />,
      bg: '#f3e8ff',
      color: '#7c3aed',
      value: modelCount,
      label: 'Models Evaluated',
    },
    {
      icon: <Trophy size={20} />,
      bg: '#dcfce7',
      color: '#16a34a',
      value: `${bestPassRate.toFixed(1)}%`,
      label: 'Best Pass Rate',
    },
    {
      icon: <Shield size={20} />,
      bg: '#fef3c7',
      color: '#d97706',
      value: avgSafety != null ? `${avgSafety.toFixed(1)}` : '—',
      label: 'Avg Safety Score',
    },
  ];

  return (
    <div className="stats-row">
      {cards.map((c) => (
        <div key={c.label} className="card card-hover stat-card">
          <div className="stat-card__icon" style={{ background: c.bg, color: c.color }}>
            {c.icon}
          </div>
          <div className="stat-card__value">{c.value}</div>
          <div className="stat-card__label">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
