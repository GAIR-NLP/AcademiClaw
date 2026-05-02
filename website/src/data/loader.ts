import type { Manifest, ExperimentData, TaskCatalogItem } from '../types/index.ts';

const DATA_BASE = import.meta.env.BASE_URL + 'data/';

export async function loadManifest(): Promise<Manifest> {
  const res = await fetch(DATA_BASE + 'manifest.json');
  if (!res.ok) throw new Error(`Failed to load manifest: ${res.status}`);
  return res.json();
}

export async function loadExperiment(filename: string): Promise<ExperimentData> {
  const res = await fetch(DATA_BASE + filename);
  if (!res.ok) throw new Error(`Failed to load ${filename}: ${res.status}`);
  return res.json();
}

export async function loadAllExperiments(): Promise<ExperimentData[]> {
  const manifest = await loadManifest();
  const experiments = await Promise.all(
    manifest.files.map((f) => loadExperiment(f))
  );
  return experiments;
}

export async function loadTasksCatalog(): Promise<TaskCatalogItem[]> {
  const res = await fetch(DATA_BASE + 'tasks-catalog.json');
  if (!res.ok) throw new Error(`Failed to load tasks catalog: ${res.status}`);
  return res.json();
}
