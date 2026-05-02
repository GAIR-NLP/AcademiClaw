import type { ExperimentData } from '../types/index.ts';
import StatsCards from './StatsCards.tsx';

interface HeroProps {
  experiments: ExperimentData[];
}

export default function Hero({ experiments }: HeroProps) {
  const totalTasks = experiments.length > 0 ? experiments[0].summary.total_tasks : 0;
  const modelCount = experiments.length;
  const bestPassRate = experiments.length > 0
    ? Math.max(...experiments.map((e) => e.summary.pass_rate))
    : 0;
  const safetyValues = experiments
    .map((e) => e.summary.avg_safety)
    .filter((v): v is number => typeof v === 'number');
  const avgSafety = safetyValues.length > 0
    ? safetyValues.reduce((a, b) => a + b, 0) / safetyValues.length
    : null;

  return (
    <section className="hero">
      <div className="container">
        <h1 className="hero__title">
          <span>Academi</span>Claw
        </h1>
        <p className="hero__subtitle">
          Comprehensive evaluation benchmark for AI coding agents on real-world academic work.
          Measuring task completion, safety, and efficiency across {totalTasks} diverse challenges.
        </p>
        <StatsCards
          totalTasks={totalTasks}
          modelCount={modelCount}
          bestPassRate={bestPassRate}
          avgSafety={avgSafety}
        />
      </div>
    </section>
  );
}
