import { useState, useCallback } from 'react';
import type { SortKey, SortDir } from '../types/index.ts';

interface UseSortableResult {
  sortKey: SortKey;
  sortDir: SortDir;
  toggleSort: (key: SortKey) => void;
}

export function useSortable(defaultKey: SortKey = 'avg_score', defaultDir: SortDir = 'desc'): UseSortableResult {
  const [sortKey, setSortKey] = useState<SortKey>(defaultKey);
  const [sortDir, setSortDir] = useState<SortDir>(defaultDir);

  const toggleSort = useCallback((key: SortKey) => {
    if (key === sortKey) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir('desc');
    }
  }, [sortKey]);

  return { sortKey, sortDir, toggleSort };
}
