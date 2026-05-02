import type { SortKey, SortDir } from '../types/index.ts';
import { ArrowUp, ArrowDown, ArrowUpDown } from 'lucide-react';

interface SortHeaderProps {
  label: string;
  sortKey: SortKey;
  currentKey: SortKey;
  currentDir: SortDir;
  onSort: (key: SortKey) => void;
}

export default function SortHeader({ label, sortKey, currentKey, currentDir, onSort }: SortHeaderProps) {
  const active = sortKey === currentKey;
  return (
    <th onClick={() => onSort(sortKey)} style={active ? { color: 'var(--primary)' } : undefined}>
      {label}
      <span className="sort-icon">
        {active ? (
          currentDir === 'asc' ? <ArrowUp size={12} /> : <ArrowDown size={12} />
        ) : (
          <ArrowUpDown size={12} />
        )}
      </span>
    </th>
  );
}
