import { useState, useEffect } from 'react';
import type { ExperimentData } from '../types/index.ts';
import { loadAllExperiments } from '../data/loader.ts';

interface UseExperimentsResult {
  experiments: ExperimentData[];
  loading: boolean;
  error: string | null;
}

export function useExperiments(): UseExperimentsResult {
  const [experiments, setExperiments] = useState<ExperimentData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    loadAllExperiments()
      .then((data) => {
        if (!cancelled) {
          setExperiments(data);
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

  return { experiments, loading, error };
}
