import type { LangFilter } from '../types/index.ts';

interface FilterPillsProps {
  filter: LangFilter;
  onChange: (f: LangFilter) => void;
}

const filters: { value: LangFilter; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'en', label: 'English' },
  { value: 'zh', label: 'Chinese' },
];

export default function FilterPills({ filter, onChange }: FilterPillsProps) {
  return (
    <div className="filter-pills">
      {filters.map((f) => (
        <button
          key={f.value}
          className={`filter-pill${filter === f.value ? ' filter-pill--active' : ''}`}
          onClick={() => onChange(f.value)}
        >
          {f.label}
        </button>
      ))}
    </div>
  );
}
