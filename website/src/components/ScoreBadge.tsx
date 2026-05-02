interface ScoreBadgeProps {
  score: number;
  threshold?: number;
}

export default function ScoreBadge({ score, threshold = 75 }: ScoreBadgeProps) {
  const variant = score >= threshold ? 'pass' : score >= 50 ? 'warn' : 'fail';
  return (
    <span className={`score-badge score-badge--${variant}`}>
      {score}
    </span>
  );
}
