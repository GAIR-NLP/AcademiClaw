import { useState, useEffect } from 'react';
import type { TaskCatalogItem } from '../types/index.ts';
import { loadTasksCatalog } from '../data/loader.ts';

interface UseTasksCatalogResult {
  tasks: TaskCatalogItem[];
  loading: boolean;
  error: string | null;
}

export function useTasksCatalog(): UseTasksCatalogResult {
  const [tasks, setTasks] = useState<TaskCatalogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    loadTasksCatalog()
      .then((data) => {
        if (!cancelled) {
          setTasks(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      });
    return () => { cancelled = true; };
  }, []);

  return { tasks, loading, error };
}
